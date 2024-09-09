from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

# Define the database URL
DATABASE_URL = "mysql+mysqlconnector://root:12345678@localhost/ecommerce"


# Set up SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Set up the database connection for async operations
database = Database(DATABASE_URL)

# Define a model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    query = "SELECT * FROM items WHERE id = :id"
    item = await database.fetch_one(query, values={"id": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
