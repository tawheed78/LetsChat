
from fastapi import APIRouter, Depends
from config import db
from models.users import UserFriends, User
from .authentication import get_current_user


router = APIRouter()

user_collection = db['users']

@router.get('/chat-list/')
async def chat_list(current_user:User=Depends(get_current_user)) :
    user = await user_collection.find_one({"username":current_user.username})
    if user:
        chat_list = user.get('friends', [])
        return chat_list
    return []
    