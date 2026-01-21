"""
Quick Start Guide for CyberBooks
Run this script to verify your setup and get started
"""

import sys
import os

def check_requirements():
    """Check if all required packages are installed"""
    required_packages = [
        'flask', 'flask_sqlalchemy', 'flask_migrate', 'flask_login',
        'flask_wtf', 'wtforms', 'bcrypt', 'pymysql', 'flask_talisman'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing packages:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\nRun: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are installed")
        return True

def check_env_file():
    """Check if .env file exists"""
    if os.path.exists('.env'):
        print("✅ .env file found")
        return True
    else:
        print("❌ .env file not found")
        print("   Run: copy .env.example .env")
        print("   Then edit .env with your database credentials")
        return False

def check_database():
    """Check database connection"""
    try:
        from app import create_app, db
        app = create_app()
        with app.app_context():
            # Try to connect
            db.engine.connect()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   Make sure MySQL is running and database 'cyberbooks' exists")
        print("   SQL: CREATE DATABASE cyberbooks;")
        return False

def main():
    print("=" * 60)
    print("CyberBooks - Setup Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", sys.version_info >= (3, 11)),
        ("Required Packages", check_requirements()),
        ("Environment File", check_env_file()),
        ("Database Connection", check_database())
    ]
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_passed = all(result for _, result in checks)
    
    if all_passed:
        print("✅ All checks passed!")
        print()
        print("Next steps:")
        print("1. Run: python init_db.py")
        print("2. Run: python run.py")
        print("3. Open: http://localhost:5000")
        print()
        print("Default admin credentials:")
        print("   Username: admin")
        print("   Password: admin123")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
    
    print("=" * 60)

if __name__ == '__main__':
    main()
