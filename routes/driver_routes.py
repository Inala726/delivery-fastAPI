from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database

router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/", response_model=schemas.DriverResponse)
def create_driver(request: schemas.DriverCreate, db: Session = Depends(get_db)):
    new_driver = models.Driver(user_id=request.user_id)
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver


@router.get("/", response_model=List[schemas.DriverResponse])
def get_all_drivers(db: Session = Depends(get_db)):
    return db.query(models.Driver).all()


@router.get("/{id}", response_model=schemas.DriverResponse)
def get_driver(id: str, db: Session = Depends(get_db)):
    driver = db.query(models.Driver).filter(models.Driver.id == id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@router.delete("/{id}")
def delete_driver(id: str, db: Session = Depends(get_db)):
    driver = db.query(models.Driver).filter(models.Driver.id == id)
    if not driver.first():
        raise HTTPException(status_code=404, detail="Driver not found")
    driver.delete(synchronize_session=False)
    db.commit()
    return {"message": "Driver deleted successfully"}
