from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from services.video_service import get_video_path, delete_video_file

router = APIRouter()

@router.get("/video/{unique_id}")
async def get_video(unique_id: str):
    video_path = get_video_path(unique_id)
    if not video_path:
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(video_path)

@router.delete("/video/{unique_id}")
async def delete_video(unique_id: str):
    if not delete_video_file(unique_id):
        raise HTTPException(status_code=404, detail="Video not found")
    return {"detail": "Video deleted successfully"}
