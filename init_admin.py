"""
Script to initialize the admin user in the database.
Run this script once to create the admin account.
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Admin
from app.auth import get_password_hash

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


def init_admin():
    db: Session = SessionLocal()
    
    try:
        # Check if admin already exists
        existing_admin = db.query(Admin).filter(Admin.username == "admin").first()
        
        if existing_admin:
            print("[INFO] Admin user already exists!")
            print(f"   Username: {existing_admin.username}")
            print(f"   Created at: {existing_admin.created_at}")
            return
        
        # Create admin user
        admin = Admin(
            username="admin",
            hashed_password=get_password_hash("hfcc2024")
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        print("[SUCCESS] Admin user created successfully!")
        print(f"   Username: admin")
        print(f"   Password: hfcc2024")
        print(f"   Created at: {admin.created_at}")
        
    except Exception as e:
        print(f"[ERROR] Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing admin user...")
    print("-" * 50)
    init_admin()
    print("-" * 50)

