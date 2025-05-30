from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel
from typing import List, Optional
from core.auth import get_current_user

router = APIRouter(prefix="/library", tags=["Library Management"])

class BookModel(BaseModel):
    title: str ="Book1"
    author: str = "Aman"
    language: str = "English"
    year: str = "2025"
    file_format: Optional[str] = "PDF" # Optional for EBook

class Library:
    def __init__(self):
        self.books = []
        self.book_count = 0

    def add_book(self, book: BookModel):
        self.books.append(book.dict())
        self.book_count += 1

    def get_books(self):
        return self.books

    def remove_book(self, title: str):
        for book in self.books:
            if book["title"].lower() == title.lower():
                self.books.remove(book)
                self.book_count -= 1
                return True
        return False

    def update_book(self, title: str, data: dict):
        for book in self.books:
            if book["title"].lower() == title.lower():
                book.update(data)
                return book
        return None

library = Library()

@router.post("/books", response_model=BookModel)
def add_book(book: BookModel, current_user: dict = Depends(get_current_user)):
    # Prevent duplicate book titles
    if any(b["title"].lower() == book.title.lower() for b in library.get_books()):
        raise HTTPException(status_code=400, detail="Book with this title already exists.")
    library.add_book(book)
    return book

@router.get("/books", response_model=List[BookModel])
def list_books(current_user: dict = Depends(get_current_user)):
    return library.get_books()

@router.get("/books/{title}", response_model=List[BookModel])
def list_books(title: str,current_user: dict = Depends(get_current_user)):
    books = [book for book in library.get_books() if book["title"].lower() == title.lower()]
    if not books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books
    

@router.put("/books/{title}", response_model=BookModel)
def update_book(title: str, book: BookModel,current_user: dict = Depends(get_current_user)):
    updated = library.update_book(title, book.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@router.delete("/books/{title}")
def delete_book(title: str,current_user: dict = Depends(get_current_user)):
    removed = library.remove_book(title)
    if not removed:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": f"Book '{title}' removed successfully."}
