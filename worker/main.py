import os
import asyncio

from src.redis.config import MyRedis
from src.redis.cache import Cache
from src.redis.stream import StreamConsumer
from src.model.gptj import GPT
from src.schema.chat import Message

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# initialize Redis
redis = MyRedis()


async def main():
    # create a rejon connection
    json_client = redis.create_rejson_connection()

    redis_client = await redis.create_connection()
    consumer = StreamConsumer(redis_client)
    cache = Cache(json_client)

    print("Stream consumer started")
    print("Stream waiting for new messages")

    # infinite loop to keep the connection to the message channel alive
    while True:
        # await for new messages from the message channel
        response = await consumer.consume_stream(
            stream_channel="message_channel", count=1, block=0
        )

        # if we have a message in the queue
        if response:
            for stream, messages in response:
                # get message from stream
                for message in messages:
                    # extract the message id
                    message_id = message[0]

                    # extract the token
                    token = [
                        k.decode('utf-8') for k, v in message[1].items()
                    ][0]

                    # extract the message
                    message = [
                        v.decode('utf-8') for k,v in message[1].items()
                    ][0]

                    print(token)

                    # create a new message instance
                    msg = Message(msg=message)

                    # add the message to the cache specifying the source human
                    await cache.add_message_to_cache(
                        token=token, source="human", message_data=dict(msg)
                    )

                    # get chat history from cache
                    data = await cache.get_chat_history(token=token)

                    # get the last 4 messages
                    message_data = data['message'][-4]

                    # clean message input and send to query
                    input = ["" + i['msg'] for i in message_data]
                    input = " ".join(input)

                    res = GPT().query(input=input)

                    # create a new Message for the bot response
                    bot_msg = Message(msg=res)
                    print(bot_msg)

                    # add the bot response to the cache specifying the source as "bot"
                    await cache(json_client).add_message_to_cache(
                        token=token, source="bot", message_data=dict(bot_msg)
                    )
                
                # delete the message from queue after it has been processed
                await consumer.delete_message(
                    stream_channel="message_channel", message_id=message_id
                )

if __name__ == "__main__":
    asyncio.run(main())
