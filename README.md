# CyberBooks - Cybersecurity E-Commerce Platform

A comprehensive Flask-based e-commerce platform for cybersecurity educational resources with secure user authentication, shopping cart, checkout, and administrative management. **Fully responsive design optimized for mobile phones, tablets, and desktop computers.**

## Features

### ✅ Functional Requirements Implemented

1. **User Registration and Authentication**
   - Secure registration with bcrypt password hashing
   - Login with session management
   - CSRF protection on all forms
   - Session security with HTTPOnly and Secure cookies
   - Protection against automated attacks
   - 26 functional tests covering all auth flows

2. **Product Management**
   - Full CRUD operations for books (Admin only)
   - Categories: Network Security, Cryptography, Ethical Hacking, Digital Forensics, etc.
   - Book attributes: title, author, ISBN, price, description, file format (PDF/ePub)
   - Stock management
   - Book reviews and ratings

3. **Search and Filtering**
   - Keyword search (title and author)
   - Filter by category
   - Filter by price range
   - Sort by newest, oldest, price, and rating

4. **Shopping Cart and Checkout**
   - Add/remove items from cart (no quantity tracking for digital products)
   - Stripe payment processing in test mode
   - Order confirmation with payment verification
   - Order history and status tracking
   - PaymentIntent workflow with webhooks

5. **Download and Access Control**
   - Purchase verification before download access
   - Only authenticated buyers can download
   - Instant access after purchase
   - Actual file serving with send_file()

6. **Review and Rating System**
   - 5-star rating system
   - Written reviews with validation
   - Only purchasers can review
   - One review per user per book
   - XSS protection on review content

7. **Database Management**
   - MySQL with SQLAlchemy ORM
   - Normalized relational structure
   - Foreign key constraints
   - Data integrity and validation
   - Modern SQLAlchemy 2.0 syntax

8. **Responsive Design** ⭐
   - Mobile-first approach with 5 breakpoint system
   - Hamburger navigation menu for mobile devices
   - Touch-optimized UI elements (min 44-48px targets)
   - Adaptive layouts for phones, tablets, and desktops
   - Progressive enhancement for modern browsers

9. **Comprehensive Testing** ⭐ NEW
   - 26 Functional Tests (Registration, Login, Cart, Reviews, Error Pages)
   - 17 Security Tests (SQL Injection, XSS, CSRF, Path Traversal, etc.)
   - 100% test pass rate with 0 warnings
   - Coverage reports with pytest-cov

10. **Security Testing** ⭐ NEW
    - SQL Injection prevention tests
    - XSS (Cross-Site Scripting) prevention tests
    - CSRF token validation tests
    - Path traversal attack prevention
    - Authentication bypass prevention
    - Password hashing verification
    - Session fixation protection
    - Mass assignment protection

## Project Structure

```
CyberBooks/
├── app/
│   ├── __init__.py              # Application factory with security config
│   ├── models.py                # Database models (User, Book, Category, Order, Review, Cart)
│   ├── forms.py                 # WTForms with validation
│   ├── routes.py                # Main routes (shop, cart, checkout, profile)
│   ├── auth.py                  # Authentication routes (login, register, logout)
│   ├── admin.py                 # Admin routes (manage books, categories, users, orders)
│   ├── templates/
│   │   ├── base.html            # Base template with navigation
│   │   ├── index.html           # Home page
│   │   ├── shop.html            # Shop with search and filters
│   │   ├── book_detail.html     # Book details and reviews
│   │   ├── cart.html            # Shopping cart
│   │   ├── checkout.html        # Checkout process
│   │   ├── profile.html         # User profile and orders
│   │   ├── order_confirmation.html
│   │   ├── add_review.html      # Review submission
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── admin/
│   │       ├── dashboard.html   # Admin dashboard with stats
│   │       ├── books.html       # Manage books
│   │       ├── book_form.html   # Add/edit book
│   │       ├── categories.html  # Manage categories
│   │       ├── category_form.html
│   │       ├── users.html       # View users
│   │       └── orders.html      # View all orders
│   └── static/
│       ├── css/
│       │   └── style.css        # Comprehensive styling
│       └── js/
│           └── main.js          # JavaScript functionality
├── config.py                    # Environment-based configuration with TestingConfig
├── pytest.ini                   # Pytest configuration with warning filters
├── requirements.txt             # Python dependencies with versions
├── manage.py                    # Interactive management menu with testing commands
├── run.py                       # Application entry point
├── init_db.py                   # Database initialization script
├── create_admin.py              # Admin user creation script
├── verify_setup.py              # Setup verification script
├── tests/
│   ├── __init__.py
│   ├── test_app.py              # 26 Functional tests (auth, cart, reviews, errors)
│   ├── test_security.py         # 17 Security tests (SQL injection, XSS, etc.)
│   └── README.md                # Testing guide
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore patterns
├── SETUP_GUIDE.md               # Detailed setup guide
├── TESTING_SUMMARY.md           # Testing documentation
└── README.md                    # This file
```

