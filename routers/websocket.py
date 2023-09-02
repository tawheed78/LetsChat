

# from datetime import datetime
# from fastapi import WebSocket, WebSocketDisconnect
# from main import app, manager

# @app.websocket("/ws/{username}")
# async def websocket_endpoint(websocket: WebSocket, username:str):
#     await manager.connect(websocket)
#     now = datetime.now()
#     current_time = now.strftime("%H:%M")

#     try:
#         while True:
#             data = await websocket.receive_text()
#             message = {"time": current_time, "username":username, "message": data }
#             await manager.broadcast(message)

#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         message = {"time": current_time, "username":username, "message": "Offline" }
#         await manager.broadcast(message)