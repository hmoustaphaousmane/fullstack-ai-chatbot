import json

from .config import MyRedis

class Cache:
    def __init__(self, json_client=None):
        if json_client is None:
            self.json_client = MyRedis().create_rejson_connection()
        else:
            self.json_client = json_client

    async def get_chat_history(self, token: str):
        data = self.json_client.get(str(token))

        chat_session = json.loads(data)
        return chat_session
