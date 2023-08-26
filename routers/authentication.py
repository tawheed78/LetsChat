from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from models.users import UserCreate
from config import db
from contexts import get_password_hash, verify_password, create_access_token

router = APIRouter()

# Set your secret key and other configurations
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

user_collection = db['users'] 

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post('/register')
async def register_user(user : UserCreate):
    existing_user = await user_collection.find_one({"username":user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = {
        "username" : user.username,
        "email" : user.email,
        "password" : hashed_password
    }
    inserted_new_user = await user_collection.insert_one(new_user)
    return {"message": "User registered successfully"}


@router.post('/login')
async def login_access_token(form_data : OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    # print(username)
    # password = form_data.password
    user = await user_collection.find_one({"username":username})
    # print(user)
    if not user or not verify_password(form_data.password, user['password']):
        raise HTTPException(
            status_code=404,
            detail={"error":"Invalid credentials."},
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}