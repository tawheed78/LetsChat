from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()


client = AsyncIOMotorClient(os.getenv("MONGO_URI"))

if client:
    print("******MongoDB connection successful.******")
else:
    print("connection failed!")

db = client["LetsChat"]


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')