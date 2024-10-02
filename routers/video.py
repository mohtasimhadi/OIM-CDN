from fastapi import APIRouter, HTTPException
from services.video_service import get_upload_status
from fastapi import APIRouter, UploadFile, BackgroundTasks
from services.video_service import initiate_video_upload
from fastapi.responses import FileResponse
from services.video_service import get_video_path, delete_video_file

router = APIRouter()

@router.get("/view/{unique_id}")
async def get_video(unique_id: str):
    video_path = get_video_path(unique_id)
    if not video_path:
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(video_path)

@router.delete("/delete/{unique_id}")
async def delete_video(unique_id: str):
    if not delete_video_file(unique_id):
        raise HTTPException(status_code=404, detail="Video not found")
    return {"detail": "Video deleted successfully"}

@router.get("/status/{unique_id}")
async def get_status(unique_id: str):
    status = get_upload_status(unique_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return {"unique_id": unique_id, "status": status}

@router.post("/upload/")
async def initiate_upload(background_tasks: BackgroundTasks, file: UploadFile):
    return await initiate_video_upload(background_tasks, file)