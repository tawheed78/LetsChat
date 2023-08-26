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

class User(BaseModel):
    username: str
    email: str | None = None


    