## Technology Stack

- **Backend**: Flask 3.0.3, Werkzeug 3.1.5
- **Database**: MySQL with PyMySQL driver, SQLAlchemy 2.0.45 ORM
- **Migration**: Flask-Migrate 4.0.7
- **Authentication**: Flask-Login 0.6.3 with session management
- **Forms**: Flask-WTF 1.2.1, WTForms 3.1.2 with CSRF protection
- **Security**: bcrypt 4.1.3 (password hashing), Flask-Talisman 1.1.0 (security headers)
- **Payment**: Stripe 14.2.0 (test mode)
- **Testing**: pytest 9.0.2, pytest-flask 1.3.0, pytest-cov 7.0.0, coverage 7.13.2
- **Utilities**: python-dotenv 1.0.1, email-validator 2.1.0

## Setup Instructions

### Prerequisites

- Python 3.11+
- MySQL Server (5.7+ or 8.0+)
- pip package manager

### 1. Database Setup

Create a MySQL database:

```sql
CREATE DATABASE cyberbooks CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Clone and Setup

```bash
# Navigate to project directory
cd CyberBooks

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy environment template
copy .env.example .env

# Edit .env file with your configuration
# - Set a strong SECRET_KEY
# - Update DATABASE_URL with your MySQL credentials
```

Example `.env`:
```
SECRET_KEY=your-very-secure-random-secret-key-here
DATABASE_URL=mysql+pymysql://root:your_password@localhost/cyberbooks
FLASK_ENV=development
FLASK_APP=run.py
```

### 4. Initialize Database

```bash
# Run initialization script
python init_db.py
```

This will:
- Create all database tables
- Add sample categories (Network Security, Cryptography, Ethical Hacking, etc.)
- Create admin user (username: `admin`, password: `admin123`)
- Add sample books

### 5. Run Database Migrations (Optional)

If you need to modify the database schema:

```bash
# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### 6. Run the Application

```bash
# Start the development server
python run.py
```

The application will be available at `http://localhost:5000`

## Default Credentials

**Admin Account:**
- Username: `admin123`
- Password: `Admin@12345`

⚠️ **Important**: Change the admin password immediately in production!

## Usage Guide

### For Customers

1. **Register an Account**
   - Navigate to Register page
   - Fill in username, email, full name, and password
   - Passwords are hashed with bcrypt before storage

2. **Browse Books**
   - Visit the Shop page
   - Use search and filters to find books
   - Filter by category, price range
   - Sort by various criteria

3. **Purchase Books**
   - Add books to cart
   - Review cart and update quantities
   - Proceed to checkout
   - Complete simulated payment

4. **Access Purchased Books**
   - View order confirmation
   - Download purchased books
   - Write reviews and ratings

### For Administrators

1. **Access Admin Panel**
   - Login with admin credentials
   - Click "Admin" in navigation

