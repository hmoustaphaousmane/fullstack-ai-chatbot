import asyncio

from src.redis.config import Redis


async def main():
    # initialize Redis
    redis = Redis()
    # create a Redis connection pool
    redis = await redis.create_connection()
    print(redis)

    # set a simple key `key` and assing a string `value` to it
    await redis.set("key", "value")

if __name__ == "__main__":
    asyncio.run(main())
