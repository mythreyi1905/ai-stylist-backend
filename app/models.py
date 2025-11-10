from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class UserBase(BaseModel):
    """Base model for user, contains common fields."""
    username: str

class UserCreate(UserBase):
    """Model for creating a new user. Expects a password."""
    password: str

class User(UserBase):
    """Model for returning a user from the API. Never includes the password."""
    id: int

    class Config:
         orm_mode = True

class Token(BaseModel):
    """Model for the authentication token response."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Model for the data contained within a token."""
    username: Optional[str] = None


class WardrobeItemBase(BaseModel):
    name: str
    item_metadata: Dict[str, Any]

class WardrobeItemCreate(WardrobeItemBase):
    pass

class WardrobeItem(WardrobeItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class StyleRequest(BaseModel):
    occasion: str
    weather_context: str