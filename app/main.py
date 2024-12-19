from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Dental Products Scraper")
app.include_router(router, prefix="/api")
