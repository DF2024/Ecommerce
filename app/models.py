from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from datetime import datetime

class formulario(SQLModel):
    username : str
    email : EmailStr
    



