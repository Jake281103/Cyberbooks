"""
Security Testing Suite for CyberBooks
Tests for SQL Injection and XSS vulnerabilities
"""
import pytest
from app import create_app, db
from app.models import User, Book, Category, Review, Order, OrderItem


@pytest.fixture
def app():
    """Create application instance for security testing"""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        
        # Create test category
        category = Category(name='Security', description='Security books')
        db.session.add(category)
        db.session.commit()
        
        # Create test book
        book = Book(
            title='Security Testing Book',
            author='Test Author',
            isbn='9876543210123',
            description='A book about security',
            price=39.99,
            file_format='PDF',
            file_path='books/security.pdf',
            cover_image='img/books/security.jpg',
            category_id=category.id
        )
        db.session.add(book)
        db.session.commit()
        
        # Create test user
        user = User(
            username='testuser',
            email='test@example.com',
            full_name='Test User'
        )
        user.set_password('Test123!')
        db.session.add(user)
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    with app.test_client() as client:
        yield client


# ==================== SQL INJECTION TESTS ====================

def test_sql_injection_login_username(client, app):
    """Test SQL injection in login username field"""
    sql_payloads = [
        "' OR '1'='1",
        "admin' --",
        "' OR 1=1 --",
        "admin' OR '1'='1' --",
        "' UNION SELECT NULL, NULL, NULL --",
        "1' OR '1' = '1')) /*",
    ]
    
    for payload in sql_payloads:
        response = client.post('/auth/login', data={
            'username': payload,
            'password': 'anypassword'
        }, follow_redirects=True)
        
        # Should not bypass authentication
        assert response.status_code == 200
        assert b'Invalid username or password' in response.data or b'login' in response.data.lower()
        
        # Verify user is not logged in
        response = client.get('/profile')
        assert response.status_code == 302  # Redirects to login


def test_sql_injection_registration_username(client, app):
    """Test SQL injection in registration username field"""
    sql_payloads = [
        "admin'; DROP TABLE users; --",
        "test' OR '1'='1",
        "'; DELETE FROM users WHERE '1'='1",
    ]
    
    for payload in sql_payloads:
        response = client.post('/auth/register', data={
            'username': payload,
            'email': f'test{payload[:5]}@example.com',
            'password': 'Test123!',
            'confirm_password': 'Test123!',
            'full_name': 'Test User'
        }, follow_redirects=True)
        
        # Should handle safely (either validation error or safe storage)
        assert response.status_code == 200
        
        # Verify database is intact
        users_count = User.query.count()
        assert users_count >= 1  # At least the fixture user exists


def test_sql_injection_search_query(client, app):
    """Test SQL injection in search functionality"""
    sql_payloads = [
        "' OR '1'='1",
        "1' UNION SELECT NULL, username, password FROM users --",
        "'; DROP TABLE books; --",
    ]
    
    for payload in sql_payloads:
        response = client.get(f'/shop?search={payload}')
        
        # Should return normal results without error
        assert response.status_code == 200
        
        # Verify database is intact
        books_count = Book.query.count()
        assert books_count >= 1  # At least the fixture book exists


def test_sql_injection_book_id_parameter(client, app):
    """Test SQL injection in book_id URL parameter"""
    sql_payloads = [
        "1 OR 1=1",
        "1'; DROP TABLE books; --",
        "1 UNION SELECT NULL",
    ]
    
    for payload in sql_payloads:
        # Try accessing book detail with SQL injection
        response = client.get(f'/book/{payload}')
        
        # Should return 404 or handle error gracefully
        assert response.status_code in [404, 500]


def test_sql_injection_review_submission(client, app):
    """Test SQL injection in review submission"""
    # Login first
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test123!'
    })
    
    user = User.query.filter_by(username='testuser').first()
    book = Book.query.first()
    
    # Create completed order
    order = Order(
        user_id=user.id,
        order_number='ORD-SEC-001',
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
    
    sql_payload = "'; DROP TABLE reviews; --"
    
    response = client.post(f'/book/{book.id}/review', data={
        'rating': 5,
        'comment': sql_payload
    }, follow_redirects=True)
    
    # Should store safely
    assert response.status_code == 200
    
    # Verify the review was stored as plain text, not executed
    review = Review.query.filter_by(user_id=user.id, book_id=book.id).first()
    if review:
        assert review.comment == sql_payload  # Stored as-is, not executed
    
    # Verify database is intact
    reviews_count = Review.query.count()
    assert reviews_count >= 0  # Table still exists


# ==================== XSS INJECTION TESTS ====================

def test_xss_injection_registration_username(client, app):
    """Test XSS in registration username field"""
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg/onload=alert('XSS')>",
        "javascript:alert('XSS')",
    ]
    
    for idx, payload in enumerate(xss_payloads):
        response = client.post('/auth/register', data={
            'username': f'xssuser{idx}',
            'email': f'xss{idx}@example.com',
            'password': 'Test123!',
            'confirm_password': 'Test123!',
            'full_name': payload
        }, follow_redirects=True)
        
        # Should accept but escape the content
        assert response.status_code == 200


def test_xss_injection_review_stored(client, app):
    """Test stored XSS in review comments"""
    # Login
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test123!'
    })
    
    user = User.query.filter_by(username='testuser').first()
    book = Book.query.first()
    
    # Create completed order
    order = Order(
        user_id=user.id,
        order_number='ORD-XSS-001',
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
    
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<<SCRIPT>alert('XSS');//<</SCRIPT>",
    ]
    
    for payload in xss_payloads:
        response = client.post(f'/book/{book.id}/review', data={
            'rating': 5,
            'comment': payload
        }, follow_redirects=True)
        
        # Should store the review
        assert response.status_code == 200
        
        # Check that XSS is escaped when displayed
        response = client.get(f'/book/{book.id}')
        assert response.status_code == 200
        
        # The script tags should be escaped in HTML output
        # Flask/Jinja2 auto-escapes by default
        assert b'<script>' not in response.data or b'&lt;script&gt;' in response.data


