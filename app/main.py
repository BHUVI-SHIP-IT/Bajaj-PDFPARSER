from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="HackRx Query System",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "HackRx Query System is running."}