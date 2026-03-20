from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    publish_data: int

    def __init__(self, id, title, author, description, rating, publish_date):

        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length = 3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    publish_data: int = Field(gt=1999, lt=2031)

    model_config = {
        'json_schema_extra' : {
            'example' : {
                'title': 'A new book',
                'author': 'Aryan',
                'description': 'A new description of the book',
                'rating': 5,
                'publish_date': 2023
            }
        }
    }


BOOKS = [
    Book(1, 'Computer Science', 'Aryan', 'A very nice book', 5, 2024),
    Book(2, 'fast with fastapi', 'Aryan', 'great book', 5, 2026),
    Book(3, 'master endpoints', 'Aryan', 'good book', 5, 2025),
    Book(4, 'HP1', 'author 1', 'Book Description', 2, 2023),
    Book(5, 'HP2', 'author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'author 3', 'Book Description', 4, 2020)
]

@app.get('/books', status_code=status.HTTP_200_OK)
async def real_all_books():
    return BOOKS


@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Book not found')    
    


@app.get('/books/', status_code=status.HTTP_200_OK)
async def book_rating(book_rating:  int = Query(gt=0, lt=6)):
    get_book = []

    for book in BOOKS:
        if book.rating == book_rating:
            get_book.append(book)

    return get_book

@app.get('/books/publish/', status_code = status.HTTP_200_OK)
async def read_book_by_publish_date(book_request: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.publish_date == book_request:
            books_to_return.append(book)

    return books_to_return

@app.post('/create-book', status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    new_book = find_book_id(new_book)
    BOOKS.append(new_book)
    return BOOKS


@app.put('/books/update_book', status_code= status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    
    if not book_changed:
        raise HTTPException(status_code=404, detail='Book not found')


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.delete('/books/{book_id}', status_code= status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_deleted = True

    if not book_deleted:
        raise HTTPException(status_code=404, detail='Book not Found')


