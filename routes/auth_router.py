from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, database
from app.utils import verify_password
from app.utils.auth import create_access_token, get_current_user
from app.schemas import TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"user_id": user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/token/test", response_model=UserResponse)
async def test_token(current_user = Depends(get_current_user)):
    """
    Test access token endpoint
    """
    return current_user


# ✅ NEW ENDPOINT
@router.get("/me", response_model=UserResponse, operation_id="get_profile")
async def get_profile(current_user: models.User = Depends(get_current_user)):
    """
    Retrieve the currently logged-in user's profile.
    Returns user data based on the JWT token.
    """
    return current_user
