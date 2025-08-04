from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import models
from app.db.session import SessionLocal
from app.schemas import token as token_schema
from app.crud import crud_user

# OAuth2PasswordBearer is a class that provides a dependency to get a "bearer token"
# from a request. We point tokenUrl to the full path of our token endpoint.
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/auth/token"
)

def get_db() -> Generator:
    """Dependency to get a DB session."""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    """
    Dependency to get the current user from a JWT token.
    Decodes the token, validates the username, and fetches the user from the DB.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = token_schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = crud_user.get_user_by_username(db, username=token_data.username)

    if user is None:
        raise credentials_exception
    return user
