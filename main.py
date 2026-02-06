import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.addresses import router as address_router
from app.core.config import settings
from app.db.session import engine
from app.db.base_class import Base


from app.models.address import Address 

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    async with engine.begin() as conn:
    
        await conn.run_sync(Base.metadata.create_all)
    print(" Database tables created")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)


app.include_router(address_router, prefix="/api/v1/addresses", tags=["Addresses"])

@app.get("/")
async def root():
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "documentation": "/docs"
    }

if __name__ == "__main__":
    
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)