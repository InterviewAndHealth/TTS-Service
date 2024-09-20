from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from utils import init, ClientConnection


@asynccontextmanager
async def lifespan(app: FastAPI):
    init()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/tts")
async def tts(request: Request, text: str = Query(...)):
    """Handle text-to-speech requests."""
    client = ClientConnection()
    return client.handle(request, text)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
