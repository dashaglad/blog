from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.db import engine, Base
from app.api.posts import router as posts_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(posts_router)


@app.get("/health")
def health():
    return {"status": "ok"}
