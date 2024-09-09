from fastapi import Depends, FastAPI # type: ignore
from sqlalchemy.orm import Session # type: ignore
import crud, models, schemas
from database import engine, SessionLocal
from typing import List

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/user/{id}", response_model=schemas.User)
def get_user_by_id(id: int,db: Session = Depends(get_db)):
    # Assuming `crud.get_user` is a function that takes an ID and returns user data
    return crud.get_user(db=db, user_id=id)

@app.get("/users", response_model=List[schemas.User])
def get_all_users_endpoint(db: Session = Depends(get_db)):
    """Retrieve all users from the database."""
    return crud.get_all_users(db=db)

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=user)
    return db_user

@app.put("/update/users/{user_id}", response_model=schemas.User)
def update_user_route(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db=db, user_id=user_id, user_update=user_update)
    return updated_user

@app.delete("/delete/users/{user_id}", response_model=schemas.User)
def delete_user_route(user_id: int,  db: Session = Depends(get_db)):
    updated_user = crud.delete_user(db=db, user_id=user_id)
    return updated_user
