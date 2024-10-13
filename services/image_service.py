import os
import shutil
import uuid
import aiofiles
from fastapi import UploadFile, BackgroundTasks
from fastapi import UploadFile, BackgroundTasks

IMAGE_DIRECTORY = "images"

if not os.path.exists(IMAGE_DIRECTORY):
    os.makedirs(IMAGE_DIRECTORY)

async def initiate_image_upload(background_tasks: BackgroundTasks, file: UploadFile):
    unique_id = str(uuid.uuid4())
    content = await file.read()
    background_tasks.add_task(save_image, unique_id, content)
    return {'image_id': unique_id}

async def save_image(unique_id: str, content: bytes):
    unique_filename = f"{unique_id}.jpg"
    file_path = os.path.join(IMAGE_DIRECTORY, unique_filename)
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            await out_file.write(content)
    except Exception as e:
        print(e)

def get_image_path(unique_id: str):
    image_path = os.path.join(IMAGE_DIRECTORY, f"{unique_id}.jpg")
    if os.path.exists(image_path):
        return image_path
    return None