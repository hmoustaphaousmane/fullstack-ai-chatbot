from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
import uuid


class Message(BaseModel):
    """Message class"""
    id = uuid.uuid4()  # chat id
    msg: str  # message text
    timestamp = str(datetime.now())  # automatically generated timestamp


class Chat(BaseModel):
    """A class that will hold data about a single Chat session"""
    token: str  # token
    messages: List[Message]
    name: str  # name of the user
    session_start = str(datetime.now())  # automatically generated timestamp
