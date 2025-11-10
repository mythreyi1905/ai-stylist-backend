from . import database
from sqlalchemy.orm import Session

def get_db():
    """
    Dependency function to get a database session for each request.
    Ensures the database session is always closed after the request.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()