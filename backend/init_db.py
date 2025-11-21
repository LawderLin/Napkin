"""
Database initialization script for Napkin
"""
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'napkin'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
}

def init_database():
    """Initialize the database with the required schema"""
    try:
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        print("Creating notes table...")
        cur.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id VARCHAR(32) PRIMARY KEY,
                content TEXT NOT NULL,
                password_hash VARCHAR(64),
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                expires_at TIMESTAMP,
                views INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        
        # Verify table was created
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'notes'
        """)
        
        if cur.fetchone():
            print("✅ Database initialized successfully!")
            print("Table 'notes' created.")
        else:
            print("⚠️  Table creation may have failed.")
        
        cur.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        print("\nPlease make sure:")
        print("1. PostgreSQL is running")
        print("2. Database 'napkin' exists (create it with: createdb napkin)")
        print("3. Database credentials in .env are correct")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("Napkin Database Initialization")
    print("==============================\n")
    init_database()
