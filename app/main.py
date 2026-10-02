from fastapi import FastAPI

from app.api.auth import router as auth_router

app = FastAPI(
    title="Multi-Vendor Ecommerce Backend",
    version="1.0.0",
)

app.include_router(auth_router)

