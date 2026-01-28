from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, send_file, current_app
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import Book, Category, Order, OrderItem, User, Review
from app.forms import BookForm, CategoryForm
from werkzeug.utils import secure_filename
import os
import uuid

admin_bp = Blueprint('admin', __name__)


def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_file(file, folder):
    """Save uploaded file and return the relative path"""
    if file and file.filename:
        # Generate unique filename to prevent conflicts
        original_filename = secure_filename(file.filename)
        filename = f"{uuid.uuid4().hex}_{original_filename}"
        
        # Create folder if it doesn't exist
        upload_path = os.path.join(current_app.root_path, 'static', folder)
        os.makedirs(upload_path, exist_ok=True)
        
        # Save file
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        
        # Return relative path for database storage
        return f"{folder}/{filename}"
    return None


def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with statistics"""
    from sqlalchemy import func, extract
    from datetime import timedelta
    
    total_books = Book.query.count()
    total_users = User.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    # Books by category
    books_by_category = db.session.query(
        Category.name, 
        func.count(Book.id).label('count')
    ).join(Book, Book.category_id == Category.id).group_by(Category.name).all()
    
    # Revenue by month (last 6 months)
    revenue_by_month = db.session.query(
        func.date_format(Order.created_at, '%Y-%m').label('month'),
        func.sum(Order.total_amount).label('revenue')
    ).filter(Order.status == 'completed').group_by('month').order_by('month').limit(6).all()
    
    # Top selling books
    top_books = db.session.query(
        Book.title,
        func.count(OrderItem.id).label('sales')
    ).join(OrderItem, OrderItem.book_id == Book.id).group_by(Book.id, Book.title).order_by(func.count(OrderItem.id).desc()).limit(5).all()
    
    # User registrations by month (last 6 months)
    user_registrations = db.session.query(
        func.date_format(User.created_at, '%Y-%m').label('month'),
        func.count(User.id).label('count')
    ).group_by('month').order_by('month').limit(6).all()
    
    return render_template('admin/dashboard.html',
                         total_books=total_books,
                         total_users=total_users,
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders,
                         books_by_category=books_by_category,
                         revenue_by_month=revenue_by_month,
                         top_books=top_books,
                         user_registrations=user_registrations,
                         title='Admin Dashboard')


@admin_bp.route('/books')
@login_required
@admin_required
def books():
    """List all books for management"""
    page = request.args.get('page', 1, type=int)
    books = Book.query.order_by(Book.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/books.html', books=books, title='Manage Books')


@admin_bp.route('/books/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_book():
    """Add a new book"""
    form = BookForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    
    if form.validate_on_submit():
        # Validate that files are provided for new book
        if not form.cover_image.data or not form.cover_image.data.filename:
            flash('Cover image is required when adding a new book.', 'danger')
            return render_template('admin/book_form.html', form=form, title='Add Book', action='Add')
        
        if not form.book_file.data or not form.book_file.data.filename:
            flash('Book file is required when adding a new book.', 'danger')
            return render_template('admin/book_form.html', form=form, title='Add Book', action='Add')
        
        # Save cover image
        cover_image_path = save_file(form.cover_image.data, 'img/books')
        
        # Save book file
        book_file_path = save_file(form.book_file.data, 'books')
        
        book = Book(
            title=form.title.data,
            author=form.author.data,
            isbn=form.isbn.data,
            description=form.description.data,
            price=form.price.data,
            file_format=form.file_format.data,
            category_id=form.category_id.data,
            file_path=book_file_path,
            cover_image=cover_image_path
        )
        
        db.session.add(book)
        db.session.commit()
        
        flash(f'Book "{book.title}" has been added successfully!', 'success')
        return redirect(url_for('admin.books'))
    
    return render_template('admin/book_form.html', form=form, title='Add Book', action='Add')


@admin_bp.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_book(book_id):
    """Edit an existing book"""
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.isbn = form.isbn.data
        book.description = form.description.data
        book.price = form.price.data
        book.file_format = form.file_format.data
        book.category_id = form.category_id.data
        
        # Update cover image if new file is uploaded
        if form.cover_image.data and hasattr(form.cover_image.data, 'filename') and form.cover_image.data.filename:
            # Delete old file if it exists
            if book.cover_image:
                old_file = os.path.join(current_app.root_path, 'static', book.cover_image)
                if os.path.exists(old_file):
                    os.remove(old_file)
            
            book.cover_image = save_file(form.cover_image.data, 'img/books')
        
        # Update book file if new file is uploaded
        if form.book_file.data and hasattr(form.book_file.data, 'filename') and form.book_file.data.filename:
            # Delete old file if it exists
            if book.file_path:
                old_file = os.path.join(current_app.root_path, 'static', book.file_path)
                if os.path.exists(old_file):
                    os.remove(old_file)
            
            book.file_path = save_file(form.book_file.data, 'books')
        
        db.session.commit()
        
        flash(f'Book "{book.title}" has been updated successfully!', 'success')
        return redirect(url_for('admin.books'))
    
    return render_template('admin/book_form.html', form=form, book=book, title='Edit Book', action='Edit')


@admin_bp.route('/books/delete/<int:book_id>', methods=['POST'])
@login_required
@admin_required
def delete_book(book_id):
    """Delete a book"""
    book = Book.query.get_or_404(book_id)
    title = book.title
    
    # Delete associated files
    if book.cover_image:
        cover_file = os.path.join(current_app.root_path, 'static', book.cover_image)
        if os.path.exists(cover_file):
            os.remove(cover_file)
    
    if book.file_path:
        book_file = os.path.join(current_app.root_path, 'static', book.file_path)
        if os.path.exists(book_file):
            os.remove(book_file)
    
    db.session.delete(book)
    db.session.commit()
    
    flash(f'Book "{title}" has been deleted.', 'success')
    return redirect(url_for('admin.books'))


@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    """List all categories"""
    categories = Category.query.order_by(Category.name).all()
    return render_template('admin/categories.html', categories=categories, title='Manage Categories')


@admin_bp.route('/categories/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_category():
    """Add a new category"""
    form = CategoryForm()
    
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash(f'Category "{category.name}" has been added successfully!', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/category_form.html', form=form, title='Add Category', action='Add')


@admin_bp.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(category_id):
    """Edit an existing category"""
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        
        db.session.commit()
        
        flash(f'Category "{category.name}" has been updated successfully!', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/category_form.html', form=form, category=category, title='Edit Category', action='Edit')


@admin_bp.route('/categories/delete/<int:category_id>', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    """Delete a category"""
    category = Category.query.get_or_404(category_id)
    
    if category.books.count() > 0:
        flash(f'Cannot delete category "{category.name}" because it contains books.', 'danger')
        return redirect(url_for('admin.categories'))
    
    name = category.name
    db.session.delete(category)
    db.session.commit()
    
    flash(f'Category "{name}" has been deleted.', 'success')
    return redirect(url_for('admin.categories'))


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """List all users"""
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/users.html', users=users, title='Manage Users')


@admin_bp.route('/orders')
@login_required
@admin_required
def orders():
    """List all orders"""
    page = request.args.get('page', 1, type=int)
    orders = Order.query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/orders.html', orders=orders, title='Manage Orders')
