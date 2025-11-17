from fastapi import FastAPI
from routers.admin_router import admin_router

app = FastAPI()
app.include_router(admin_router,prefix="/api/admin",tags=['admin'])
