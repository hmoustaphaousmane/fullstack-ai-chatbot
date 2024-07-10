from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # list of active connections
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Method that accepts a Websocket and add it to the list of active
        connections"""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove the provided Websockt from the list of active connections"""
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send asychronously message to websocket"""
        await websocket.send_text(message)
