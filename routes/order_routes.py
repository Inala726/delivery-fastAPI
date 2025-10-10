from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

def get_db():from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.OrderResponse)
def create_order(request: schemas.OrderCreate, db: Session = Depends(get_db)):
    new_order = models.Order(
        customer_id=request.customer_id,
        restaurant_id=request.restaurant_id,
        total_price=request.total_price,
        status=request.status
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/", response_model=List[schemas.OrderResponse])
def get_all_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()


@router.get("/{id}", response_model=schemas.OrderResponse)
def get_order(id: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{id}")
def delete_order(id: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == id)
    if not order.first():
        raise HTTPException(status_code=404, detail="Order not found")
    order.delete(synchronize_session=False)
    db.commit()
    return {"message": "Order deleted successfully"}

    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.OrderResponse)
def create_order(request: schemas.OrderCreate, db: Session = Depends(get_db)):
    new_order = models.Order(
        customer_id=request.customer_id,
        restaurant_id=request.restaurant_id,
        total_price=request.total_price,
        status=request.status
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/", response_model=List[schemas.OrderResponse])
def get_all_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()


@router.get("/{id}", response_model=schemas.OrderResponse)
def get_order(id: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{id}")
def delete_order(id: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == id)
    if not order.first():
        raise HTTPException(status_code=404, detail="Order not found")
    order.delete(synchronize_session=False)
    db.commit()
    return {"message": "Order deleted successfully"}
