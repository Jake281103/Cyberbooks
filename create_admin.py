"""
Create or update admin user for CyberBooks
"""

from app import create_app, db
from app.models import User
import getpass

def create_admin():
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("CyberBooks - Admin User Management")
        print("=" * 60)
        print()
        
        username = input("Enter admin username [admin]: ").strip() or "admin"
        
        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        
        if existing_user:
            print(f"\n⚠️  User '{username}' already exists.")
            choice = input("Do you want to update the password? (yes/no): ").strip().lower()
            if choice not in ['yes', 'y']:
                print("Operation cancelled.")
                return
            user = existing_user
            action = "updated"
        else:
            user = User()
            user.username = username
            user.email = input("Enter email: ").strip()
            user.full_name = input("Enter full name: ").strip()
            action = "created"
        
        # Get password
        while True:
            password = getpass.getpass("Enter password (min 8 characters): ")
            if len(password) < 8:
                print("❌ Password must be at least 8 characters long")
                continue
            
            confirm_password = getpass.getpass("Confirm password: ")
            if password != confirm_password:
                print("❌ Passwords do not match")
                continue
            
            break
        
        # Set password and admin status
        user.set_password(password)
        user.is_admin = True
        
        if action == "created":
            db.session.add(user)
        
        db.session.commit()
        
        print()
        print(f"✅ Admin user '{username}' {action} successfully!")
        print()
        print("You can now login with:")
        print(f"   Username: {username}")
        print(f"   Password: (the password you just entered)")
        print()

if __name__ == '__main__':
    try:
        create_admin()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
