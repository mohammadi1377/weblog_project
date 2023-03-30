from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from .auth import template

router = APIRouter(
    tags=["Root"]
)


@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return template.TemplateResponse(
        "root.html",
        {"request": request},
    )
