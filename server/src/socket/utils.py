from fastapi import WebSocket, status, Query
from typing import Optional


async def get_token(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
):
    """Function that receives a websocket and a token, then check if the to
    token is None or null"""
    # if the token is None or empty
    if token is None or token == "":
        # return a policy violation status if available
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    # TODO: additional token validation

    # Return the token
    return token
