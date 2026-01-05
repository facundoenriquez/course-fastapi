from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
]


@app.get("/books/")
async def get_all_books():
    return BOOKS


@app.get("/books/{book_title}")
async def get_book_by_title(book_title: str):
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            return book
    return {"error": "Book not found"}

@app.get("/books/category/")
async def get_books_by_category(category: str):
    categorized_books = [
        book for book in BOOKS if book["category"].casefold() == category.casefold()]
    return categorized_books


@app.post("/books/create_book/")
async def add_book(new_book=Body()):
    BOOKS.append(new_book)
    return BOOKS


@app.put("/books/update_book/")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]["title"].casefold() == updated_book["title"].casefold():
            BOOKS[i] = updated_book
            return BOOKS
    return {"error": "Book not found"}


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i]["title"].casefold() == book_title.casefold():
            BOOKS.pop(i)
            return {"message": "Book deleted successfully", "books": BOOKS}
    return {"error": "Book not found"}


@app.get("/books/author/")
async def get_books_by_author(book_author: str):
    filtered_books = [book for book in BOOKS if book["author"].casefold() == book_author.casefold()]
    return filtered_books
