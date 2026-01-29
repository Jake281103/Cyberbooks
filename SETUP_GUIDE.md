# CyberBooks - Quick Setup Guide

## Step-by-Step Installation

### Step 1: Install MySQL

1. Download MySQL from https://dev.mysql.com/downloads/mysql/
2. Install and set root password
3. Start MySQL service

### Step 2: Create Database

Open MySQL command line and run:
```sql
CREATE DATABASE cyberbooks CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Step 3: Setup Python Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment

The `.env` file is already created. Update it if needed:
```
DATABASE_URL=mysql+pymysql://root:YOUR_MYSQL_PASSWORD@localhost/cyberbooks
```

### Step 5: Verify Setup

```powershell
python verify_setup.py
```

This will check:
- Python version
- Required packages
- Environment file
- Database connection

### Step 6: Initialize Database

```powershell
python init_db.py
```

This creates:
- All database tables
- Sample categories (Network Security, Cryptography, etc.)
- Admin user (username: admin, password: admin123)
- Sample books

### Step 7: Run Application

```powershell
python run.py
```

Visit: http://localhost:5000

### Step 8 (Optional): Run Tests

```powershell
# Run functional tests (26 tests)
python -m pytest tests/test_app.py -v

# Run security tests (17 tests)
python -m pytest tests/test_security.py -v

# Run all tests with coverage
python -m pytest tests/ -v --cov=app --cov-report=html
```

All tests should pass ✅
Coverage report available in `htmlcov/index.html`

## Default Login Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Test Payment Card (Stripe Test Mode):**
- Card Number: `4242 4242 4242 4242`
- Expiry: Any future date (e.g., 12/25)
- CVC: Any 3 digits (e.g., 123)

⚠️ Change admin password immediately!

## Testing the Features

### Running Tests

```powershell
# Functional tests
python -m pytest tests/test_app.py -v

# Security tests
python -m pytest tests/test_security.py -v

# All tests with coverage
python -m pytest tests/ -v --cov=app --cov-report=html
```

### As a Customer:

1. **Register**: Create a new account
2. **Browse**: Go to Shop page, use filters
3. **Add to Cart**: Click "Add to Cart" on any book
4. **Checkout**: Complete purchase with Stripe (use test card above)
5. **Download**: Access purchased books from profile
6. **Review**: Write reviews for purchased books (only for purchased books)

### As an Admin:

1. **Login**: Use admin/admin123
2. **Dashboard**: View statistics
3. **Manage Books**: Add, edit, delete books
4. **Manage Categories**: Create categories
5. **View Orders**: Monitor all orders (with payment status)
6. **View Users**: See all registered users

## Troubleshooting

### Database Connection Error
**Error**: `Can't connect to MySQL server`
**Solution**: 
1. Ensure MySQL is running
2. Check DATABASE_URL in .env
3. Verify database exists: `SHOW DATABASES;`

### Import Error
**Error**: `ModuleNotFoundError`
**Solution**:
1. Activate virtual environment
2. Run: `pip install -r requirements.txt`

### Admin Login Fails
**Error**: Invalid credentials
**Solution**:
1. Run: `python init_db.py` again
2. Use: admin / admin123

### Tests Fail
**Error**: `pytest: command not found` or test failures
**Solution**:
1. Install test dependencies: `pip install -r requirements.txt`
2. Ensure virtual environment is activated
3. Check pytest.ini exists
4. Run: `python -m pytest tests/ -v`

### Stripe Payment Error
**Error**: `Invalid API key` or payment fails
**Solution**:
1. Verify STRIPE_PUBLIC_KEY and STRIPE_SECRET_KEY in .env
2. Use test mode keys (pk_test_... and sk_test_...)
3. Use test card: 4242 4242 4242 4242
4. Check console for webhook errors

### Coverage Report Issues
**Error**: Coverage report not generated
**Solution**:
1. Install coverage: `pip install coverage pytest-cov`
2. Run: `python -m pytest tests/ --cov=app --cov-report=html`
3. Open: htmlcov/index.html

## Project Features Overview

### Testing Features ⭐ NEW
✅ 26 functional tests (Registration, Login, Cart, Reviews, Error Pages)
✅ 17 security tests (SQL Injection, XSS, CSRF, Path Traversal)
✅ Comprehensive code coverage with pytest-cov
✅ All tests pass with 0 warnings
✅ Security validation for attack prevention

### Payment Processing ⭐ NEW
✅ Stripe PaymentIntent integration (Test Mode)
✅ Secure payment confirmation workflow
✅ Order creation only after payment success
✅ Webhook handling for payment events
✅ Payment status tracking

### Security Features
✅ Bcrypt password hashing (verified by tests)
✅ CSRF protection on all forms (tested)
✅ Session security (HTTPOnly, Secure cookies)
✅ SQL injection prevention - ORM parameterized queries (6 tests)
✅ XSS prevention - Auto-escaping (5 tests)
✅ Role-based access control
✅ Purchase verification for downloads
✅ One-time book purchase enforcement
✅ Path traversal attack prevention (tested)
✅ Authentication bypass prevention (tested)
✅ Session fixation protection (tested)
✅ Mass assignment protection (tested)
✅ Password hashing verification (tested)

