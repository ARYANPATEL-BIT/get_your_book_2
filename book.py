from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int


    def __init__(self, id, title, author, description, rating):

        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length = 3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)

    model_config = {
        'json_schema_extra' : {
            'example' : {
                'title': 'A new book',
                'author': 'Aryan',
                'description': 'A new description of the book',
                'rating': 5
            }
        }
    }


BOOKS = [
    Book(1, 'Computer Science', 'Aryan', 'A very nice book', 5),
    Book(2, 'fast with fastapi', 'Aryan', 'great book', 5),
    Book(3, 'master endpoints', 'Aryan', 'good book', 5),
    Book(4, 'HP1', 'author 1', 'Book Description', 2),
    Book(5, 'HP2', 'author 2', 'Book Description', 3),
    Book(6, 'HP3', 'author 3', 'Book Description', 4)
]

@app.get('/books')
async def real_all_books():
    return BOOKS


@app.post('/create-book')
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    new_book = find_book_id(new_book)
    BOOKS.append(new_book)
    return BOOKS


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book