from fastapi import FastAPI
from routers import image
from routers import video

app = FastAPI()
app.include_router(image.router, prefix="/image")
app.include_router(video.router, prefix="/video")