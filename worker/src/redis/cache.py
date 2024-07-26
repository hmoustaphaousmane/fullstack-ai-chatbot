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

    async def add_message_to_cache(self, token: str, message_data: dict):
        # fetch the existing chat session
        data = self.json_client.get(str(token))
        if data is None:
            raise ValueError("Chat session not found for the given token.")
        
        chat_session = json.loads(data)
        print(chat_session)

        # sdd the new message to the list of messages
        chat_session['messages'].append(message_data)

        # store the updated chat session back into the cache
        self.json_client.set(str(token), json.dumps(chat_session))

        return 
