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
        from_attributes = True


# ---------- DRIVER ----------
class DriverCreate(BaseModel):
    user_id: int


class DriverResponse(BaseModel):
    id: int
    user_id: int
    is_available: bool

    class Config:
        from_attributes = True


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
        from_attributes = True


# ---------- MENU ITEM ----------
class MenuItemCreate(BaseModel):
    name: str
    description: Optional[str]
    price: float
    restaurant_id: int


class MenuItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    restaurant_id: int

    class Config:
        from_attributes = True


# ---------- ORDER ITEM ----------
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: float


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    menu_item_id: int
    quantity: float

    class Config:
        from_attributes = True


# ---------- ORDER ----------
class OrderCreate(BaseModel):
    customer_id: int
    restaurant_id: int
    items: List[OrderItemCreate]


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    restaurant_id: int
    driver_id: Optional[int]
    total_price: float
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