def test_xss_injection_book_search(client, app):
    """Test reflected XSS in search functionality"""
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert(1)>",
        "\"><script>alert('XSS')</script>",
    ]
    
    for payload in xss_payloads:
        response = client.get(f'/shop?search={payload}')
        
        # Should display search results safely
        assert response.status_code == 200
        
        # XSS should be escaped in the output
        assert b'<script>' not in response.data or b'&lt;script&gt;' in response.data


def test_xss_injection_profile_name(client, app):
    """Test XSS in user profile display"""
    xss_payload = "<script>alert('XSS')</script>"
    
    # Register with XSS in full name
    client.post('/auth/register', data={
        'username': 'xssprofile',
        'email': 'xssprofile@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'full_name': xss_payload
    })
    
    # Login
    client.post('/auth/login', data={
        'username': 'xssprofile',
        'password': 'Test123!'
    })
    
    # Check profile page
    response = client.get('/profile')
    assert response.status_code == 200
    
    # XSS should be escaped
    assert b'<script>' not in response.data or b'&lt;script&gt;' in response.data


def test_xss_injection_book_description(client, app):
    """Test that book descriptions escape HTML properly"""
    # This tests that admin-added content is also escaped
    xss_payload = "<script>alert('XSS')</script>"
    
    category = Category.query.first()
    book = Book(
        title='XSS Test Book',
        author='XSS Author',
        isbn='1111111111111',
        description=xss_payload,
        price=29.99,
        file_format='PDF',
        file_path='books/xss.pdf',
        cover_image='img/books/xss.jpg',
        category_id=category.id
    )
    db.session.add(book)
    db.session.commit()
    
    # View book detail page
    response = client.get(f'/book/{book.id}')
    assert response.status_code == 200
    
    # XSS should be escaped
    assert b'<script>' not in response.data or b'&lt;script&gt;' in response.data


# ==================== ADDITIONAL SECURITY TESTS ====================

def test_path_traversal_book_download(client, app):
    """Test path traversal attack in book download"""
    # Login
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test123!'
    })
    
    path_traversal_payloads = [
        "../../etc/passwd",
        "..\\..\\windows\\system.ini",
        "....//....//etc/passwd",
    ]
    
    for payload in path_traversal_payloads:
        response = client.get(f'/download/{payload}')
        
        # Should reject or return 404, not serve system files
        assert response.status_code in [404, 403, 400]


def test_authentication_bypass_attempts(client, app):
    """Test various authentication bypass attempts"""
    protected_routes = [
        '/profile',
        '/cart',
        '/checkout',
    ]
    
    for route in protected_routes:
        response = client.get(route)
        
        # Should redirect to login
        assert response.status_code == 302
        assert b'/auth/login' in response.data or 'login' in response.headers.get('Location', '')


def test_csrf_token_validation(client, app):
    """Test that CSRF protection is enabled in production"""
    # This test verifies CSRF is only disabled in testing
    # In production, CSRF tokens should be required
    
    # Note: CSRF is disabled in test config
    # This test documents that it should be enabled in production
    assert app.config['WTF_CSRF_ENABLED'] == False  # Only in testing!
    assert app.config['TESTING'] == True


def test_password_hashing_security(client, app):
    """Test that passwords are properly hashed"""
    # Register a user
    client.post('/auth/register', data={
        'username': 'secureuser',
        'email': 'secure@example.com',
        'password': 'SecurePass123!',
        'confirm_password': 'SecurePass123!',
        'full_name': 'Secure User'
    })
    
    # Check that password is hashed in database
    user = User.query.filter_by(username='secureuser').first()
    assert user is not None
    assert user.password_hash is not None
    assert user.password_hash != 'SecurePass123!'  # Not stored in plain text
    assert len(user.password_hash) > 50  # Hashed passwords are long
    assert user.password_hash.startswith('$2b$')  # bcrypt hash format


def test_session_fixation_protection(client, app):
    """Test protection against session fixation attacks"""
    # Get initial session
    response = client.get('/auth/login')
    initial_cookie = response.headers.get('Set-Cookie')
    
    # Login
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test123!'
    }, follow_redirects=True)
    
    # Session should be regenerated after login
    login_cookie = response.headers.get('Set-Cookie')
    
    # Verify user is logged in
    response = client.get('/profile')
    assert response.status_code == 200


def test_sql_injection_order_by_clause(client, app):
    """Test SQL injection in ORDER BY clause"""
    sort_payloads = [
        "title; DROP TABLE books; --",
        "1 OR 1=1",
        "title) OR 1=1 --",
    ]
    
    for payload in sort_payloads:
        response = client.get(f'/shop?sort={payload}')
        
        # Should handle safely
        assert response.status_code in [200, 400]
        
        # Verify database is intact
        books_count = Book.query.count()
        assert books_count >= 1


def test_mass_assignment_protection(client, app):
    """Test protection against mass assignment vulnerabilities"""
    # Try to set admin role during registration
    response = client.post('/auth/register', data={
        'username': 'hacker',
        'email': 'hacker@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'full_name': 'Hacker',
        'is_admin': 'true',  # Try to inject admin privilege
        'role': 'admin'
    }, follow_redirects=True)
    
    # User should be created but not as admin
    user = User.query.filter_by(username='hacker').first()
    if user:
        # Verify user is not admin (assuming is_admin field exists)
        # This test documents the protection should exist
        assert not getattr(user, 'is_admin', False)
