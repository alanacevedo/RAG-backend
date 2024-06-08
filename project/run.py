from dotenv import load_dotenv
load_dotenv()

import os
from app.main import app

HOST_URL = os.getenv("HOST_URL")
PORT = int(os.getenv("PORT"))

print(HOST_URL, PORT)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST_URL, port=PORT)