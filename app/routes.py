from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_file, abort, current_app
from flask_login import login_required, current_user
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import or_
from app import db
from app.models import Book, Category, CartItem, Order, OrderItem, Review
from app.forms import ReviewForm, CheckoutForm, SearchForm, BookForm
from datetime import datetime
import os
import json
import stripe

main_bp = Blueprint('main', __name__)
csrf = CSRFProtect()


@main_bp.route('/')
def index():
    """Home page with featured books"""
    featured_books = Book.query.order_by(Book.created_at.desc()).limit(8).all()
    categories = Category.query.all()
    return render_template('index.html', 
                         featured_books=featured_books,
                         categories=categories,
                         title='CyberBooks - Cybersecurity E-Library')


@main_bp.route('/shop')
def shop():
    """Shop page with search and filtering"""
    form = SearchForm(request.args, meta={'csrf': False})
    
    # Base query
    query = Book.query
    
    # Search by keyword (title or author)
    search_term = request.args.get('query', '').strip()
    if search_term:
        query = query.filter(
            or_(
                Book.title.ilike(f'%{search_term}%'),
                Book.author.ilike(f'%{search_term}%')
            )
        )
    
    # Filter by category
    category_id = request.args.get('category', type=int)
    if category_id and category_id != 0:
        query = query.filter(Book.category_id == category_id)
    
    # Filter by price range
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    if min_price is not None and min_price > 0:
        query = query.filter(Book.price >= min_price)
    if max_price is not None and max_price > 0:
        query = query.filter(Book.price <= max_price)
    
    # Sorting
    sort_by = request.args.get('sort_by', 'newest')
    if sort_by == 'oldest':
        query = query.order_by(Book.created_at.asc())
    elif sort_by == 'price_low':
        query = query.order_by(Book.price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(Book.price.desc())
    elif sort_by == 'rating':
        # Sort by average rating - using subquery for efficiency
        from sqlalchemy import func
        rating_subq = db.session.query(
            Review.book_id,
            func.avg(Review.rating).label('avg_rating')
        ).group_by(Review.book_id).subquery()
        
        query = query.outerjoin(rating_subq, Book.id == rating_subq.c.book_id)\
                    .order_by(rating_subq.c.avg_rating.desc().nullslast())
    else:  # newest (default)
        query = query.order_by(Book.created_at.desc())
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    books = query.paginate(page=page, per_page=12, error_out=False)
    
    # Get all categories for filter
    form.category.choices = [(0, 'All Categories')] + [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    
    return render_template('shop.html', 
                         books=books, 
                         form=form,
                         title='Shop - CyberBooks')


@main_bp.route('/book/<int:book_id>')
def book_detail(book_id):
    """Book detail page"""
    book = Book.query.get_or_404(book_id)
    
    # Paginate reviews
    page = request.args.get('page', 1, type=int)
    reviews = Review.query.filter_by(book_id=book_id).order_by(Review.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Check if user has purchased this book
    has_purchased = False
    if current_user.is_authenticated:
        has_purchased = OrderItem.query.join(Order).filter(
            Order.user_id == current_user.id,
            OrderItem.book_id == book_id,
            Order.status == 'completed'
        ).first() is not None
    
    return render_template('book_detail.html', 
                         book=book, 
                         reviews=reviews,
                         has_purchased=has_purchased,
                         title=book.title)


@main_bp.route('/book/<int:book_id>/review', methods=['GET', 'POST'])
@login_required
def add_review(book_id):
    """Add a review for a book"""
    book = Book.query.get_or_404(book_id)
    
    # Check if user has purchased this book
    has_purchased = OrderItem.query.join(Order).filter(
        Order.user_id == current_user.id,
        OrderItem.book_id == book_id,
        Order.status == 'completed'
    ).first() is not None
    
    if not has_purchased:
        flash('You can only review books you have purchased.', 'warning')
        return redirect(url_for('main.book_detail', book_id=book_id))
    
    # Check if user already reviewed this book
    existing_review = Review.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if existing_review:
        flash('You have already reviewed this book.', 'info')
        return redirect(url_for('main.book_detail', book_id=book_id))
    
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            user_id=current_user.id,
            book_id=book_id,
            rating=form.rating.data,
            comment=form.comment.data
        )
        
        db.session.add(review)
        db.session.commit()
        
        flash('Your review has been submitted!', 'success')
        return redirect(url_for('main.book_detail', book_id=book_id))
    
    return render_template('add_review.html', form=form, book=book, title=f'Review: {book.title}')


@main_bp.route('/cart')
@login_required
def cart():
    """View shopping cart"""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    total = sum(item.subtotal for item in cart_items)
    
    return render_template('cart.html', 
                         cart_items=cart_items, 
                         total=total,
                         title='Shopping Cart')


@main_bp.route('/cart/add/<int:book_id>', methods=['POST'])
@login_required
def add_to_cart(book_id):
    """Add a book to cart"""
    book = Book.query.get_or_404(book_id)
    
    # Check if user has already purchased this book
    already_purchased = OrderItem.query.join(Order).filter(
        Order.user_id == current_user.id,
        OrderItem.book_id == book_id,
        Order.status == 'completed'
    ).first() is not None
    
    if already_purchased:
        flash(f'You have already purchased "{book.title}". You can download it from your profile.', 'warning')
        return redirect(request.referrer or url_for('main.shop'))
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    
    if cart_item:
        flash(f'"{book.title}" is already in your cart.', 'info')
    else:
        cart_item = CartItem(user_id=current_user.id, book_id=book_id)
        db.session.add(cart_item)
        db.session.commit()
        flash(f'"{book.title}" has been added to your cart.', 'success')
    
    return redirect(request.referrer or url_for('main.shop'))


@main_bp.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    """Remove item from cart"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.user_id != current_user.id:
        abort(403)
    
    db.session.delete(cart_item)
    db.session.commit()
    
    flash('Item removed from cart.', 'success')
    return redirect(url_for('main.cart'))


@main_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout process with Stripe payment"""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('main.shop'))
    
    total = sum(item.subtotal for item in cart_items)
    
    form = CheckoutForm()
    
    if request.method == 'GET':
        # Initialize Stripe publishable key for GET request
        stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')
        publishable_key = current_app.config.get('STRIPE_PUBLIC_KEY')
        
        return render_template('checkout.html', 
                             cart_items=cart_items, 
                             total=total, 
                             form=form,
                             publishable_key=publishable_key,
                             title='Checkout')
    
    # Handle JSON request from Stripe payment form (CSRF validated via form token)
    if request.is_json or request.content_type == 'application/json':
        # Manually validate CSRF token from header
        from flask_wtf.csrf import validate_csrf
        try:
            csrf_token = request.headers.get('X-CSRFToken')
            if csrf_token:
                validate_csrf(csrf_token)
        except Exception:
            return jsonify({'error': 'CSRF token validation failed'}), 400
        try:
            stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')
            
            # Prepare cart items data for metadata
            cart_data = json.dumps([{
                'book_id': item.book_id,
                'price': float(item.book.price)
            } for item in cart_items])
            
            # Create Stripe PaymentIntent (don't create order yet)
            intent = stripe.PaymentIntent.create(
                amount=int(total * 100),  # Convert to cents
                currency='usd',
                metadata={
                    'user_id': current_user.id,
                    'user_email': current_user.email,
                    'user_name': current_user.full_name,
                    'cart_data': cart_data,
                    'total_amount': str(total)
                }
            )
            
            # Return response with payment intent client secret
            # Order will be created only after successful payment
            return jsonify({
                'clientSecret': intent.client_secret
            })
            
        except stripe.error.StripeError as e:
            return jsonify({'error': str(e.user_message)}), 400
        except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'}), 400


@main_bp.route('/order/<int:order_id>')
@login_required
def order_confirmation(order_id):
    """Order confirmation page"""
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        abort(403)
    
    return render_template('order_confirmation.html', order=order, title='Order Confirmation')


@main_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    # Paginate orders
    orders_page = request.args.get('orders_page', 1, type=int)
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).paginate(
        page=orders_page, per_page=10, error_out=False
    )
    
    # Paginate reviews
    reviews_page = request.args.get('reviews_page', 1, type=int)
    reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()).paginate(
        page=reviews_page, per_page=10, error_out=False
    )
    
    return render_template('profile.html', 
                         orders=orders, 
                         reviews=reviews,
                         title='My Profile')


