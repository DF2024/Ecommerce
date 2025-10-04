from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import relationship
from pydantic import EmailStr
from typing import Optional, ClassVar, List
from enum import Enum


# -----------------------------
# ENUM ROLES
# -----------------------------
class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


# -----------------------------
# USUARIOS
# -----------------------------
class UserBase(SQLModel):
    username: str
    email: EmailStr


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    role: UserRole = Field(default=UserRole.CUSTOMER)

    # Relaciones
    orders: ClassVar[List["Order"]] = relationship("Order", back_populates="user")
    cart_items: ClassVar[List["Cart"]] = relationship("Cart", back_populates="user")


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int


class UserLogin(SQLModel):
    username: str
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str


# -----------------------------
# PRODUCTOS
# -----------------------------
class ProductBase(SQLModel):
    name: str
    description: str
    price: float
    stock: int
    image_url: Optional[str] = None


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relaciones
    cart_items: ClassVar[List["Cart"]] = relationship("Cart", back_populates="product")
    order_items: ClassVar[List["OrderItem"]] = relationship("OrderItem", back_populates="product")


class ProductCreate(ProductBase):
    pass


# -----------------------------
# CARRITO
# -----------------------------
class CartBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int


class Cart(CartBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relaciones
    user: ClassVar["User"] = relationship("User", back_populates="cart_items")
    product: ClassVar["Product"] = relationship("Product", back_populates="cart_items")


class CartCreate(CartBase):
    pass


# -----------------------------
# ÓRDENES
# -----------------------------
class OrderBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    total: float


class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relaciones
    user: ClassVar["User"] = relationship("User", back_populates="orders")
    items: ClassVar[List["OrderItem"]] = relationship("OrderItem", back_populates="order")


class OrderCreate(OrderBase):
    pass


# -----------------------------
# ITEMS DE ÓRDEN
# -----------------------------
class OrderItemBase(SQLModel):
    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    price: float


class OrderItem(OrderItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relaciones
    order: ClassVar["Order"] = relationship("Order", back_populates="items")
    product: ClassVar["Product"] = relationship("Product", back_populates="order_items")
