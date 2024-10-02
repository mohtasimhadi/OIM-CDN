from fastapi import APIRouter, HTTPException
from services.video_service import get_upload_status

router = APIRouter()

@router.get("/status/{unique_id}")
async def get_status(unique_id: str):
    status = get_upload_status(unique_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return {"unique_id": unique_id, "status": status}
