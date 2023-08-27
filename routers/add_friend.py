from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from config import db
from models.users import UserFriends, User
from .authentication import get_current_user, get_user
from motor.motor_asyncio import AsyncIOMotorCollection

router = APIRouter()

user_collection = db['users']



@router.post('/add/')
async def add_friend(username, current_user: User = Depends(get_current_user)):
    add_user = await user_collection.find_one({"username":username})
    # print(current_user)
    if not add_user:
        raise HTTPException(status_code=400, detail="Username does not exist")
    
    await user_collection.update_one(
        {"username": current_user.username},
        {"$addToSet" : {"friends" : add_user['username']}}
    )
    return {"message": "Friend added successfully"}

