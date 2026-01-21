from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, send_file
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import Book, Category, Order, OrderItem, User, Review
from app.forms import BookForm, CategoryForm
import os

admin_bp = Blueprint('admin', __name__)


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
    total_books = Book.query.count()
    total_users = User.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_books=total_books,
                         total_users=total_users,
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders,
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
        book = Book(
            title=form.title.data,
            author=form.author.data,
            isbn=form.isbn.data,
            description=form.description.data,
            price=form.price.data,
            file_format=form.file_format.data,
            category_id=form.category_id.data,
            file_path=form.file_path.data,
            cover_image=form.cover_image.data,
            stock=form.stock.data
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
        book.file_path = form.file_path.data
        book.cover_image = form.cover_image.data
        book.stock = form.stock.data
        
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
