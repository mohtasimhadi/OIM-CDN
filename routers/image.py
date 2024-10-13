from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
from services.image_service import initiate_image_upload, get_image_path
from fastapi import BackgroundTasks

router = APIRouter()

@router.post("/upload/")
async def upload_image(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    return await initiate_image_upload(background_tasks, file)

# @router.post("/upload/")
# async def upload_image(file: UploadFile = File(...)):
#     unique_id = str(uuid.uuid4())
#     extension = os.path.splitext(file.filename)[1]
#     unique_filename = f"{unique_id}{extension}"
#     file_path = os.path.join(IMAGE_DIRECTORY, unique_filename)
    
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
    
#     return {"image_id": unique_id}

@router.get("/view/{image_id}")
async def view_image(image_id: str):
    image_path = get_image_path(image_id)
    if not image_path:
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)

@router.delete("/delete/{image_id}")
async def delete_image(image_id: str):
    image_path = get_image_path(image_id)
    if not image_path:
        raise HTTPException(status_code=404, detail="Image not found")
    os.remove(image_path)
    return {"message": f"Image with ID '{image_id}' deleted successfully."}
