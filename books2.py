from typing import Optional
from fastapi import Body, FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(
        description="The ID of the book (automatically assigned)", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=5)
    published_date: int = Field(gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Alchemist",
                "author": "Paulo Coelho",
                "description": "A novel about a shepherd's journey to find treasure.",
                "rating": 4,
                "published_date": 1988
            }
        }
    }


BOOKS = [
    Book(1, "The Great Gatsby", "F. Scott Fitzgerald",
         "A novel set in the Roaring Twenties.", 5, 1925),
    Book(2, "1984", "George Orwell",
         "A dystopian novel about totalitarianism.", 5, 1948),
    Book(3, "To Kill a Mockingbird", "Harper Lee",
         "A novel about racial injustice in the Deep South.", 5, 1960),
    Book(4, "The Catcher in the Rye", "J.D. Salinger",
         "A story about teenage rebellion and angst.", 4, 1951),
    Book(5, "Pride and Prejudice", "Jane Austen",
         "A classic romance novel.", 5, 1813),
    Book(6, "The Hobbit", "J.R.R. Tolkien",
         "A fantasy novel about a hobbit's adventure.", 5, 1937),
]


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found.")


@app.get("/books/rating/", status_code=status.HTTP_200_OK)
async def read_books_by_rating(rating: int = Query(gt=0, lt=6)):
    books_with_rating = [book for book in BOOKS if book.rating == rating]
    return books_with_rating


@app.post("/create_book/", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return BOOKS


def find_book_id(book: Book):
    book.id = 0 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book/{book_id}", status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book_request: BookRequest = Body()):
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            updated_book = Book(**book_request.model_dump())
            updated_book.id = book_id
            BOOKS[index] = updated_book
            return BOOKS[index]
    raise HTTPException(status_code=404, detail="Book not found.")


@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int = Path(gt=0)):
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS.pop(index)
            return {"Success": "Book deleted."}
    raise HTTPException(status_code=404, detail="Book not found.")


@app.get("/books/published_date/", status_code=status.HTTP_200_OK)
async def read_books_by_published_date(published_date: int = Query(gt=0)):
    books_with_date = [
        book for book in BOOKS if book.published_date == published_date]
    return books_with_date
