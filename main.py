from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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
async def websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        await websocket.send_text(f"Received: {message}")

