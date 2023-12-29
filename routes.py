from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Query, Depends, Header
from fastapi.encoders import jsonable_encoder
from typing import List
from datetime import datetime, timedelta
from dotenv import dotenv_values
from models import Book, BookUpdate, UserCheck, User
from authentication import create_access_token, get_current_user

config = dotenv_values(".env")

book_router = APIRouter()
user_router = APIRouter()

@book_router.post("/", response_description="Create a new book", status_code=status.HTTP_201_CREATED, response_model=Book)
def create_book(request: Request, book: Book = Body(...)):
    # Convert datetime.date to datetime.datetime for MongoDB compatibility
    book.published_date = datetime.combine(book.published_date, datetime.min.time()) 

    book = jsonable_encoder(book)
    new_book = request.app.database["books"].insert_one(book)
    created_book = request.app.database["books"].find_one(
        {"_id": new_book.inserted_id}
    )
    
    return created_book

@book_router.get("/", response_description="List all books", response_model=List[Book])
def list_books(request: Request, page: int = Query(1, gt=0), per_page: int = Query(3, gt=0)):
    skip = (page - 1) * per_page
    books = list(request.app.database["books"].find().skip(skip).limit(per_page))
    return books

@book_router.get("/{title}", response_description="Get a single book by title", response_model=Book)
def find_book(title: str, request: Request, ):
    if (book := request.app.database["books"].find_one({"title": title})) is not None:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with title {title} not found")

@book_router.put("/{title}", response_description="Update a book", response_model=Book)
def update_book(title: str, request: Request, newBook: BookUpdate = Body(...)):

    # Convert datetime.date to datetime.datetime for MongoDB compatibility
    if newBook.published_date:
        newBook.published_date = datetime.combine(newBook.published_date, datetime.min.time())
    
    # First checking it's not None
    if (request.app.database["books"].find_one({"title": title})) is not None:

        # Converting to dictionary for MongoDB compatibility
        newBookCheck = {k: v for k, v in newBook.dict().items() if v is not None}

        if len(newBookCheck) >= 1:
            try:
                # Updating the book
                update_result = request.app.database["books"].find_one_and_update(
                    filter={"title": title},
                    update={"$set": newBook.model_dump(exclude_unset=True)},
                    return_document=True,
                )
            except:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with title {title} not updated")

            # Returning book as response
            return update_result
    
    # Raising 404 if no book with the same "title" was found
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with title {title} not found")

@book_router.delete("/{title}", response_description="Delete a book")
def delete_book(title: str, request: Request, response: Response):
    delete_result = request.app.database["books"].delete_one({"title": title})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with title {title} not found")

@book_router.get("/average_price/{year}", response_description="Get average price after a year")
def get_average_price(year: int, request: Request):
    pipeline = [
        {"$match": {"published_date": {"$gt": f"{year}-01-01"}}},
        {"$group": {"_id": None, "average_price": {"$avg": "$price"}}}
    ]

    result = list(request.app.database["books"].aggregate(pipeline))

    if result:
        average_price = result[0]["average_price"]
        return {"average_price": str(round(average_price, 2))}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No books found after the specified year")

@user_router.post("/sign_up", response_model=User)
async def login_for_access_token(form_data: UserCheck, request: Request):

    if request.app.database["users"].find_one({"username": form_data.username}):
        access_token_expires = timedelta(minutes=int(config["ACCESS_TOKEN_EXPIRE_MINUTES"]))
        access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
        new_user = User(username=form_data.username, password=form_data.password, token = access_token)
        new_user = jsonable_encoder(new_user)

        try:
            request.app.database["users"].find_one_and_update(
                filter={"username": form_data.username},
                update={"$set": {"token": access_token}}
            )
        except:
            request.app.database["users"].insert_one(new_user)

        return new_user


    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

@user_router.get("/username/", response_model=User)
async def get_usersame(request: Request, token: str):
    user_detail = request.app.database["users"].find_one({"token" : token})
    return user_detail

@user_router.get("/users", response_model=List[User])
async def get_users(request: Request):
    users = list(request.app.database["users"].find())
    return users