### User Features
✅ Registration and authentication
✅ Browse and search books
✅ Filter by category and price
✅ Shopping cart management (no quantity for digital books)
✅ Stripe secure checkout
✅ Order history with payment status
✅ Download purchased books
✅ Review and rate books (one per user per book)
✅ User profile with purchase history

### Admin Features
✅ Dashboard with statistics
✅ Manage books (CRUD)
✅ Manage categories
✅ View all users
✅ View all orders with payment status
✅ Product inventory management

## Database Schema

- **users**: User accounts and authentication
- **categories**: Book categories
- **books**: Book catalog
- **orders**: Purchase orders
- **order_items**: Items in each order
- **reviews**: Book reviews and ratings
- **cart_items**: Shopping cart items

## API Endpoints

### Public Routes
- `GET /` - Home page
- `GET /shop` - Browse books with filters
- `GET /book/<id>` - Book details with reviews
- `GET /auth/register` - User registration
- `GET /auth/login` - User login

### User Routes (Authenticated)
- `POST /cart/add/<id>` - Add to cart
- `GET /cart` - View cart
- `POST /cart/remove/<id>` - Remove from cart
- `GET /checkout` - Checkout page
- `POST /checkout` - Create PaymentIntent
- `POST /payment/confirmation` - Confirm payment
- `GET /order/<id>` - View order
- `GET /profile` - User profile
- `GET /book/<id>/review` - Review page
- `POST /book/<id>/review` - Submit review
- `GET /download/<file>` - Download book (verification required)

### Admin Routes (Admin Only)
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/books` - Manage books
- `POST /admin/books` - Create book
- `GET /admin/books/<id>/edit` - Edit book
- `GET /admin/categories` - Manage categories
- `GET /admin/users` - View users
- `GET /admin/orders` - View orders

### API Endpoints
- `GET /api/books` - Books list (JSON)
- `POST /stripe/webhook` - Stripe webhook

### Error Pages
- `GET /404` - Page not found
- `GET /403` - Access forbidden
- `GET /500` - Server error

## Quick Management Commands

### Using Interactive Menu

```powershell
python manage.py
```

Menu options:
1. **Setup Environment** - Install dependencies
2. **Verify Setup** - Check Python and packages
3. **Initialize Database** - Create tables and sample data
4. **Create Admin User** - Add new admin account
5. **Run Development Server** - Start Flask app
6. **Create Database Migration** - SQLAlchemy migration
7. **Apply Database Migration** - Run migrations
8. **View Database Info** - Show statistics
9. **Run Tests** - Run functional tests (test_app.py)
10. **Run Security Tests** - Run security tests (test_security.py)
11. **Run All Tests with Coverage** - Full test suite with report
12. **Clean Test Cache** - Remove .pytest_cache and __pycache__
13. **Exit** - Quit menu

### Direct Commands

```powershell
# Install dependencies
pip install -r requirements.txt

# Verify setup
python verify_setup.py

# Initialize database
python init_db.py

# Create admin user
python create_admin.py

# Run tests
python -m pytest tests/test_app.py -v
python -m pytest tests/test_security.py -v
python -m pytest tests/ -v --cov=app --cov-report=html

# Start server
python run.py

# Database migrations
flask db migrate -m "migration message"
flask db upgrade
```

## Next Steps

1. **Verify Everything Works**
   - Run tests: `python manage.py` → Option 11
   - All 43 tests should pass ✅

2. **Add Real Books**
   - Login as admin
   - Use admin panel to add books
   - Upload book files to `app/static/books/`

3. **Customize Categories**
   - Use admin panel to create categories
   - Or update database directly

4. **Setup Stripe (Production)**
   - Use live keys (pk_live_... and sk_live_...)
   - Configure webhook endpoint
   - Test with real cards

5. **Change Admin Password**
   - Login as admin
   - Change password in user settings
   - Or update database directly

6. **Test Payment Flow**
   - Use test card: 4242 4242 4242 4242
   - Create account and purchase book
   - Verify order created and download works

7. **Run Security Tests**
   - Verify all 17 security tests pass
   - Review security test results
   - Check for any vulnerabilities

8. **Customize Styling**
   - Edit `app/static/css/style.css`
   - Modify HTML templates in `app/templates/`
   - Update colors, fonts, layout

## Production Deployment Checklist

Before deploying to production:

### Security
- [ ] Set `FLASK_ENV=production` in .env
- [ ] Generate strong, random SECRET_KEY
- [ ] Change default admin password
- [ ] Set up proper MySQL user (limited privileges)
- [ ] Enable HTTPS with SSL/TLS certificates
- [ ] Configure security headers (Talisman)
- [ ] Run all tests: `pytest tests/ -v`
- [ ] Run security tests: `pytest tests/test_security.py -v`

### Payment Processing
- [ ] Switch to Stripe live keys (pk_live_... and sk_live_...)
- [ ] Configure production webhook endpoint
- [ ] Test with real payment cards
- [ ] Verify order creation and email notifications

### Server Setup
- [ ] Use production WSGI server (gunicorn)
- [ ] Set up proper error logging
- [ ] Configure automated backups
- [ ] Set up monitoring and alerts
- [ ] Configure firewall rules
- [ ] Enable database encryption

### Deployment Command
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

## Need Help?

Check the main README.md for detailed documentation.

---

Happy Coding! 🚀