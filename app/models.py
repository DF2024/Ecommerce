from __future__ import annotations

from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from typing import Optional, List
from enum import Enum

## USUARIOS

class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"

class UserBase(SQLModel):
    username : str
    email : EmailStr


class User(UserBase, table = True):
    id : Optional[int] = Field(default = None, primary_key = True)
    hashed_password : str
    role : UserRole = Field(default=UserRole.CUSTOMER)
    orders : List["Order"] = Relationship(back_populates="user")
    ## RELACIÓN CON PRODUCTOS

class UserCreate(UserBase):
    password : str

class UserResponse(UserBase):
    id : int

class UserLogin(SQLModel):
    username : str
    password : str

class Token(SQLModel):
    access_token : str
    token_type : str

## PRODUCTOS

class ProductBase(SQLModel):
    name: str
    description: str
    price: float
    stock: int
    image_url: Optional[str] = None

class Product(ProductBase, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ProductCreate(ProductBase):
    pass

## Carrito

class CartBase(SQLModel):
    user_id : int = Field(foreign_key="user.id")
    product_id : int = Field(foreign_key="product.id")
    quantity: int

class Cart(CartBase, table = True):
    id : Optional[int] = Field(default=None, primary_key=True)
    user : "User" = Relationship()
    product : "Product" = Relationship()

class CartCreate(CartBase):
    pass


## ORDEN

class OrderBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    total: float

class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: "User" = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")

class OrderCreate(OrderBase):
    pass

class OrderItemBase(SQLModel):
    order_id : int = Field(foreign_key="order.id")
    product_id : int = Field(foreign_key="product.id")
    quantity : int
    price: float

class OrderItem(OrderItemBase, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order: "Order" = Relationship(back_populates="items")
    product: "Product" = Relationship()