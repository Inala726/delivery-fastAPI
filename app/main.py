from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models, database


# Create all tables at startup
models.Base.metadata.create_all(bind=database.engine)

# Initialize FastAPI app
app = FastAPI(title="Food Delivery API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes
# app.include_router(user_routes.router)
# app.include_router(post_routes.router)


# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to User Food Delivery API"}