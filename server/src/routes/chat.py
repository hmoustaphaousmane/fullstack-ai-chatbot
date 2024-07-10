import os
from fastapi import (
    APIRouter, FastAPI, WebSocket, Request, BackgroundTasks, HTTPException
)
import uuid

chat = APIRouter()

# @route    POST /token
# @desc     Route to generate chat token
# @access   Public


@chat.post("/token")
async def token_generator(name: str, request: Request):
    """
    Chat token generator

    arg: client name
    """

    # Check to ensure the name field is not empty
    if name == "":
        raise HTTPException(status_code=400, detail={
            "loc": "name", "msg": "Enter a valid name"
        })
    
    # Generate a token using uuid4
    token = str(uuid.uuid4())

    # session data
    data = {"name": name, "token": token}

    # return the session data to the client
    return data


# @route    POST /refresh_token
# @desc     Route to refresh token
# @access   Public


@chat.post("/refresh_token")
async def refresh_token(request: Request):
    return None


# @route    Websoket /chat
# @desc     Socket for chatbot
# @access Public


@chat.websocket("/chat")
async def websocket_endpint(websocket: WebSocket = WebSocket):
    return None
