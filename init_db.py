import logging
from app.db.session import engine
from app.db.base import Base
# This line is crucial: it imports the models so that Base knows about them.
from app.db import models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db() -> None:
    logger.info("Creating database tables...")
    try:
        # The Base object has a metadata attribute that stores the schema of all tables
        # that inherit from it. create_all() creates all these tables in the database.
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

if __name__ == "__main__":
    init_db()
