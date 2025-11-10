from sqlalchemy import create_engine, Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

DATABASE_URL = "sqlite:///./wardrobe.db"

Base = declarative_base()

class User(Base):
    """Represents a user in the users table (SQLAlchemy Model)."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    wardrobe_items = relationship("WardrobeItem", back_populates="owner")

class WardrobeItem(Base):
    """Represents a wardrobe item in the wardrobe_items table (SQLAlchemy Model)."""
    __tablename__ = 'wardrobe_items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    item_metadata = Column(JSON)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="wardrobe_items")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    print("Creating database and tables...")
    Base.metadata.create_all(bind=engine)
    print("Database and tables created successfully.")

if __name__ == "__main__":
    create_db_and_tables()