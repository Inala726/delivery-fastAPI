from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database

router = APIRouter(
    prefix="/menu",
    tags=["Menu Items"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/", response_model=schemas.MenuItemResponse)
def create_menu_item(request: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    new_item = models.MenuItem(
        name=request.name,
        price=request.price,
        restaurant_id=request.restaurant_id
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get("/", response_model=List[schemas.MenuItemResponse])
def get_all_menu_items(db: Session = Depends(get_db)):
    return db.query(models.MenuItem).all()


@router.get("/{id}", response_model=schemas.MenuItemResponse)
def get_menu_item(id: str, db: Session = Depends(get_db)):
    item = db.query(models.MenuItem).filter(models.MenuItem.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item


@router.delete("/{id}")
def delete_menu_item(id: str, db: Session = Depends(get_db)):
    item = db.query(models.MenuItem).filter(models.MenuItem.id == id)
    if not item.first():
        raise HTTPException(status_code=404, detail="Menu item not found")
    db.delete(item)
    db.commit()
    return {"message": "Menu item deleted successfully"}
