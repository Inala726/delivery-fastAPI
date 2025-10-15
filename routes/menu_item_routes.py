from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database
from app.utils.cloudinary_util import upload_image, delete_image

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
        description=request.description,
        price=request.price,
        restaurant_id=request.restaurant_id,
        image_url=request.image_url
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.post("/{item_id}/upload-image")
async def upload_menu_item_image(
    item_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload an image for a menu item to Cloudinary"""
    # Check if menu item exists
    menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # If there's an existing image, delete it from Cloudinary
    if menu_item.image_url:
        # Extract public_id from the URL
        try:
            old_public_id = menu_item.image_url.split("/")[-1].split(".")[0]
            await delete_image(f"menu_items/{old_public_id}")
        except:
            pass  # If deletion fails, continue with upload
    
    # Upload new image to Cloudinary
    result = await upload_image(file, folder="menu_items")
    
    # Update menu item with new image URL
    menu_item.image_url = result["url"]
    db.commit()
    
    return {"image_url": result["url"]}


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
