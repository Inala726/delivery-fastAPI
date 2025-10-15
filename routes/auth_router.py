# #
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from pydantic import BaseModel, EmailStr
# from app import models, database
# from app.utils import verify_password
# from app.utils.auth import create_access_token

# router = APIRouter(prefix="/auth", tags=["Authentication"])


# # Dependency to get database session
# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # Request model for login
# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str


# # Response model for token
# class TokenResponse(BaseModel):
#     access_token: str
#     token_type: str = "bearer"


# @router.post("/login", response_model=TokenResponse)
# def login(data: LoginRequest, db: Session = Depends(get_db)):
#     """
#     Authenticate a user using email and password, then issue a JWT access token.
#     """
#     user = db.query(models.User).filter(models.User.email == data.email).first()
#     if not user or not verify_password(data.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid credentials",
#         )

#     # Generate JWT token with user ID
#     token = create_access_token({"user_id": user.id})

#     return {"access_token": token, "token_type": "bearer"}


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
    Test access token
    """
    return current_user