from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.engine import get_engine
from controller import user_controller, login_controller


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_engine()
    yield
    print("Server's down")

app = FastAPI(lifespan=lifespan)
app.include_router(user_controller.router)
app.include_router(login_controller.router)


@app.get("/")
def test_home():
    return {"is_everything": "ok"}
