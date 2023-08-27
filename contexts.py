 
# from datetime import datetime, timedelta
# from typing import Annotated
# from config import SECRET_KEY as SECRET_KEY, ALGORITHM as ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES as ATEM
# import jwt
# from fastapi import Depends, HTTPException, Header
# from jose import JWTError, jwt
# from models.users import User
# from routers.authentication import oauth2_scheme




# # Create JWT token
# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt



# async def get_current_user(authorization : str = Header(None)) -> str:
#     if authorization is None:
#         raise HTTPException(status_code=401, detail="Authorization header missing")
#     try:
#         token = authorization.split(" ")[1]
#         print(token)
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=401, detail="Invalid authentication token")
#         return username
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid authentication token")

# def fake_decode_token(token):
#     return User(
#         username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
#     )

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     return user
