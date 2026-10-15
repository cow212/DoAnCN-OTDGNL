"""Entry point - Clean Architecture bootstrap."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from presentation.middleware.path import LowercasePathMiddleware
from presentation.routers.auth import router as auth_router
from presentation.routers.questions import router as questions_router
from presentation.routers.exam import router as exam_router

app = FastAPI(
    title="OnThiDGNL API (Python - Clean Architecture)",
    description="Port 1:1 logic của API .NET sang Python, tổ chức Clean Architecture.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LowercasePathMiddleware)

app.include_router(auth_router, prefix="/api")
app.include_router(questions_router, prefix="/api")
app.include_router(exam_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "OnThiDGNL Python API (Clean Architecture) is running", "docs": "/docs"}
