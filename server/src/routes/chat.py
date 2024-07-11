import os
from fastapi import (
    APIRouter, Depends, FastAPI, WebSocket, Request, BackgroundTasks,
    HTTPException, WebSocketDisconnect
)
import uuid

from ..socket.connection import ConnectionManager
from ..socket.utils import get_token
from ..redis.producer import Producer
from ..redis.config import Redis

chat = APIRouter()

# initialize the connection manager
manager = ConnectionManager()

# intialize redis connection
redis = Redis()

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
async def websocket_endpint(
    websocket: WebSocket = WebSocket, token: str = Depends(get_token)
):
    # add the new websocket to the connction manager
    await manager.connect(websocket)

    # create a new Redis connection
    redis_client = await redis.create_connection()

    # initialize a producer with redis_client
    producer = Producer(redis_client)

    try:
        # run a while true loop to ensure the socket stays open
        while True:
            # receive any message sent by the client
            data = await websocket.receive_text()
            print(data)
            # TODO: send the received message from the client the AI model,
            # and send, the response from the AI model, back to the client

            # initialize stream data dictionnary
            stream_data = {}
            # add `data` to `stream_data` with the key `token`
            stream_data[token] = data
            # add `stream_data` to the stream using redis client `producer`
            await producer.add_to_stream(stream_data, "message_channel")
            # send a hard coded response back to the client - for now
            await manager.send_personal_message(
                "Response: Simulating response from the GPT service.",
                websocket
            )
    # execept when the socket gets disconnected
    except WebSocketDisconnect:
        manager.disconnect(websocket)
