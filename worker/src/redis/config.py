import os
import aioredis
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


class Redis():
    def __init__(self):
        """initialize connection"""
        self.REDIS_URL = os.getenv('REDIS_URL')
        self.REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
        self.REDIS_USER = os.getenv('REDIS_USER')
        self.connection_url = f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_URL}"

    async def create_connection(self):
        """Method that create a Redis connection"""
        self.connection = aioredis.from_url(
            self.connection_url, db=0
        )

        # Return the connection pool
        return self.connection
