import socket
from fastapi import FastAPI
from routers import image, video

app = FastAPI()
app.include_router(image.router, prefix="/image")
app.include_router(video.router, prefix="/video")

if __name__ == "__main__":
    import uvicorn
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"App is accessible at: http://{local_ip}:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
