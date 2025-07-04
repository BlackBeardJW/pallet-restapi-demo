# Initialize the database
from db import engine, Base
from models import Pallet

Base.metadata.create_all(bind=engine)
print("Database initialized successfully.")