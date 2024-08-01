class Cache:

    
    def __init__(self, json_cient):
        self.json_client = json_cient

    async def get_chat_history(self, token: str):
        data = self.json_client.get(str(token))

        return data
    