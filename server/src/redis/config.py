import os
from rejson import Client
from redis import asyncio as aioredis
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


class Redis():
    def __init__(self) -> None:
        """initialize connection"""
        self.REDIS_URL = os.getenv('REDIS_URL')
        self.REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
        self.REDIS_USER = os.getenv('REDIS_USER')
        self.connection_url = f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_URL}"

    async def create_connection(self):
        """Method that create a Redis connection"""
        # try:
        self.connection = aioredis.from_url(
            self.connection_url, db=0
        )
        # except TimeoutError:
        #    pass

        # Return the connection pool
        return self.connection

    def create_rejson_connection(self):
        """Method that allows to connect Redis with the rejson Client thus to
        manipulate JSON data in Redis, which are not available in aioredis"""
        self.redisJson = Client(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            decode_response=True,
            username=self.REDIS_USER,
            password=self.REDIS_PASSWORD
        )

        return self.redisJson
