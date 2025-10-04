from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from fastapi.templating import Jinja2Templates
from app.routers import crud
from app.db import lifespan

app = FastAPI(lifespan=lifespan)

# Configuración de archivos estáticos (ruta relativa)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory="app/templates")

# Routers
app.include_router(crud.router)