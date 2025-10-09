from datetime import datetime
import enum
from sqlalchemy import Boolean, Column, DateTime, Enum, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class UserRole(enum.Enum):
    CUSTOMER = "customer"
    DRIVER = "driver"
    RESTAURANT_OWNER = "restaurant_owner"
    ADMIN = "admin"

class OrderStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    PREPARING = "preparing"
    ON_THE_WAY = "on_the_way"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    is_active = Column(Boolean, default=True)  # customer | restaurant | driver | admin
    
    restaurants = relationship("Restaurant", back_populates="owner")
    orders = relationship("Order", back_populates="customer")

class Restaurant(Base):
    __tablename__ = 'restaurants'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    is_open = Column(Boolean, default=True)   

    owner = relationship("User", back_populates="restaurants")
    menus = relationship("MenuItem", back_populates="restaurant")
    orders = relationship("Order", back_populates="restaurant")

class MenuItem(Base):
    __tablename__ = 'menu_items'
    
    id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey("users.id"))
    restaurant_id = Column(String, ForeignKey("restaurants.id"))
    driver_id = Column(String, ForeignKey("drivers.id"), nullable=True)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("User", back_populates="orders")
    restaurant = relationship("Restaurant", back_populates="orders")
    driver = relationship("Driver", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey("users.id"))
    restaurant_id = Column(String, ForeignKey("restaurants.id"))
    driver_id = Column(String, ForeignKey("drivers.id"), nullable=True)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("User", back_populates="orders")
    restaurant = relationship("Restaurant", back_populates="orders")
    driver = relationship("Driver", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String, primary_key=True, index=True)
    order_id = Column(String, ForeignKey("orders.id"))
    menu_item_id = Column(String, ForeignKey("menu_items.id"))
    quantity = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    is_available = Column(Boolean, default=True)

    user = relationship("User")
    orders = relationship("Order", back_populates="driver")
