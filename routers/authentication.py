from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
import jwt
from passlib.context import CryptContext
from models.users import TokenData, User, UserCreate, UserInDB, Token
from config import db

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

# Hashing passwords
def get_password_hash(password):
    return pwd_context.hash(password)

# Verify passwords
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_user(username: str):
    user = await user_collection.find_one({'username': username})
    if user:
        return UserInDB(**user)
    return None

async def authenticate_user(user_collection, username: str, password: str):
    user = await get_user(user_collection, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Create JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

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


@router.post('/token', response_model=Token)
async def login_access_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()]):

    username = form_data.username
    
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

