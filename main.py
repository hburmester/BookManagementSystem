from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import dotenv_values
from routes import router as book_router
from pymongo import MongoClient

config = dotenv_values(".env")

sample_books = [
    {"title": "Book 1", "author": "Author 1", "published_date": "2023-01-01", "genre": "Fiction", "price": 19.99},
    {"title": "Book 2", "author": "Author 2", "published_date": "2022-05-15", "genre": "Science Fiction", "price": 24.99},
    {"title": "Book 3", "author": "Author 3", "published_date": "2021-10-20", "genre": "Mystery", "price": 14.99},
    {"title": "Book 4", "author": "Author 4", "published_date": "2020-03-08", "genre": "Thriller", "price": 29.99},
    {"title": "Book 5", "author": "Author 5", "published_date": "2019-12-12", "genre": "Fantasy", "price": 18.99},
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = MongoClient(config["MONGODB_ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    app.collection = app.database["books"]
    print(app.collection.insert_many(sample_books))
    yield
    app.collection.delete_many({})
    app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(book_router, tags=["books"], prefix="/book")