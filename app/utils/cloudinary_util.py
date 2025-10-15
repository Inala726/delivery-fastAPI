from cloudinary import uploader
import cloudinary
from fastapi import HTTPException, UploadFile
import os

async def upload_image(file: UploadFile, folder: str = "menu_items") -> dict:
    """
    Upload an image to Cloudinary
    Returns: dict containing 'url' and 'public_id'
    """
    try:
        # Verify file is an image
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Upload to cloudinary
        result = uploader.upload(
            file.file,
            folder=folder,
            resource_type="auto"
        )
        
        return {
            "url": result["secure_url"],
            "public_id": result["public_id"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_image(public_id: str):
    """
    Delete an image from Cloudinary using its public_id
    """
    try:
        result = uploader.destroy(public_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))