import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
from src.routers.admin_router import admin_router
import uvicorn
from fastapi import FastAPI



app = FastAPI()
app.include_router(admin_router,prefix="/api/admin",tags=['admin'])

if __name__ == '__main__':
    uvicorn.run('src.main:app', host="127.0.0.1", port=8000)

