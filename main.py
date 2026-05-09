from fastapi import FastAPI, Request
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse

from app.features.auth.routes import router as auth_router
from app.features.tasks.routes import router as tasks_router

app = FastAPI()


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Something went wrong. Please try again."},
    )


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


app.include_router(auth_router)
app.include_router(tasks_router)
