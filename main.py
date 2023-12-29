from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import dotenv_values
from routes import book_router, user_router
from pymongo import MongoClient
import os

config = dotenv_values(".env")

try:
    MONGODB_ATLAS_URI = config["MONGODB_ATLAS_URI"]
    DB_NAME=config["DB_NAME"]
except:
    MONGODB_ATLAS_URI = os.environ["MONGODB_ATLAS_URI"]
    DB_NAME=os.environ["DB_NAME"]

sample_books = [
    {"title": "Book 1", "author": "Author 1", "published_date": "2023-01-01", "genre": "Fiction", "price": 19.99},
    {"title": "Book 2", "author": "Author 2", "published_date": "2022-05-15", "genre": "Science Fiction", "price": 24.99},
    {"title": "Book 3", "author": "Author 3", "published_date": "2021-10-20", "genre": "Mystery", "price": 14.99},
    {"title": "Book 4", "author": "Author 4", "published_date": "2020-03-08", "genre": "Thriller", "price": 29.99},
    {"title": "Book 5", "author": "Author 5", "published_date": "2019-12-12", "genre": "Fantasy", "price": 18.99},
]

sample_users = [
    {"username": "hburmester", "password": "passtest", "token": None},
    {"username": "wburmester", "password": "testword", "token": None},
    {"username": "aburmester", "password": "wordpass", "token": None}
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = MongoClient(MONGODB_ATLAS_URI)
    app.database = app.mongodb_client[DB_NAME]
    app.book_collection = app.database["books"]
    app.user_collection = app.database["users"]
    app.book_collection.insert_many(sample_books)
    app.user_collection.insert_many(sample_users)
    yield
    app.book_collection.delete_many({})
    app.user_collection.delete_many({})
    app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(book_router, tags=["books"], prefix="/book")
app.include_router(user_router, tags=["userAuth"], prefix="/userAuth")