2. **Manage Books**
   - Add new books with details
   - Edit existing books
   - Delete books
   - View all books

3. **Manage Categories**
   - Create new categories
   - Edit category details
   - Delete empty categories

4. **Monitor System**
   - View dashboard statistics
   - Monitor all orders
   - View user list

## Security Features

### Authentication & Password Security
- Bcrypt hashing with automatic salt generation
- Minimum 8-character password requirement
- Password confirmation validation
- Secure session management with Flask-Login
- Login required decorators on protected routes

### CSRF & XSS Protection
- Flask-WTF CSRF tokens on all forms
- Automatic token validation
- Jinja2 auto-escaping prevents XSS attacks
- Stored XSS tests verify HTML escaping
- Reflected XSS tests verify input sanitization

### Session Security
- Secure session cookies (production)
- HTTPOnly cookies to prevent XSS token theft
- SameSite cookies for CSRF protection (production)
- 2-hour session timeout
- Session fixation attack prevention

### SQL Injection Prevention
- SQLAlchemy ORM parameterized queries
- Input validation with WTForms
- 6 SQL injection tests verify protection
- No direct SQL query execution

### Access Control
- Role-based access (admin/user)
- Purchase verification for downloads
- One-time book purchase (no re-buying)
- One review per user per book enforcement

### Security Headers (Production)
- Flask-Talisman for security headers
- HTTPS enforcement (DEBUG=False)
- Content Security Policy
- X-Frame-Options to prevent clickjacking
- X-Content-Type-Options to prevent MIME sniffing

### Path Traversal Protection
- File download validation
- No directory traversal allowed
- Verified with path traversal tests

### Testing & Validation
- 43 total tests (26 functional + 17 security)
- SQL injection tests pass ✅
- XSS prevention tests pass ✅
- CSRF validation tests pass ✅
- Authentication bypass tests pass ✅
- Path traversal tests pass ✅

## API Endpoints

- `GET /api/books` - List all books (JSON)
- `GET /api/hello` - Test endpoint

## Database Schema

### Users
- id, username, email, password_hash, full_name, is_admin, created_at, last_login

### Categories
- id, name, description

### Books
- id, title, author, isbn, description, price, file_format, file_path, cover_image, category_id, stock, created_at, updated_at

### Orders
- id, user_id, order_number, total_amount, status, payment_method, created_at

### OrderItems
- id, order_id, book_id, quantity, price

### Reviews
- id, user_id, book_id, rating, comment, created_at

### CartItems
- id, user_id, book_id, quantity, added_at

## Development

### Running Tests

```bash
# Run functional tests
python -m pytest tests/test_app.py -v

# Run security tests (SQL Injection, XSS, etc.)
python -m pytest tests/test_security.py -v

# Run all tests with coverage report
python -m pytest tests/ -v --cov=app --cov-report=html --cov-report=term
```

**Test Coverage:**
- **26 Functional Tests**: Registration, Login, Cart, Reviews, Error Pages, Shop
- **17 Security Tests**: SQL Injection, XSS, Path Traversal, Authentication Bypass, etc.
- All tests pass with 0 warnings ✅

View coverage report:
```bash
# After running tests with coverage
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac
```

### Using the Management Menu

```bash
# Interactive management menu
python manage.py
```

Menu options:
1. Setup Environment
2. Verify Setup
3. Initialize Database
4. Create Admin User
5. Run Development Server
6. Create Database Migration
7. Apply Database Migration
8. View Database Info
9. Run Functional Tests
10. Run Security Tests
11. Run All Tests with Coverage
12. Clean Test Cache
13. Exit

### Database Migrations

```bash
# After model changes
flask db migrate -m "Description of changes"
flask db upgrade
```


### Database Connection Issues
- Verify MySQL is running
- Check DATABASE_URL in .env
- Ensure database exists
- Verify user permissions

### Import Errors
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

### Migration Issues
- Delete migrations folder and reinitialize
- Drop and recreate database if necessary

