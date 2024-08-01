from .config import MyRedis

class StreamConsumer:

    
    def __init__(self, redis_client):
        self.redice_client = redis_client

    async def consume_stream(self, count: int, block: int, stream_channel):
        response = await self.redice_client.xread(
            streams={stream_channel: '0-0'}, count=count, block=block
        )

        return response

    async def delete_message(self, stream_channel, message_id):
        await self.redice_client.xdel(stream_channel, message_id)
    