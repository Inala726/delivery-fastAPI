from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from enum import Enum


# ---------- AUTH ----------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: 'UserResponse'


# ---------- ENUMS ----------
class UserRole(str, Enum):
    customer = "customer"
    driver = "driver"
    restaurant_owner = "restaurant_owner"
    admin = "admin"


class OrderStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    preparing = "preparing"
    on_the_way = "on_the_way"
    delivered = "delivered"
    cancelled = "cancelled"


# ---------- USER ----------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[UserRole] = UserRole.customer


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
    image_url: Optional[str] = None


class MenuItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    image_url: Optional[str]
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
