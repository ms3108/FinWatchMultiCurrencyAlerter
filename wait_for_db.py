import sys
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

def wait_for_db(db_url, max_attempts=10, delay=5):
    """Wait for the database to be ready."""
    engine = create_engine(db_url)
    for attempt in range(max_attempts):
        try:
            with engine.connect() as conn:
                conn.execute("SELECT 1")
                print("Database is ready!")
                return True
        except Exception as e:
            print(f"Waiting for database... Attempt {attempt + 1}/{max_attempts}")
            time.sleep(delay)
    
    print("Failed to connect to database after multiple attempts")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python wait_for_db.py <database_url>")
        sys.exit(1)
    
    if not wait_for_db(sys.argv[1]):
        sys.exit(1)
