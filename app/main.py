from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app import models, database
from routes import user_routes, restaurant_routes, menu_item_routes, order_routes, driver_routes, auth_router


# Create all tables at startup
models.Base.metadata.create_all(bind=database.engine)

# Initialize FastAPI app
app = FastAPI(title="Food Delivery API", docs_url="/docs")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static file directory
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# routes
app.include_router(auth_router.router)
app.include_router(user_routes.router)
app.include_router(restaurant_routes.router)
app.include_router(menu_item_routes.router)
app.include_router(order_routes.router)
app.include_router(driver_routes.router)

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to Food Delivery API"}