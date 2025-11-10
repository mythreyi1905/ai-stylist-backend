from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from . import auth
from . import crud, models, database
from .dependencies import get_db 
from . import stylist
from typing import List

#ensures that the database tables are created if they don't exist
database.create_db_and_tables()

app = FastAPI(
    title="AI Fashion Stylist API",
    description="The backend API for the AI Fashion Stylist application.",
    version="0.1.0"
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Stylist API!"}

@app.get("/users/me", response_model=models.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    """
    Get the current logged-in user's details.
    """
    return current_user

@app.post("/users/", response_model=models.User, status_code=status.HTTP_201_CREATED)
def register_user(user: models.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user.
    """
    # Check if a user with that username already exists
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # If not, create the new user
    new_user = crud.create_user(db=db, user=user)
    return new_user

@app.post("/token", response_model=models.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint to login a user and get an access token.
    FastAPI's OAuth2PasswordRequestForm expects a form-data body with 'username' and 'password'.
    """
    user = crud.authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create the token
    access_token = auth.create_access_token(
        data={"sub": user.username}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/wardrobe/", response_model=models.WardrobeItem, status_code=status.HTTP_201_CREATED)
def add_item_to_wardrobe(
    item: models.WardrobeItemCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Endpoint to add a new clothing item to the current user's wardrobe.
    This endpoint is protected; a valid access token must be provided.
    """
    return crud.create_wardrobe_item(db=db, item=item, user_id=current_user.id)

@app.delete("/wardrobe/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_wardrobe_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Delete a specific item from the current user's wardrobe.
    """
    deleted_item = crud.delete_wardrobe_item(db=db, item_id=item_id, user_id=current_user.id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return

@app.put("/wardrobe/{item_id}", response_model=models.WardrobeItem)
def edit_wardrobe_item(
    item_id: int,
    item_update: models.WardrobeItemCreate, # We can reuse the Create model for updates
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Update a specific item in the current user's wardrobe.
    """
    updated_item = crud.update_wardrobe_item(
        db=db, item_id=item_id, item_update=item_update, user_id=current_user.id
    )
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.get("/wardrobe/", response_model=List[models.WardrobeItem])
def view_wardrobe(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Endpoint to view all items in the current user's wardrobe.
    This endpoint is also protected.
    """
    return crud.get_wardrobe_items_by_user(db=db, user_id=current_user.id)

@app.post("/style-me/", response_model=dict)
def get_style_suggestion(
    request: models.StyleRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    The main AI Stylist endpoint.
    Takes a user's occasion and weather context, retrieves their wardrobe,
    and returns a generated outfit suggestion.
    """
    user_wardrobe = crud.get_wardrobe_items_by_user(db, user_id=current_user.id)

    if not user_wardrobe:
        return {"suggestion": "Your wardrobe is empty! Please add some items before getting styled."}

    stylist_instance = stylist.AIStylist(user_wardrobe)
    suggestion = stylist_instance.get_suggestion(
        user_query=request.occasion,
        weather_context=request.weather_context
    )

    return {"suggestion": suggestion}