@main_bp.route('/download/<int:book_id>')
@login_required
def download_book(book_id):
    """Download a purchased book"""
    book = Book.query.get_or_404(book_id)
    
    # Check if user has purchased this book
    has_purchased = OrderItem.query.join(Order).filter(
        Order.user_id == current_user.id,
        OrderItem.book_id == book_id,
        Order.status == 'completed'
    ).first() is not None
    
    if not has_purchased:
        flash('You can only download books you have purchased.', 'danger')
        abort(403)
    
    # Check if file path exists
    if not book.file_path:
        flash('This book file is not available for download.', 'warning')
        return redirect(url_for('main.profile'))
    
    # Build full file path
    file_full_path = os.path.join(current_app.root_path, 'static', book.file_path)
    
    # Check if file actually exists
    if not os.path.exists(file_full_path):
        flash('Book file not found on server.', 'danger')
        return redirect(url_for('main.profile'))
    
    # Determine the file extension and MIME type
    file_ext = os.path.splitext(book.file_path)[1].lower()
    if file_ext == '.pdf':
        mimetype = 'application/pdf'
    elif file_ext == '.epub':
        mimetype = 'application/epub+zip'
    else:
        mimetype = 'application/octet-stream'
    
    # Create download filename with book title
    download_filename = f"{book.title}{file_ext}"
    
    # Serve the file
    return send_file(
        file_full_path,
        mimetype=mimetype,
        as_attachment=True,
        download_name=download_filename
    )


