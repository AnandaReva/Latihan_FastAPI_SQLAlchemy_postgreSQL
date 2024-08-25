#main.py
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db import models
from db import schemas
from db.connect import get_db, disconnect_from_db, connect_to_db
from db.models import BookModel, UserModel, BookAuthorModel, BookBorrowModel
from db.schemas import Book, User  # Pydantic schemas
from contextlib import asynccontextmanager

import datetime

# Startup and Shutdown functions
async def startup():
    connect_to_db()

async def shutdown():
    disconnect_from_db()

# Lifespan FastAPI with async context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def index():
    return {"message": "Index page"}

# SHOW ALL USERS
@app.get("/users", response_model=List[User] , tags=["Users"])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()  # Updated to UserModel
    if users is None:
            raise HTTPException(status_code=404, detail="User not found")
    return users

# SHOW USER WITH ID
@app.get("/user/{id}", response_model=User, tags=["Users"])
def get_user(id: int, db: Session = Depends(get_db)):
        user = db.query(UserModel).filter(UserModel.id == id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Users Empty")
        return user
    
# SHOW USER WITH ID AND BOOKS AUTHORED AND BORROWED
@app.get("/user-detail/{id}", response_model=schemas.UserWithAuthoredAndBorrowedBooks, tags=["Users"])
def get_user_detail(id: int, db: Session = Depends(get_db)):
    # Dapatkan user berdasarkan ID
    user = db.query(models.UserModel).filter(models.UserModel.id == id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Dapatkan buku yang telah ditulis oleh user
    authored_books = db.query(models.BookModel).join(models.BookAuthorModel).filter(models.BookAuthorModel.user_id == id).all()

    # Dapatkan buku yang telah dipinjam oleh user
    borrowed_books = db.query(models.BookModel).join(models.BookBorrowModel).filter(models.BookBorrowModel.user_id == id).all()

    # Konversi objek SQLAlchemy ke dict sebelum mengirim ke Pydantic
    authored_books_dict = [schemas.Book.from_orm(book) for book in authored_books]
    borrowed_books_dict = [schemas.Book.from_orm(book) for book in borrowed_books]

    # Bentuk response menggunakan schema
    return schemas.UserWithAuthoredAndBorrowedBooks(
        id=user.id,
        username=user.username,
        email=user.email,
        password=user.password,  # Perhatikan bahwa password biasanya tidak dikembalikan dalam response
        role_id=user.role_id,
        created_at=user.created_at,
        updated_at=user.updated_at,
        authored_books=authored_books_dict,
        borrowed_books=borrowed_books_dict
    )

# CREATE NEW USER
@app.post("/user", response_model=User, tags=["Users"])
def add_user(user: User, db: Session = Depends(get_db)):
    db_user = UserModel(
        username=user.username,
        email=user.email,
        password=user.password,
        role_id=user.role_id,  # Handles defaulting to 2 or using provided value
        created_at=user.created_at or datetime.datetime.utcnow(),
        updated_at=user.updated_at or datetime.datetime.utcnow()
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User could not be created")
    return {"message": "New User successfully added"}

# DELETE USER WITH ID
@app.delete("/user/{id}", tags=["Users"])
def delete_user(id: int, db: Session = Depends(get_db)):
    # Cari pengguna berdasarkan ID
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User successfully deleted"}












@app.post("/book", response_model=Book, tags=["Books"])
def add_book(book: Book, db: Session = Depends(get_db)):
    db_book = BookModel(
        title=book.title,
        description=book.description,
        year=book.year,
        created_at=book.created_at or datetime.datetime.utcnow(),
        updated_at=book.updated_at or datetime.datetime.utcnow()
    )
    db.add(db_book)
    try:
        db.commit()
        db.refresh(db_book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Book could not be created")
    return {"message": "New Book successfully added"}

@app.get("/books", response_model=List[Book], tags=["Books"])   
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(BookModel).all()  # Updated to BookModel
    return books

@app.delete("/book/{id}", tags=["Books"])
def delete_book(id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}
        
