
from fastapi import FastAPI

from gateway.routers.client import router as client_router


app = FastAPI()

# Add routers
app.add_route("/client", client_router)
app.add_websocket_route("/client", client_router)


@app.get("/")
async def root():
    return {"message": "Gateway to Microservices"}
