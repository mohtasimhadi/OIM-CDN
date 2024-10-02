# Video CDN API

## Project Structure

```
oim-cdn/
│
├── main.py
├── readme.md
├── requirements.txt
├── routers/
│   ├── upload.py
│   ├── status.py
│   ├── video.py
│
└── services/
    └── video_service.py

```

- main.py: Entry point for the application.
- routers/: Contains route definitions for uploading, checking status, retrieving, and deleting videos.
- services/: Contains the business logic for handling video uploads and file operations.

## Installation

**1. Clone the Repository**
```{bash}
git clone <>
cd OIM-CDN
```

**2. Create a Virtual Environment (Optional)**
```{Python}
python -m venv env
```

**3. Activate the Virtual Environment**
- Windows
```{bash}
.\env\Scripts\activate
```
- Linux/MacOS
```{bash}
source env/bin/activate
```

**4. Install Dependencies**
```{bash}
pip install requirements.txt
```

## Running the Application
To start the application run the following command:
```{bash}
uvicorn main:app --reload
```

- The application will be available at `http://127.0.0.1:8000`
- The `--reload` flag automatically restarts the server when change is made in the code.

## Endpoints

### 1. Upload Video

- **Endpoint**: `/upload/`
- **Method**: `POST`
- **Description**: Upload a video and get a unique ID.
- **Request**:
  - Form data: `file` (the video file to be uploaded)
- **Response**:
  ```json
  {
    "unique_id": "generated-unique-id"
  }
  ```

**Example Using cURL**:

```bash
curl -X POST "http://127.0.0.1:8000/upload/" -F "file=@/path/to/your/video.mp4"
```

**Example Using Python**:

```python
import requests

url = "http://127.0.0.1:8000/upload/"
file_path = "/path/to/your/video.mp4"

with open(file_path, "rb") as file:
    response = requests.post(url, files={"file": file})

print(response.json())
```

### 2. Get Upload Status

- **Endpoint**: `/status/{unique_id}`
- **Method**: `GET`
- **Description**: Check the current status of the video upload (`in progress`, `completed`, or `failed`).
- **Request Parameter**:
  - `{unique_id}`: The unique ID provided when uploading the video.
- **Response**:
  ```json
  {
    "unique_id": "generated-unique-id",
    "status": "completed"
  }
  ```

**Example Using cURL**:

```bash
curl "http://127.0.0.1:8000/status/{unique_id}"
```

Replace `{unique_id}` with the actual unique ID.

### 3. Get Video by Unique ID

- **Endpoint**: `/video/{unique_id}`
- **Method**: `GET`
- **Description**: Retrieve the video using the unique ID.
- **Request Parameter**:
  - `{unique_id}`: The unique ID of the video to retrieve.
- **Response**: Returns the video file if found.

**Example Using cURL**:

```bash
curl -O "http://127.0.0.1:8000/video/{unique_id}"
