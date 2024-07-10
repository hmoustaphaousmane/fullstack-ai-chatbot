# Import required libraries
from fastapi import FastAPI, Request
import uvicorn
import os
from dotenv import load_dotenv, find_dotenv

from routes.chat import chat

# Find .env and load  variables from it
_ = load_dotenv(find_dotenv())

# Initialize FastAPI as api
api = FastAPI()

# connect chat router to the main API
api.include_router(chat)

# test route
@api.get("/test")
async def root():
    """Route that will return a simple JSON response"""
    return {"msg": "API is Online"}


if __name__ == "__main__":
    if os.getenv('APP_ENV') == "development":
        # set up development server
        uvicorn.run(
            "main:api", host="0.0.0.0", port=3500, workers=4, reload=True
        )
    else:
        pass
