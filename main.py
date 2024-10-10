import socket
from fastapi import FastAPI
from routers import image, video

app = FastAPI()
app.include_router(image.router, prefix="/image")
app.include_router(video.router, prefix="/video")

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    import uvicorn
    local_ip = get_local_ip()
    print(f"\033[92mINFO:  \t\033[0m  App is accessible at: \033[94mhttp://{local_ip}:8000\033[0m")
    uvicorn.run(app, host="0.0.0.0", port=8000)
