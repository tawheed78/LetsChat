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
    mobile : int
    

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
    friends : List


# class UserInDB(BaseModel):
#     _id: str  # Assuming _id is a string field
#     username: str
#     email: str
#     hashed_password: str
#     friends: list = []

# class User(BaseModel):
#     username: str
#     email: str | None = None