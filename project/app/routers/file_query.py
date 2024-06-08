from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.file_query import FileQuery, FileQueryResponse
import shutil
import os 

DATA_DIR = os.getenv("DATA_DIR")


router = APIRouter()

@router.post("/file_query/", response_model=FileQueryResponse)
async def file_query(uploaded_file: UploadFile,
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
