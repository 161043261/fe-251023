from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .router.controllers import router as api_router
from .router.webhooks import router as webhooks_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=["*"],
)

app.include_router(api_router, prefix="/api")
app.include_router(webhooks_router, prefix="/webhooks")
