from pydantic import BaseModel
from typing import List

# User model
class Name(BaseModel):
    fname : str
    lname : str

class UserCreate(BaseModel):
    name : Name
    email : str
    username: str
    password: str
    mobile : str
    

class UserFriends(BaseModel):
    friend_username : str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    username: str
    email: str | None = None
    hashed_password: str | None=None
    friends: List[str] = []

class AddFriendRequest(BaseModel):
    username: str