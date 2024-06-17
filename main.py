import os
from fastapi import FastAPI
from app.routers import user
from app.config import settings
from app.dependicies import init_db
from app.utils.exceptions import CustomHTTPException, custom_http_exception_handler
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title=settings.APP_TITLE, 
    description=settings.APP_DESCRIPTION, 
    version=settings.APP_VERSION,
)

@app.get("/", include_in_schema=False)
def read_root():
    return {"status": "200 OK", "message": "Welcome to PFN TEST"}

# @app.get("/favicon.ico")
# async def get_favicon():
#     # Adjust the path to where your favicon.ico file is located
#     favicon_path = os.path.join(os.getcwd(), "static", "favicon.ico")
#     return FileResponse(favicon_path)

app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(user.router)
# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
