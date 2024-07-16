import os
import json
from fastapi import (
    APIRouter, Depends, FastAPI, WebSocket, Request, BackgroundTasks,
    HTTPException, WebSocketDisconnect
)
import uuid

from ..socket.connection import ConnectionManager
from ..socket.utils import get_token
from ..redis.producer import Producer
from ..redis.config import MyRedis
from ..schema.chat import Chat

chat = APIRouter()

# initialize the connection manager
manager = ConnectionManager()

# intialize redis connection
redis = MyRedis()

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
    
    # create redis JSON connection
    json_client = redis.create_rejson_connection()

    # create new chat session
    chat_session = Chat(
        token=token,
        messages=[],
        name=name
    )

    # store chat session in redis JSON with the to token as key
    # json_client.jsonset(str(token), Path.rootPath(), chat_session.model_dump())
    json_client.set(str(token), json.dumps(chat_session.model_dump()))

    # set a timeout for redis data
    redis_client = await redis.create_connection()
    await redis_client.expire(str(token), 3600)
    # i.e. chat session data will be lost after 60 min

    # return the session data to the client
    return chat_session


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
