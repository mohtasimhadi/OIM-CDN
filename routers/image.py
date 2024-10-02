from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
import uuid

router = APIRouter()

IMAGE_DIRECTORY = "images/"

if not os.path.exists(IMAGE_DIRECTORY):
    os.makedirs(IMAGE_DIRECTORY)

@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    unique_id = str(uuid.uuid4())
    extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{unique_id}{extension}"
    file_path = os.path.join(IMAGE_DIRECTORY, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"image_id": unique_id}

@router.get("/view/{image_id}")
async def view_image(image_id: str):
    # Search for the image file by UUID
    matching_files = [f for f in os.listdir(IMAGE_DIRECTORY) if f.startswith(image_id)]
    if not matching_files:
        raise HTTPException(status_code=404, detail="Image not found")
    
    file_path = os.path.join(IMAGE_DIRECTORY, matching_files[0])
    return FileResponse(file_path)

@router.delete("/delete/{image_id}")
async def delete_image(image_id: str):
    # Search for the image file by UUID
    matching_files = [f for f in os.listdir(IMAGE_DIRECTORY) if f.startswith(image_id)]
    if not matching_files:
        raise HTTPException(status_code=404, detail="Image not found")
    
    file_path = os.path.join(IMAGE_DIRECTORY, matching_files[0])
    os.remove(file_path)
    return {"message": f"Image with ID '{image_id}' deleted successfully."}
