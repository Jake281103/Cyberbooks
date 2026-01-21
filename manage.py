"""
CyberBooks Management Script
Convenient commands for common tasks
"""

import sys
import os

def print_menu():
    print("\n" + "=" * 60)
    print("CyberBooks - Management Menu")
    print("=" * 60)
    print("\n1. Setup Environment")
    print("2. Verify Setup")
    print("3. Initialize Database")
    print("4. Create Admin User")
    print("5. Run Development Server")
    print("6. Create Database Migration")
    print("7. Apply Database Migration")
    print("8. View Database Info")
    print("9. Exit")
    print("\n" + "=" * 60)

def setup_env():
    """Install dependencies"""
    print("\n📦 Installing dependencies...")
    os.system("pip install -r requirements.txt")
    print("\n✅ Dependencies installed!")
    input("\nPress Enter to continue...")

def verify_setup():
    """Run setup verification"""
    print("\n🔍 Verifying setup...")
    os.system("python verify_setup.py")
    input("\nPress Enter to continue...")

def init_db():
    """Initialize database"""
    print("\n🗄️  Initializing database...")
    os.system("python init_db.py")
    input("\nPress Enter to continue...")

def create_admin():
    """Create admin user"""
    print("\n👤 Creating admin user...")
    os.system("python create_admin.py")
    input("\nPress Enter to continue...")

def run_server():
    """Run development server"""
    print("\n🚀 Starting development server...")
    print("Press Ctrl+C to stop\n")
    os.system("python run.py")

def create_migration():
    """Create database migration"""
    print("\n📝 Creating database migration...")
    message = input("Enter migration message: ")
    os.system(f'flask db migrate -m "{message}"')
    input("\nPress Enter to continue...")

def apply_migration():
    """Apply database migration"""
    print("\n⬆️  Applying database migration...")
    os.system("flask db upgrade")
    input("\nPress Enter to continue...")

def db_info():
    """Show database information"""
    print("\n🗄️  Database Information")
    print("=" * 60)
    
    try:
        from app import create_app, db
        from app.models import User, Book, Category, Order, Review, CartItem
        
        app = create_app()
        with app.app_context():
            print(f"Users: {User.query.count()}")
            print(f"Books: {Book.query.count()}")
            print(f"Categories: {Category.query.count()}")
            print(f"Orders: {Order.query.count()}")
            print(f"Reviews: {Review.query.count()}")
            print(f"Cart Items: {CartItem.query.count()}")
            
            print("\n📊 Admin Users:")
            admins = User.query.filter_by(is_admin=True).all()
            for admin in admins:
                print(f"  - {admin.username} ({admin.email})")
            
            print("\n📚 Categories:")
            categories = Category.query.all()
            for cat in categories:
                print(f"  - {cat.name}: {cat.books.count()} books")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("\nPress Enter to continue...")

def main():
    """Main menu loop"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_menu()
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == '1':
            setup_env()
        elif choice == '2':
            verify_setup()
        elif choice == '3':
            init_db()
        elif choice == '4':
            create_admin()
        elif choice == '5':
            run_server()
        elif choice == '6':
            create_migration()
        elif choice == '7':
            apply_migration()
        elif choice == '8':
            db_info()
        elif choice == '9':
            print("\n👋 Goodbye!")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
