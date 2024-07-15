from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

class Message(BaseModel):
    """Message class"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)  # chat id
    msg: str  # message text
    # automatically generated timestamp
    timestamp: str = Field(default_factory=lambda: str(datetime.now()))

class Chat(BaseModel):
    """A class that will hold data about a single Chat session"""
    token: str  # token
    messages: List[Message]
    name: str  # name of the user
    # automatically generated timestamp
    session_start: str = Field(default_factory=lambda: str(datetime.now()))
