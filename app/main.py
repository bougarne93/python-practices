from fastapi import FastAPI
from app.api.routes import router as api_router
from app.api.routes_sql import router as sql_router
from app.api.routes_auth import router as auth_router

""" app = FastAPI(
    title="Learning Backend API",
    description="API Python Backend Training",
    version="1.0.0",
) """

# Attach the API router
#app.include_router(api_router)
app = FastAPI()
app.include_router(sql_router)
app.include_router(auth_router)