from fastapi import APIRouter, UploadFile, BackgroundTasks
from services.video_service import initiate_video_upload

router = APIRouter()

@router.post("/upload/")
async def initiate_upload(background_tasks: BackgroundTasks, file: UploadFile):
    return await initiate_video_upload(background_tasks, file)