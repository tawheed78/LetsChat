# from routers.authentication import pwd_context 
from datetime import datetime, timedelta
from config import SECRET_KEY as SECRET_KEY, ALGORITHM as ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES as ATEM
import jwt
# Hashing passwords
def get_password_hash(password):
    from routers.authentication import pwd_context
    return pwd_context.hash(password)

# Verify passwords
def verify_password(plain_password, hashed_password):
    from routers.authentication import pwd_context
    return pwd_context.verify(plain_password, hashed_password)

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