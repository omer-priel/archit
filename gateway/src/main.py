
from fastapi import FastAPI

from src.routers.client import router as client_router


app = FastAPI()

app.add_route("/client", client_router)


@app.get("/")
async def root():
    return {"message": "Gateway to Microservices"}
