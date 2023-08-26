from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from routers.authentication import router as authentication_router

# client = AsyncIOMotorClient("mongodb+srv://tawheed:FJedrjvIV8dIGhKl@letschat.o7u0o5n.mongodb.net/?retryWrites=true&w=majority")

# if client:
#     print("******MongoDB connection successful.******")
# else:
#     print("connection failed!")

# db = client["LetsChat"]

app = FastAPI()

app.include_router(authentication_router)

