# BookManagementSystem
Book Management using Backend MongoDB and FastAPI

## FastAPI Book Management System

This project is a simple Book Management System developed using FastAPI, MongoDB, and Python.

## Getting Started

### Prerequisites

Make sure you have Python installed. You will also need to set up a MongoDB database.

### Installation

1. Clone the repository:

```bash
git clone [repository_url]
cd [project_directory]
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

Create a .env file in the project root and add the following configuration:

```bash
MONGODB_ATLAS_URI=[your_mongodb_atlas_uri]
DB_NAME=[your_database_name]
```

Replace [your_mongodb_atlas_uri] and [your_database_name] with your MongoDB Atlas connection string and desired database name.

### Running the Application

Run the FastAPI application:

```bash
uvicorn main:app --reload
```

## Postman Documentation

You can find the Postman Documentation in the PostmanCollection folder

## Swagger Documentation

You can find the Swagger Documentation in the SwaggerDoc folder

## test_main.py

To implement tests cases

## authentication.py

To implement user authentication using OATH2

### Heroku Endpoints

GET https://book-management-seek-fb49ceb1fdf6.herokuapp.com/book/

POST https://book-management-seek-fb49ceb1fdf6.herokuapp.com/book/

GET https://book-management-seek-fb49ceb1fdf6.herokuapp.com/book/{title}

PUT https://book-management-seek-fb49ceb1fdf6.herokuapp.com/book/{title}

DELETE https://book-management-seek-fb49ceb1fdf6.herokuapp.com/book/{title}

GET https://book-management-seek-fb49ceb1fdf6.herokuapp.com/book/average_price/{year}
