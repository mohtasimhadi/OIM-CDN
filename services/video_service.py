import os
import shutil
import uuid
import aiofiles
from typing import Dict
from fastapi import UploadFile, BackgroundTasks
import ffmpeg

VIDEO_STORAGE = "videos"
TEMP_STORAGE  = 'temp_videos'
os.makedirs(VIDEO_STORAGE, exist_ok=True)
os.makedirs(TEMP_STORAGE, exist_ok=True)

upload_status: Dict[str, str] = {}

async def initiate_video_upload(background_tasks: BackgroundTasks, file: UploadFile):
    unique_id = str(uuid.uuid4())
    upload_status[unique_id] = "in progress"
    content = await file.read()
    background_tasks.add_task(save_video, unique_id, content)
    return {"unique_id": unique_id}

async def save_video(unique_id: str, content: bytes):
    video_path = os.path.join(VIDEO_STORAGE, f"{unique_id}.mp4")
    try:
        async with aiofiles.open(video_path, 'wb') as out_file:
            await out_file.write(content)
            compress_video(video_path)
        upload_status[unique_id] = "completed"
    except Exception as e:
        print(e)
        upload_status[unique_id] = "failed"

def get_upload_status(unique_id: str):
    return upload_status.get(unique_id)

def get_video_path(unique_id: str):
    video_path = os.path.join(VIDEO_STORAGE, f"{unique_id}.mp4")
    if os.path.exists(video_path):
        return video_path
    return None


def delete_video_file(unique_id: str):
    video_path = os.path.join(VIDEO_STORAGE, f"{unique_id}.mp4")
    if os.path.exists(video_path):
        os.remove(video_path)
        upload_status.pop(unique_id, None)
        return True
    return False

def get_video_size(video_path):
    probe = ffmpeg.probe(video_path)
    file_size = int(probe['format']['size'])
    return file_size / (1024 * 1024)

def get_video_duration(video_path):
    probe = ffmpeg.probe(video_path)
    duration = float(probe['format']['duration'])
    return duration

def compress(video_full_path, output_file_name, target_size):
    probe = ffmpeg.probe(video_full_path)
    duration = float(probe['format']['duration'])
    target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

    video_bitrate = target_total_bitrate

    i = ffmpeg.input(video_full_path)
    ffmpeg.output(i, os.devnull,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                  ).overwrite_output().run()
    ffmpeg.output(i, output_file_name,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac'}
                  ).overwrite_output().run()

def compress_video(video_path):
    if get_video_size(video_path) > 100.00:
        duration = get_video_duration(video_path)
        temp_output = video_path.replace(VIDEO_STORAGE, TEMP_STORAGE)
        compress(video_path, temp_output, (32000 + 100000) * (50.073741824 * duration) / (8 * 1024))
        replace_file(temp_output, video_path)

def replace_file(source, destination):
    shutil.move(source, destination)