from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.features.tasks.routes import router as tasks_router

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


app.include_router(tasks_router)