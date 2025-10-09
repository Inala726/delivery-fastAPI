from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from enum import Enum


# ---------- ENUMS ----------
class UserRole(str, Enum):
    CUSTOMER = "customer"
    DRIVER = "driver"
    RESTAURANT_OWNER = "restaurant_owner"
    ADMIN = "admin"


class OrderStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    PREPARING = "preparing"
    ON_THE_WAY = "on_the_way"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# ---------- USER ----------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[UserRole] = UserRole.CUSTOMER


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool

    class Config:
        orm_mode = True


# ---------- DRIVER ----------
class DriverCreate(BaseModel):
    user_id: str


class DriverResponse(BaseModel):
    id: str
    user_id: str
    is_available: bool

    class Config:
        orm_mode = True


# ---------- RESTAURANT ----------
class RestaurantCreate(BaseModel):
    name: str
    address: str
    owner_id: int


class RestaurantResponse(BaseModel):
    id: int
    name: str
    address: str
    is_open: bool
    owner_id: int

    class Config:
        orm_mode = True


# ---------- MENU ITEM ----------
class MenuItemCreate(BaseModel):
    name: str
    description: Optional[str]
    price: float
    restaurant_id: int


class MenuItemResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    price: float
    restaurant_id: int

    class Config:
        orm_mode = True


# ---------- ORDER ITEM ----------
class OrderItemCreate(BaseModel):
    menu_item_id: str
    quantity: float


class OrderItemResponse(BaseModel):
    id: str
    order_id: str
    menu_item_id: str
    quantity: float

    class Config:
        orm_mode = True


# ---------- ORDER ----------
class OrderCreate(BaseModel):
    customer_id: str
    restaurant_id: str
    items: List[OrderItemCreate]


class OrderResponse(BaseModel):
    id: str
    customer_id: str
    restaurant_id: str
    driver_id: Optional[str]
    total_price: float
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True
