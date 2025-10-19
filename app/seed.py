# seed.py
import bcrypt
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import DATABASE_URL  # Adjust if your DB URL is defined elsewhere
from app.models import Base, User, Driver, Restaurant, MenuItem, OrderItem, Order  # Import your SQLAlchemy models
from app.schemas import UserRole, OrderStatus  # For enums

# Setup database connection (mirroring your app/database.py)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def seed_data():
    db = SessionLocal()
    try:
        # Optional: Drop and recreate tables (dev only; deletes all data!)
        # Base.metadata.drop_all(bind=engine)
        # Base.metadata.create_all(bind=engine)

        # Step 1: Seed Users (different roles)
        if db.query(User).count() == 0:  # Check to avoid duplicates
            users = [
                User(
                    name="Admin User",
                    email="admin@example.com",
                    password=hash_password("adminpass123"),
                    role=UserRole.admin,
                    is_active=True
                ),
                User(
                    name="Restaurant Owner",
                    email="owner@example.com",
                    password=hash_password("ownerpass123"),
                    role=UserRole.restaurant_owner,
                    is_active=True
                ),
                User(
                    name="Customer",
                    email="customer@example.com",
                    password=hash_password("customerpass123"),
                    role=UserRole.customer,
                    is_active=True
                ),
                User(
                    name="Driver",
                    email="driver@example.com",
                    password=hash_password("driverpass123"),
                    role=UserRole.driver,
                    is_active=True
                ),
            ]
            db.add_all(users)
            db.commit()
            print("Seeded 4 users.")

        # Refresh to get IDs
        db.refresh(users[0])
        db.refresh(users[1])
        db.refresh(users[2])
        db.refresh(users[3])

        admin_id = users[0].id
        owner_id = users[1].id
        customer_id = users[2].id
        driver_user_id = users[3].id

        # Step 2: Seed Driver (linked to driver user)
        if db.query(Driver).count() == 0:
            driver = Driver(
                user_id=driver_user_id,
                is_available=True
            )
            db.add(driver)
            db.commit()
            db.refresh(driver)
            print(f"Seeded driver with ID {driver.id}.")

        driver_id = driver.id  # Note: This is the Driver model's ID, not user_id

        # Step 3: Seed Restaurant (linked to owner)
        if db.query(Restaurant).count() == 0:
            restaurant = Restaurant(
                name="Sample Pizza Place",
                address="123 Main St, Cityville",
                is_open=True,
                owner_id=owner_id
            )
            db.add(restaurant)
            db.commit()
            db.refresh(restaurant)
            print(f"Seeded restaurant with ID {restaurant.id}.")

        restaurant_id = restaurant.id

        # Step 4: Seed Menu Items (linked to restaurant)
        if db.query(MenuItem).count() == 0:
            menu_items = [
                MenuItem(
                    name="Margherita Pizza",
                    description="Classic cheese pizza",
                    price=12.99,
                    restaurant_id=restaurant_id,
                    # image_url="https://example.com/pizza.jpg"
                ),
                MenuItem(
                    name="Pepperoni Pizza",
                    description="Pizza with pepperoni slices",
                    price=14.99,
                    restaurant_id=restaurant_id,
                    # image_url="https://example.com/pepperoni.jpg"
                ),
            ]
            db.add_all(menu_items)
            db.commit()
            print("Seeded 2 menu items.")

        # Refresh to get IDs
        db.refresh(menu_items[0])
        db.refresh(menu_items[1])

        # Step 5: Seed Order with Items (linked to customer, restaurant, driver)
        if db.query(Order).count() == 0:
            # Create order items first (they'll be associated via relationship)
            order_items = [
                OrderItem(
                    menu_item_id=menu_items[0].id,
                    quantity=1
                ),
                OrderItem(
                    menu_item_id=menu_items[1].id,
                    quantity=2
                ),
            ]

            # Calculate total price (you may have logic for this in your app; hardcoding here)
            total_price = (menu_items[0].price * 1) + (menu_items[1].price * 2)

            order = Order(
                customer_id=customer_id,
                restaurant_id=restaurant_id,
                driver_id=driver_id,  # Optional; assign a driver
                total_price=total_price,
                status=OrderStatus.pending,
                created_at=datetime.utcnow(),
                items=order_items  # Assuming your Order model has a relationship to OrderItem
            )
            db.add(order)
            db.commit()
            db.refresh(order)
            print(f"Seeded order with ID {order.id} and 2 items.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()