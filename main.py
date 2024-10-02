from fastapi import FastAPI
from routers import upload, status, video

app = FastAPI()

app.include_router(upload.router)
app.include_router(status.router)
app.include_router(video.router)