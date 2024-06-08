from pydantic import BaseModel

class FileQuery(BaseModel):
    filename: str
    content_type: str
    query: str

class FileQueryResponse(BaseModel):
    success: bool
    response: str