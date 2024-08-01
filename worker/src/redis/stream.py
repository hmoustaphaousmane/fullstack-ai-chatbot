
class StreamConsumer:

    def __init__(self, redis_client):
        self.redis_client = redis_client  # initialize a redis client

    async def consume_stream(self, count: int, block: int, stream_channel):
        """
        Methode that pulls a new message from the queue from the message
        channel using the `xread` method provided by aioredis
        """
        response = await self.redis_client.xread(
            streams={stream_channel: '0-0'}, count=count, block=block
        )

        return response

    async def delete_message(self, stream_channel, message_id):
        await self.redis_client.xdel(stream_channel, message_id)
