from fastapi import FastAPI
from .routers import file_query

app = FastAPI()
app.include_router(file_query.router)

@app.get("/")
async def root():
    return {"message": "Hello, try file_query endpoint"}


