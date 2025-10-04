

from fastapi import FastAPI, Request
from sqlmodel import select

from routers import crud
from db import SessionDep, lifespan


app = FastAPI(
    lifespan=lifespan
)

app.include_router(crud.router)