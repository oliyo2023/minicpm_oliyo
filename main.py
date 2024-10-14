import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import store

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
async def root():
    # Serve an index.html file from the static directory
    return FileResponse('static/index.html')
@app.get("/api")
async def api():
    return {"message": "Hello API"}

# Add a 404 handler for static files
@app.exception_handler(404)
async def custom_404_handler(request, exc):
    return FileResponse('static/404.html')
# Add a 500 handler for static files
@app.exception_handler(500)
async def custom_500_handler(request, exc):
    return FileResponse('static/500.html')
# Add CORS middleware if needed
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# 添加WebSocket路由
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async def listen_for_changes():
        # 订阅PocketBase的实时更新
        async for event in store.pb.realtime.subscribe("*"):  # 订阅所有集合，您可以根据需要指定特定集合
            # 将PocketBase的实时事件通过WebSocket发送给客户端
            await websocket.send_json(event)

    try:
        await listen_for_changes()
    except Exception as e:
        print(f"WebSocket连接关闭: {e}")
    finally:
        store.pb.realtime.unsubscribe("*")

#add a route to get api key
@app.get("/api/key")
async def get_api_key(platform: str):
    return {"api_key": store.getApiKeyByPlatform(platform)}

# 实时订阅PocketBase集合变化
# async def subscribe_to_changes():
#     def on_change(e):
#         print(f"Change detected: {e.action} {e.record}")
#         # 这里可以添加将变化推送到WebSocket客户端的逻辑

#     store.pb.collection('chat').subscribe( on_change)

# # 启动实时订阅
# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(subscribe_to_changes())
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)