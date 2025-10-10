"""
Migration script to add updated_at column to existing quiet_time_entries table.
Run this script once to update your database schema.
"""
from sqlalchemy import text
from app.database import SessionLocal, engine
from app.models import Base

def migrate_database():
    print("Starting database migration...")
    print("-" * 50)
    
    db = SessionLocal()
    
    try:
        # Check if column already exists
        check_query = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='quiet_time_entries' 
            AND column_name='updated_at';
        """)
        
        result = db.execute(check_query).fetchone()
        
        if result:
            print("[SUCCESS] Column 'updated_at' already exists!")
            print("   No migration needed.")
            return
        
        # Add updated_at column
        print("[INFO] Adding 'updated_at' column to quiet_time_entries table...")
        
        alter_query = text("""
            ALTER TABLE quiet_time_entries 
            ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE 
            DEFAULT CURRENT_TIMESTAMP;
        """)
        
        db.execute(alter_query)
        db.commit()
        
        # Update existing rows to set updated_at = created_at
        print("[INFO] Setting updated_at to created_at for existing entries...")
        
        update_query = text("""
            UPDATE quiet_time_entries 
            SET updated_at = created_at 
            WHERE updated_at IS NULL;
        """)
        
        db.execute(update_query)
        db.commit()
        
        print("[SUCCESS] Migration completed successfully!")
        print("   - Added 'updated_at' column")
        print("   - Populated existing entries with created_at values")
        
    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("-" * 50)


if __name__ == "__main__":
    migrate_database()

