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

## Default Login Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

⚠️ Change this password immediately!

## Testing the Features

### As a Customer:

1. **Register**: Create a new account
2. **Browse**: Go to Shop page, use filters
3. **Add to Cart**: Click "Add to Cart" on any book
4. **Checkout**: Complete purchase with simulated payment
5. **Download**: Access purchased books from profile
6. **Review**: Write reviews for purchased books

### As an Admin:

1. **Login**: Use admin/admin123
2. **Dashboard**: View statistics
3. **Manage Books**: Add, edit, delete books
4. **Manage Categories**: Create categories
5. **View Orders**: Monitor all orders
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

## Project Features Overview

### Security Features
✅ Bcrypt password hashing
✅ CSRF protection on all forms
✅ Session security (HTTPOnly, Secure cookies)
✅ SQL injection prevention (ORM)
✅ Role-based access control
✅ Purchase verification for downloads

### User Features
✅ Registration and authentication
✅ Browse and search books
✅ Filter by category and price
✅ Shopping cart management
✅ Simulated checkout
✅ Order history
✅ Download purchased books
✅ Review and rate books

### Admin Features
✅ Dashboard with statistics
✅ Manage books (CRUD)
✅ Manage categories
✅ View all users
✅ View all orders
✅ Product inventory

## Database Schema

- **users**: User accounts and authentication
- **categories**: Book categories
- **books**: Book catalog
- **orders**: Purchase orders
- **order_items**: Items in each order
- **reviews**: Book reviews and ratings
- **cart_items**: Shopping cart items

## API Endpoints

- `GET /` - Home page
- `GET /shop` - Browse books with filters
- `GET /book/<id>` - Book details
- `POST /cart/add/<id>` - Add to cart
- `GET /cart` - View cart
- `POST /checkout` - Complete purchase
- `GET /profile` - User profile
- `GET /admin/dashboard` - Admin panel
- `GET /api/books` - Books API (JSON)

## Next Steps

1. **Add Real Books**: Use admin panel to add your books
2. **Customize Categories**: Add more relevant categories
3. **Change Admin Password**: Go to database and update
4. **Upload Book Files**: Add actual PDF/ePub files
5. **Customize Styling**: Edit static/css/style.css

## Production Deployment Notes

Before deploying to production:

1. Set `FLASK_ENV=production` in .env
2. Use a strong, random SECRET_KEY
3. Change admin password
4. Set up proper MySQL user with limited privileges
5. Enable HTTPS
6. Use a production WSGI server (gunicorn)
7. Set up proper error logging
8. Configure backups for database

## Need Help?

Check the main README.md for detailed documentation.

---

Happy Coding! 🚀