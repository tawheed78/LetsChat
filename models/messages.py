from datetime import datetime
from pydantic import BaseModel
from typing import List

class Messages(BaseModel):
    sender : str
    receiver : str
    message : str
    timestamp : datetime.utcnow()