import os
import asyncio

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from src.redis.config import MyRedis
from src.redis.cache import Cache
from src.model.gptj import GPT
from src.schema.chat import Message


async def main():
    # initialize Redis
    redis = MyRedis()
    # create a rejon connection
    json_client = redis.create_rejson_connection()

    # add a new message to the chat history
    await Cache(json_client).add_message_to_cache(
        token=os.getenv('token'),
        source="human",
        message_data={
            "id": "1",
            "msg": "Hello",
            "timestamp": "2024-07-26 12:12:34:04.038491"
        }
    )

    data = await Cache(json_client).get_chat_history(
        token=os.getenv('token')
    )
    # print(data)

    # trim the cache data to get the last 4 messages
    message_data = data['messages']#[-4]
    print(message_data)

    # extract the msg in a list
    input = ["" + i['msg'] for i in message_data]
    input = " ".join(input)  # join it to an empty string

    res = GPT().query(input=input)

    # create a new Message for the bot response
    msg = Message(msg=res)
    print(msg)

    # add the bot response to the cache specifying the source as "bot"
    await Cache(json_client).add_message_to_cache(
        token=os.getenv('token'),
        source="bot",
        message_data=dict(msg)  #.dict()
    )

    # # create a Redis connection pool
    # redis = await redis.create_connection()
    # print(redis)

    # # set a simple key `key` and assing a string `value` to it
    # await redis.set("key", "value")

if __name__ == "__main__":
    asyncio.run(main())
