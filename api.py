from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from dotenv import load_dotenv
import shutil
import os 

load_dotenv()

app = FastAPI()

DATA_DIR = os.getenv("DATA_DIR")


class FileQuery(BaseModel):
    filename: str
    content_type: str
    query: str

class FileQueryResponse(BaseModel):
    success: bool
    response: str


@app.post("/upload/", response_model=FileQueryResponse)
async def upload_file(uploaded_file: UploadFile,
                      query: str = Form(...)
):
    
    # validate request
    try:
        validated_query = FileQuery(
            filename=uploaded_file.filename,
            content_type=uploaded_file.content_type,
            query=query
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    file_location = f"{DATA_DIR}/{uploaded_file.filename}"
    with open(file_location, "wb") as file:
        shutil.copyfileobj(uploaded_file.file, file)

    return {
        "success": True,
        "response": "TestResponse"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8010)