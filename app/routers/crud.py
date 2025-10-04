from fastapi import APIRouter, Request, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from routers import auth
from app.db import SessionDep
from sqlmodel import select
from pathlib import Path

from sqlmodel import Session
from app.models import User, UserLogin, UserResponse, Product, UserCreate, ProductCreate, Cart, CartCreate, Order, OrderCreate, OrderItem
# from sqlmodel import select
# from db import SessionDep

router = APIRouter()

oauth_scheme = OAuth2PasswordBearer(tokenUrl = "login")

## INDICA DONDE SE VAN A ENCONTRAR LAS PLANTILLAS HTML
# Las plantillas se encuentran en app/backend/templates (un nivel por encima de los enrutadores)
templates_dir = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

@router.post("/register", response_model="UserResponse")
async def UserCreate(session: SessionDep, user_data : UserCreate):

    statament = select(User).where(User.username == user_data.username)
    existing_user = session.exec(statament).first()

    if existing_user:
        raise HTTPException(status_code= 400, detail = "El usuario ya existe")

    hashed_pw = auth.hash_password(user_data.password)

    new_user = User(
        username = user_data.username,
        email = user_data.email,
        hashed_password= hashed_pw
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


