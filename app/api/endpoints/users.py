from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.db import models
from app.crud import crud_user
from app.schemas import user as user_schema

router = APIRouter()


@router.post("/users/", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def create_new_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: user_schema.UserCreate,
):
    """
    Create a new user.
    """
    user_by_email = crud_user.get_user_by_email(db, email=user_in.email)
    if user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )

    user_by_username = crud_user.get_user_by_username(db, username=user_in.username)
    if user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )

    user = crud_user.create_user(db=db, user=user_in)
    return user


@router.get("/users/me", response_model=user_schema.User)
def read_current_user(
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Get current user.
    """
    return current_user
