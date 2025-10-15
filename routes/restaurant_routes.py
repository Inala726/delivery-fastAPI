from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database
from app.utils.role_checker import check_roles
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/", response_model=schemas.RestaurantResponse, dependencies=[Depends(check_roles(["restaurant_owner", "admin"]))])
def create_restaurant(
    request: schemas.RestaurantCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only allow admin to create restaurant for other users
    if current_user.role != "admin" and current_user.id != request.owner_id:
        raise HTTPException(
            status_code=403,
            detail="Can only create restaurant for yourself"
        )
    
    new_restaurant = models.Restaurant(
        name=request.name,
        address=request.address,
        owner_id=request.owner_id
    )
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant


@router.get("/", response_model=List[schemas.RestaurantResponse])
def get_all_restaurants(db: Session = Depends(get_db)):
    return db.query(models.Restaurant).all()


@router.get("/{id}", response_model=schemas.RestaurantResponse)
def get_restaurant(id: int, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.delete("/{id}")
def delete_restaurant(id: int, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == id)
    if not restaurant.first():
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurant.delete(synchronize_session=False)
    db.commit()
    return {"message": "Restaurant deleted successfully"}
