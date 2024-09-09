from sqlalchemy.orm import Session # type: ignore
from sqlalchemy.exc import  SQLAlchemyError # type: ignore
import models, schemas
from fastapi import HTTPException,status # type: ignore

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> dict:
    """Delete a user by ID."""
    try:
        user = db.query(models.User).filter(models.User.id == user_id).one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        db.delete(user)
        db.commit()
        return {"detail": "User deleted successfully"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while deleting the user")


def update_user(db: Session, user_id: int, user_update: schemas.UserCreate):
    # Retrieve the user from the database
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    
    # Check if user exists
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user fields if provided
    if user_update.email:
        db_user.email = user_update.email
    if user_update.hashed_password:
        db_user.hashed_password = user_update.hashed_password
    
    # Commit the transaction
    db.commit()
    db.refresh(db_user)
    
    return db_user
