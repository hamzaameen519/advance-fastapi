from sqlalchemy.orm import Session # type: ignore
import models, schemas
from fastapi import HTTPException # type: ignore
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
      try:
        deleted_user = db.remove(db=db, user_id=user_id)
        return deleted_user
      except HTTPException as e:
        raise e

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
