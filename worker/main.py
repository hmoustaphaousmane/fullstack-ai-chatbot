import asyncio

from src.redis.config import MyRedis
from src.redis.cache import Cache


async def main():
    # initialize Redis
    redis = MyRedis()
    # create a rejon connection
    json_client = redis.create_rejson_connection()

    # add a new message to the chat history
    await Cache(json_client).add_message_to_cache(
        token="1ea18262-d763-4bc8-86f2-e9c9fc419e98",
        message_data={
            "id": "1",
            "msg": "Hello",
            "timestamp": "2024-07-26 12:12:34:04.038491"
        }
    )

    data = await Cache(json_client).get_chat_history(
        token="1ea18262-d763-4bc8-86f2-e9c9fc419e98"
    )
    print(data)
    # # create a Redis connection pool
    # redis = await redis.create_connection()
    # print(redis)

    # # set a simple key `key` and assing a string `value` to it
    # await redis.set("key", "value")

if __name__ == "__main__":
    asyncio.run(main())
