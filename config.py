from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()


client = AsyncIOMotorClient("mongodb+srv://tawheed:FJedrjvIV8dIGhKl@letschat.o7u0o5n.mongodb.net/?retryWrites=true&w=majority")

if client:
    print("******MongoDB connection successful.******")
else:
    print("connection failed!")

db = client["LetsChat"]


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')