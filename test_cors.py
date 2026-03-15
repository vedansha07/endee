from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload(request: Request):
    print("Received upload request headers:", request.headers)
    return {"message": "Success"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
