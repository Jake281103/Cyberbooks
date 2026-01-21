"""
Database Initialization Script for CyberBooks
This script initializes the database with sample categories and an admin user.
"""

from app import create_app, db
from app.models import User, Category, Book
from decimal import Decimal

def init_database():
    app = create_app()
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        
        # Create categories
        print("Creating categories...")
        categories_data = [
            {
                'name': 'Network Security',
                'description': 'Books about network protocols, firewalls, and network defense'
            },
            {
                'name': 'Cryptography',
                'description': 'Encryption, decryption, and cryptographic algorithms'
            },
            {
                'name': 'Ethical Hacking',
                'description': 'Penetration testing and ethical hacking techniques'
            },
            {
                'name': 'Digital Forensics',
                'description': 'Computer forensics and digital investigation'
            },
            {
                'name': 'Malware Analysis',
                'description': 'Analyzing and understanding malicious software'
            },
            {
                'name': 'Web Security',
                'description': 'Web application security and OWASP guidelines'
            }
        ]
        
        for cat_data in categories_data:
            if not Category.query.filter_by(name=cat_data['name']).first():
                category = Category(**cat_data)
                db.session.add(category)
        
        db.session.commit()
        print(f"Created {len(categories_data)} categories")
        
        # Create admin user
        print("Creating admin user...")
        admin_email = "admin@cyberbooks.com"
        if not User.query.filter_by(email=admin_email).first():
            admin = User(
                username='admin',
                email=admin_email,
                full_name='Administrator',
                is_admin=True
            )
            admin.set_password('admin123')  # Change this in production!
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: username=admin, password=admin123")
        else:
            print("Admin user already exists")
        
        # Create sample books
        print("Creating sample books...")
        crypto_cat = Category.query.filter_by(name='Cryptography').first()
        ethical_cat = Category.query.filter_by(name='Ethical Hacking').first()
        network_cat = Category.query.filter_by(name='Network Security').first()
        
        sample_books = [
            {
                'title': 'Applied Cryptography',
                'author': 'Bruce Schneier',
                'isbn': '9781119096726',
                'description': 'A comprehensive guide to cryptographic protocols, algorithms, and techniques.',
                'price': Decimal('49.99'),
                'category_id': crypto_cat.id if crypto_cat else None,
                'file_format': 'PDF'
            },
            {
                'title': 'The Web Application Hacker\'s Handbook',
                'author': 'Dafydd Stuttard',
                'isbn': '9781118026472',
                'description': 'Finding and exploiting security flaws in web applications.',
                'price': Decimal('44.99'),
                'category_id': ethical_cat.id if ethical_cat else None,
                'file_format': 'PDF'
            },
            {
                'title': 'Network Security Essentials',
                'author': 'William Stallings',
                'isbn': '9780134527338',
                'description': 'Applications and standards for network security.',
                'price': Decimal('39.99'),
                'category_id': network_cat.id if network_cat else None,
                'file_format': 'ePub'
            }
        ]
        
        for book_data in sample_books:
            if not Book.query.filter_by(isbn=book_data['isbn']).first():
                book = Book(**book_data)
                db.session.add(book)
        
        db.session.commit()
        print(f"Created {len(sample_books)} sample books")
        
        print("\n✅ Database initialization complete!")
        print("\n📝 Login credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n⚠️  Remember to change the admin password in production!")

if __name__ == '__main__':
    init_database()
