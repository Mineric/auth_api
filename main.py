from fastapi import FastAPI
from app.routers import user
from app.config import settings
from app.dependicies import init_db

app = FastAPI(title=settings.APP_TITLE, description=settings.APP_DESCRIPTION, version=settings.APP_VERSION)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(user.router)

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
