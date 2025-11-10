from sqlalchemy.orm import Session
from . import database, models, auth

def get_user_by_username(db: Session, username: str):
    """Fetches a single user from the database by their username."""
    return db.query(database.User).filter(database.User.username == username).first()

def create_user(db: Session, user: models.UserCreate):
    """Creates a new user in the database."""
    # Hash the password before storing it
    hashed_password = auth.get_hashed_password(user.password)
    
    # Create a new SQLAlchemy User object
    db_user = database.User(username=user.username, hashed_password=hashed_password)
    
    # Add the new user object to the session
    db.add(db_user)
    # Commit the changes to the database
    db.commit()
    # Refresh the object to get the new ID from the database
    db.refresh(db_user)
    
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticates a user.
    
    Checks if the user exists and if the provided password is correct.
    Returns the user object if successful, otherwise returns False.
    """
    user = get_user_by_username(db, username=username)
    if not user:
        # User not found
        return False
    if not auth.verify_password(password, user.hashed_password):
        # Incorrect password
        return False
    # Authentication successful
    return user


def create_wardrobe_item(db: Session, item: models.WardrobeItemCreate, user_id: int):
    """Adds a new wardrobe item to the database for a specific user."""
    db_item = database.WardrobeItem(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_wardrobe_items_by_user(db: Session, user_id: int):
    """Fetches all wardrobe items for a specific user."""
    return db.query(database.WardrobeItem).filter(database.WardrobeItem.owner_id == user_id).all()

def delete_wardrobe_item(db: Session, item_id: int, user_id: int):
    db_item = db.query(database.WardrobeItem).filter(
        database.WardrobeItem.id == item_id,
        database.WardrobeItem.owner_id == user_id
    ).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item
    return None

def update_wardrobe_item(db: Session, item_id: int, item_update: models.WardrobeItemCreate, user_id: int):
    """Updates an existing wardrobe item for a specific user."""
    db_item = db.query(database.WardrobeItem).filter(
        database.WardrobeItem.id == item_id,
        database.WardrobeItem.owner_id == user_id
    ).first()

    if db_item:
        # Update the item's data from the request
        update_data = item_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        
        db.commit()
        db.refresh(db_item)
    
    return db_item