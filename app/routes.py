from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_file, abort
from flask_login import login_required, current_user
from sqlalchemy import or_
from app import db
from app.models import Book, Category, CartItem, Order, OrderItem, Review
from app.forms import ReviewForm, CheckoutForm, SearchForm
from datetime import datetime
import os

main_bp = Blueprint('main', __name__)


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
    if category_id:
        query = query.filter(Book.category_id == category_id)
    
    # Filter by price range
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    if min_price is not None:
        query = query.filter(Book.price >= min_price)
    if max_price is not None:
        query = query.filter(Book.price <= max_price)
    
    # Sorting
    sort_by = request.args.get('sort_by', 'newest')
    if sort_by == 'oldest':
        query = query.order_by(Book.created_at.asc())
    elif sort_by == 'price_low':
        query = query.order_by(Book.price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(Book.price.desc())
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
    reviews = Review.query.filter_by(book_id=book_id).order_by(Review.created_at.desc()).all()
    
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
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    
    if cart_item:
        cart_item.quantity += 1
        flash(f'Increased quantity of "{book.title}" in your cart.', 'info')
    else:
        cart_item = CartItem(user_id=current_user.id, book_id=book_id, quantity=1)
        db.session.add(cart_item)
        flash(f'"{book.title}" has been added to your cart.', 'success')
    
    db.session.commit()
    
    return redirect(request.referrer or url_for('main.shop'))


@main_bp.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    """Update cart item quantity"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.user_id != current_user.id:
        abort(403)
    
    quantity = request.form.get('quantity', type=int)
    
    if quantity and quantity > 0:
        cart_item.quantity = quantity
        db.session.commit()
        flash('Cart updated.', 'success')
    else:
        flash('Invalid quantity.', 'danger')
    
    return redirect(url_for('main.cart'))


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
    """Checkout process"""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('main.shop'))
    
    total = sum(item.subtotal for item in cart_items)
    
    form = CheckoutForm()
    
    if form.validate_on_submit():
        # Create order
        order = Order(
            user_id=current_user.id,
            order_number=Order.generate_order_number(),
            total_amount=total,
            status='completed',
            payment_method=form.payment_method.data
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                book_id=cart_item.book_id,
                quantity=cart_item.quantity,
                price=cart_item.book.price
            )
            db.session.add(order_item)
        
        # Clear cart
        for cart_item in cart_items:
            db.session.delete(cart_item)
        
        db.session.commit()
        
        flash(f'Order {order.order_number} completed successfully!', 'success')
        return redirect(url_for('main.order_confirmation', order_id=order.id))
    
    return render_template('checkout.html', 
                         cart_items=cart_items, 
                         total=total, 
                         form=form,
                         title='Checkout')


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
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()).all()
    
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
    
    # In a real application, serve the actual file
    # For demo purposes, we'll just show a message
    flash(f'Downloading "{book.title}" ({book.file_format})...', 'info')
    return redirect(url_for('main.profile'))


@main_bp.route('/api/books')
def api_books():
    """API endpoint for books"""
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])


@main_bp.route('/api/hello')
def hello():
    """Test API endpoint"""
    return jsonify({'message': 'Hello from CyberBooks API!'})
