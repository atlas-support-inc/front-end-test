import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


ws_router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, user_id, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        await self.send_online_user()

    async def disconnect(self, user_id):
        if self.active_connections.get(user_id):
            del self.active_connections[user_id]
        await self.send_online_user()

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

    async def send_online_user(self):
        await self.broadcast(
            json.dumps(
                {'online_users': list(self.active_connections.keys())}
            )
        )

    async def send_new_chat(self, user_id):
        if self.active_connections.get(user_id):
            websocket = self.active_connections[user_id]
            await websocket.send_text(json.dumps({
                'new_chat': True,
            }))


manager = ConnectionManager()


@ws_router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
    except WebSocketDisconnect:
        manager.disconnect(user_id)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = 2
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                console.log(event)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@ws_router.get("/test_ws")
async def get():
    return HTMLResponse(html)
