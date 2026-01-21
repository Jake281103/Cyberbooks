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

2. **Product Management**
   - Full CRUD operations for books (Admin only)
   - Categories: Network Security, Cryptography, Ethical Hacking, Digital Forensics, etc.
   - Book attributes: title, author, ISBN, price, description, file format (PDF/ePub)
   - Stock management

3. **Search and Filtering**
   - Keyword search (title and author)
   - Filter by category
   - Filter by price range
   - Sort by newest, oldest, price, and rating

4. **Shopping Cart and Checkout**
   - Add/remove items from cart
   - Update quantities
   - Simulated secure checkout process
   - Order confirmation and order history

5. **Download and Access Control**
   - Purchase verification before download access
   - Only authenticated buyers can download
   - Instant access after purchase

6. **Review and Rating System**
   - 5-star rating system
   - Written reviews with validation
   - Only purchasers can review
   - One review per user per book

7. **Database Management**
   - MySQL with SQLAlchemy ORM
   - Normalized relational structure
   - Foreign key constraints
   - Data integrity and validation

8. **Responsive Design** ⭐ NEW
   - Mobile-first approach with 5 breakpoint system
   - Hamburger navigation menu for mobile devices
   - Touch-optimized UI elements (min 44-48px targets)
   - Adaptive layouts for phones, tablets, and desktops
   - Progressive enhancement for modern browsers
   - See [RESPONSIVE_DESIGN.md](RESPONSIVE_DESIGN.md) for details

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
├── config.py                    # Environment-based configuration
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── init_db.py                   # Database initialization script
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore patterns
└── README.md                    # This file
```

## Technology Stack

- **Backend**: Flask 3.0.3
- **Database**: MySQL with PyMySQL driver
- **ORM**: SQLAlchemy 3.1.1
- **Migration**: Flask-Migrate 4.0.7
- **Authentication**: Flask-Login 0.6.3
- **Forms**: Flask-WTF 1.2.1, WTForms 3.1.2
- **Security**: bcrypt 4.1.3, Flask-Talisman 1.1.0
- **Password Hashing**: bcrypt with salt
- **Session Management**: Flask sessions with security headers

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
- Username: `admin`
- Password: `admin123`

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

1. **Password Security**
   - Bcrypt hashing with automatic salt generation
   - Minimum 8-character password requirement
   - Password confirmation validation

2. **Session Security**
   - Secure session cookies
   - HTTPOnly cookies to prevent XSS
   - SameSite cookies for CSRF protection
   - 2-hour session timeout

3. **CSRF Protection**
   - Flask-WTF CSRF tokens on all forms
   - Automatic token validation

4. **Access Control**
   - Role-based access (admin/user)
   - Purchase verification for downloads
   - Login required decorators

5. **SQL Injection Prevention**
   - SQLAlchemy ORM parameterized queries
   - Input validation with WTForms

6. **Headers Security** (Production)
   - Flask-Talisman for security headers
   - HTTPS enforcement in production
   - Content Security Policy

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
# Set testing environment
set FLASK_ENV=testing

# Run tests (add test files to tests/ directory)
python -m pytest
```

### Database Migrations

```bash
# After model changes
flask db migrate -m "Description of changes"
flask db upgrade
```

## Production Deployment

1. **Update Configuration**
   - Set `FLASK_ENV=production`
   - Use strong SECRET_KEY
   - Configure production database
   - Enable HTTPS

2. **Security Checklist**
   - Change default admin password
   - Use environment variables for secrets
   - Enable Flask-Talisman
   - Set up SSL/TLS certificates
   - Configure firewall rules
   - Regular security updates

3. **WSGI Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 run:app
   ```

## Troubleshooting

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

## License

MIT License - Educational purposes

## Support

For issues and questions, please refer to the project documentation or contact the development team.

---

**CyberBooks** - Securing Knowledge, One Book at a Time 🔐📚
