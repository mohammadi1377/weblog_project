from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from .auth import template

router = APIRouter(
    tags=["Root"]
)


# BASE_PATH = Path(__file__).resolve().parent
# TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "Template"))
@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return template.TemplateResponse(
        "root.html",
        {"request": request},
    )