@main_bp.route('/api/books')
def api_books():
    """API endpoint for books"""
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])


@main_bp.route('/api/hello')
def hello():
    """Test API endpoint"""
    return jsonify({'message': 'Hello from CyberBooks API!'})


@main_bp.route('/admin/book/add', methods=['GET', 'POST'])
@login_required
def add_book():
    """Add a new book to the library"""
    form = BookForm()
    if form.validate_on_submit():
        # Save book cover image
        cover_image = form.cover_image.data
        cover_image_filename = secure_filename(cover_image.filename)
        cover_image_path = os.path.join('app/static/img/books/', cover_image_filename)
        cover_image.save(cover_image_path)

        # Save book file
        book_file = form.book_file.data
        book_file_filename = secure_filename(book_file.filename)
        book_file_path = os.path.join('app/static/books/', book_file_filename)
        book_file.save(book_file_path)

        # Create new book entry
        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            description=form.description.data,
            price=form.price.data,
            cover_image=cover_image_filename,
            book_file=book_file_filename,
            category_id=form.category.data,
            created_at=datetime.utcnow()
        )
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('main.shop'))
    return render_template('admin/add_book.html', form=form, title='Add Book')


@main_bp.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook for payment confirmation"""
    stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')
    webhook_secret = current_app.config.get('STRIPE_WEBHOOK_SECRET')
    
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        if webhook_secret:
            # Verify webhook signature
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        else:
            # If webhook secret not configured, construct event without verification
            event = json.loads(payload)
    except ValueError as e:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        return jsonify({'error': 'Invalid signature'}), 400
    
    # Handle payment_intent.succeeded event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        order_id = payment_intent['metadata'].get('order_id')
        
        if order_id:
            order = Order.query.get(int(order_id))
            if order:
                order.status = 'completed'
                db.session.commit()
                print(f'Order {order.order_number} marked as completed')
    
    # Handle payment_intent.payment_failed event
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        order_id = payment_intent['metadata'].get('order_id')
        
        if order_id:
            order = Order.query.get(int(order_id))
            if order:
                order.status = 'failed'
                db.session.commit()
                print(f'Order {order.order_number} payment failed')
    
    return jsonify({'status': 'success'}), 200


@main_bp.route('/payment-confirmation', methods=['POST'])
@login_required
def payment_confirmation():
    """Handle payment confirmation from Stripe"""
    # Manually validate CSRF token from header for JSON requests
    from flask_wtf.csrf import validate_csrf
    try:
        csrf_token = request.headers.get('X-CSRFToken')
        if csrf_token:
            validate_csrf(csrf_token)
    except Exception:
        return jsonify({'error': 'CSRF token validation failed'}), 400
    
    stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')
    
    data = request.get_json()
    payment_intent_id = data.get('paymentIntentId')
    
    try:
        # Retrieve payment intent from Stripe
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if payment_intent.status == 'succeeded':
            # Payment successful - now create the order
            user_id = int(payment_intent.metadata.get('user_id'))
            
            # Verify user matches
            if user_id != current_user.id:
                return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
            
            # Parse cart data from metadata
            cart_data = json.loads(payment_intent.metadata.get('cart_data', '[]'))
            total_amount = float(payment_intent.metadata.get('total_amount', '0'))
            
            # Create order
            order = Order(
                user_id=current_user.id,
                order_number=Order.generate_order_number(),
                total_amount=total_amount,
                status='completed',
                payment_method='stripe'
            )
            db.session.add(order)
            db.session.flush()  # Get order ID
            
            # Create order items
            for item in cart_data:
                order_item = OrderItem(
                    order_id=order.id,
                    book_id=item['book_id'],
                    price=item['price']
                )
                db.session.add(order_item)
            
            # Clear cart
            CartItem.query.filter_by(user_id=current_user.id).delete()
            
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'orderId': order.id,
                'orderNumber': order.order_number
            })
        
        return jsonify({'status': 'error', 'message': 'Payment not confirmed'}), 400
    
    except stripe.error.StripeError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400
