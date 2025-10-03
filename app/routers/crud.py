import uvicorn
from fastapi import APIRouter, Request, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
# from sqlmodel import select
# from db import SessionDep

router = APIRouter()

## INDICA DONDE SE VAN A ENCONTRAR LAS PLANTILLAS HTML
# Las plantillas se encuentran en app/backend/templates (un nivel por encima de los enrutadores)
templates_dir = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

@router.get("/hola", response_class = HTMLResponse)
async def home(request : Request):
    ## RENDERIZA LAS PLANTILLAS HTML
    return templates.TemplateResponse(
        "index.html",#LLAMA A LA PLANTILLA 
        {"request": request, "name": "Andrés"}
    )