from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Any, Optional, Dict

class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: dict):
        super().__init__(status_code=status_code, detail=detail)

async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )

