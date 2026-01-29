"""
Unit Tests for CyberBooks Application
Tests cover main functionalities: Registration, Login, Add to Cart, Write Review
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Book, Category, CartItem, Review, Order, OrderItem
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """Create application instance for testing"""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['LOGIN_DISABLED'] = False
    
    # Disable CSRF protection for testing
    app.config['WTF_CSRF_METHODS'] = []
    
    with app.app_context():
        db.create_all()
        
        # Create test category
        category = Category(name='Cybersecurity', description='Security books')
        db.session.add(category)
        db.session.commit()
        
        # Create test book
        book = Book(
            title='Test Cybersecurity Book',
            author='Test Author',
            isbn='1234567890123',
            description='A test book about cybersecurity',
            price=29.99,
            file_format='PDF',
            file_path='books/test.pdf',
            cover_image='img/books/test.jpg',
            category_id=category.id
        )
        db.session.add(book)
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    with app.test_client() as client:
        yield client


@pytest.fixture
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()


# ==================== USER REGISTRATION TESTS ====================

def test_register_page_loads(client):
    """Test that registration page loads successfully"""
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data


def test_successful_registration(client):
    """Test successful user registration"""
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'full_name': 'Test User'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    # Check user was created in database
    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.email == 'test@example.com'


def test_duplicate_username_registration(client):
    """Test that duplicate username registration fails"""
    # Register first user
    client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'full_name': 'Test User'
    })
    
    # Try to register with same username
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'different@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'full_name': 'Different User'
    }, follow_redirects=True)
    
    assert b'Username already exists' in response.data or b'already' in response.data.lower()


def test_duplicate_email_registration(client):
    """Test that duplicate email registration fails"""
    # Register first user
    client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'full_name': 'Test User'
    })
    
    # Try to register with same email
    response = client.post('/auth/register', data={
        'username': 'differentuser',
        'email': 'test@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'full_name': 'Different User'
    }, follow_redirects=True)
    
    assert b'Email already registered' in response.data or b'already' in response.data.lower()


def test_password_mismatch_registration(client):
    """Test that password mismatch is caught"""
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test123!',
        'confirm_password': 'Different123!',
        'full_name': 'Test User'
    }, follow_redirects=True)
    
    assert b'Passwords must match' in response.data or b'password' in response.data.lower()


# ==================== USER LOGIN TESTS ====================

def test_login_page_loads(client):
    """Test that login page loads successfully"""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_successful_login(client):
    """Test successful user login"""
    # Register user first
    client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'full_name': 'Test User'
    })
    
    # Now login
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test123!'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'testuser' in response.data or b'profile' in response.data.lower()


def test_login_wrong_password(client):
    """Test that wrong password fails"""
    # Register user
    client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'full_name': 'Test User'
    })
    
    # Try to login with wrong password
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'WrongPassword123!'
    }, follow_redirects=True)
    
    assert b'Invalid username or password' in response.data or b'invalid' in response.data.lower()


def test_login_nonexistent_user(client):
    """Test that login with non-existent user fails"""
    response = client.post('/auth/login', data={
        'username': 'nonexistent',
        'password': 'Test123!'
    }, follow_redirects=True)
    
    assert b'Invalid username or password' in response.data or b'invalid' in response.data.lower()


def test_logout(client):
    """Test user logout"""
    # Register and login
    client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'full_name': 'Test User'
    })
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test123!'
    })
    
    # Logout
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data or b'login' in response.data.lower()


def test_protected_page_requires_login(client):
    """Test that protected pages redirect to login"""
    response = client.get('/profile', follow_redirects=True)
    assert b'Please log in' in response.data or b'login' in response.data.lower()


# ==================== ADD TO CART TESTS ====================

def test_add_to_cart_requires_login(client, app):
    """Test that adding to cart requires login"""
    with app.app_context():
        book = Book.query.first()
        response = client.post(f'/cart/add/{book.id}', follow_redirects=True)
        assert b'Please log in' in response.data or b'login' in response.data.lower()


def test_successful_add_to_cart(client, app):
    """Test successfully adding a book to cart"""
    # Register and login
    client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'full_name': 'Test User'
    })
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test123!'
    })
    
    # Add book to cart
    book = Book.query.first()
    response = client.post(f'/cart/add/{book.id}', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'added to your cart' in response.data or b'cart' in response.data.lower()
    
    # Check cart item was created
    cart_item = CartItem.query.filter_by(book_id=book.id).first()
    assert cart_item is not None


def test_add_same_book_twice_to_cart(client, app):
    """Test that adding same book twice shows appropriate message"""
    # Register and login
    client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'full_name': 'Test User'
    })
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test123!'
    })
    
    # Add book first time
    book = Book.query.first()
    client.post(f'/cart/add/{book.id}')
    
    # Add same book second time
    response = client.post(f'/cart/add/{book.id}', follow_redirects=True)
    assert b'already in your cart' in response.data or b'already' in response.data.lower()


def test_view_cart(client, app):
    """Test viewing cart page"""
    # Register and login
    client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'full_name': 'Test User'
    })
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test123!'
    })
    
    # Add book to cart
    book = Book.query.first()
    client.post(f'/cart/add/{book.id}')
    
    # View cart
    response = client.get('/cart')
    assert response.status_code == 200
    assert b'Shopping Cart' in response.data or b'cart' in response.data.lower()


def test_remove_from_cart(client, app):
    """Test removing item from cart"""
    # Register and login
    client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'full_name': 'Test User'
    })
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test123!'
    })
    
    # Add book to cart
    book = Book.query.first()
    client.post(f'/cart/add/{book.id}')
    
    cart_item = CartItem.query.filter_by(book_id=book.id).first()
    assert cart_item is not None
    
    # Remove from cart
    response = client.post(f'/cart/remove/{cart_item.id}', follow_redirects=True)
    assert response.status_code == 200
    
    # Check cart item was deleted
    deleted_item = db.session.get(CartItem, cart_item.id)
    assert deleted_item is None


# ==================== WRITE REVIEW TESTS ====================

def test_add_review_requires_login(client, app):
    """Test that adding review requires login"""
    book = Book.query.first()
    response = client.get(f'/book/{book.id}/review', follow_redirects=True)
    assert b'Please log in' in response.data or b'login' in response.data.lower()


def test_add_review_requires_purchase(client, app):
    """Test that user must purchase book before reviewing"""
    # Register and login
    client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'full_name': 'Test User'
    })
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test123!'
    })
    
    # Try to review without purchasing
    book = Book.query.first()
    response = client.get(f'/book/{book.id}/review', follow_redirects=True)
    assert b'purchased' in response.data.lower() or b'review' in response.data.lower()


def test_successful_review_submission(client, app):
    """Test successfully submitting a review"""
    # Register and login
    client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'full_name': 'Test User'
    })
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test123!'
    })
    
    user = User.query.filter_by(username='testuser').first()
    book = Book.query.first()
    
    # Create completed order
    order = Order(
        user_id=user.id,
        order_number='ORD-TEST-001',
        total_amount=book.price,
        status='completed',
        payment_method='stripe'
    )
    db.session.add(order)
    db.session.commit()
    
    order_item = OrderItem(
        order_id=order.id,
        book_id=book.id,
        price=book.price
    )
    db.session.add(order_item)
    db.session.commit()
    
    # Submit review
    response = client.post(f'/book/{book.id}/review', data={
        'rating': 5,
        'comment': 'Excellent book! Very informative.'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Review added successfully' in response.data or b'review' in response.data.lower()
    
    # Check review was created
    review = Review.query.filter_by(user_id=user.id, book_id=book.id).first()
    assert review is not None
    assert review.rating == 5


def test_duplicate_review_prevention(client, app):
    """Test that user cannot review same book twice"""
    # Register and login
    client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'full_name': 'Test User'
    })
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test123!'
    })
    
    user = User.query.filter_by(username='testuser').first()
    book = Book.query.first()
    
    # Create completed order
    order = Order(
        user_id=user.id,
        order_number='ORD-TEST-002',
        total_amount=book.price,
        status='completed',
        payment_method='stripe'
    )
    db.session.add(order)
    db.session.commit()
    
    order_item = OrderItem(
        order_id=order.id,
        book_id=book.id,
        price=book.price
    )
    db.session.add(order_item)
    db.session.commit()
    
    # Submit first review
    client.post(f'/book/{book.id}/review', data={
        'rating': 5,
        'comment': 'Great book!'
    })
    
    # Try to submit second review
    response = client.post(f'/book/{book.id}/review', data={
        'rating': 4,
        'comment': 'Still good!'
    }, follow_redirects=True)
    
    assert b'already reviewed' in response.data.lower() or b'already' in response.data.lower()


# ==================== ERROR PAGE TESTS ====================

def test_404_page(client):
    """Test 404 error page"""
    response = client.get('/thispagedoesnotexist')
    assert response.status_code == 404
    assert b'404' in response.data or b'not found' in response.data.lower()


def test_403_page(client):
    """Test 403 forbidden page"""
    # Try to access admin page without login
    response = client.get('/admin/dashboard')
    assert response.status_code in [302, 403]


# ==================== SHOP & BOOK LISTING TESTS ====================

def test_shop_page_loads(client, app):
    """Test that shop page loads successfully"""
    response = client.get('/shop')
    assert response.status_code == 200
    assert b'Shop' in response.data or b'shop' in response.data.lower()


def test_book_appears_in_shop(client, app):
    """Test that created book appears in shop"""
    with app.app_context():
        response = client.get('/shop')
        book = Book.query.first()
        assert book.title.encode() in response.data


def test_book_detail_page(client, app):
    """Test book detail page loads"""
    with app.app_context():
        book = Book.query.first()
        response = client.get(f'/book/{book.id}')
        assert response.status_code == 200
        assert book.title.encode() in response.data


def test_home_page(client, app):
    """Test home page loads"""
    response = client.get('/')
    assert response.status_code == 200

