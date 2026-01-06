from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

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
    id: Optional[int] = Field(description="The ID of the book (automatically assigned)", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=5)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Alchemist",
                "author": "Paulo Coelho",
                "description": "A novel about a shepherd's journey to find treasure.",
                "rating": 4
            }
        }
    }


BOOKS = [
    Book(1, "The Great Gatsby", "F. Scott Fitzgerald",
         "A novel set in the Roaring Twenties.", 5),
    Book(2, "1984", "George Orwell", "A dystopian novel about totalitarianism.", 5),
    Book(3, "To Kill a Mockingbird", "Harper Lee",
         "A novel about racial injustice in the Deep South.", 5),
    Book(4, "The Catcher in the Rye", "J.D. Salinger",
         "A story about teenage rebellion and angst.", 4),
    Book(5, "Pride and Prejudice", "Jane Austen", "A classic romance novel.", 5),
    Book(6, "The Hobbit", "J.R.R. Tolkien",
         "A fantasy novel about a hobbit's adventure.", 5),
]


@app.get("/books/")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return {"Error": "Book not found."}

@app.get("/books/rating/")
async def read_books_by_rating(rating: int):
    books_with_rating = [book for book in BOOKS if book.rating == rating]
    return books_with_rating


@app.post("/create_book/")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return BOOKS

def find_book_id(book: Book):
    book.id = 0 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book