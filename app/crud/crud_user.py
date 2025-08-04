from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db import models
from app.schemas import user as user_schema


def get_user_by_email(db: Session, email: str) -> models.User | None:
    """Fetches a user by their email address."""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> models.User | None:
    """Fetches a user by their username."""
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: user_schema.UserCreate) -> models.User:
    """Creates a new user in the database."""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
