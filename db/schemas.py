#db/schemas.py
from pydantic import BaseModel
from typing import Optional, List
import datetime

class Book(BaseModel):
    id: Optional[int] = None  # ID yang dihasilkan oleh database
    title: str
    description: str
    year: int
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True  
        

class User(BaseModel):
    id: Optional[int] = None  # ID yang dihasilkan oleh database
    username: str
    email: str
    password: str
    role_id: Optional[int] = 2  # Default value set to 2
    created_at: Optional[datetime.datetime] = None  # Default to None, will be handled by DB
    updated_at: Optional[datetime.datetime] = None  # Default to None, will be handled by DB
    class Config:
        orm_mode = True

class BookWithAuthorsAndBorrowers(BaseModel):
    id: Optional[int] = None  # ID yang dihasilkan oleh database
    title: str
    description: str
    year: int
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    authors: List[User] = []  # List of Users who are authors
    borrowers: List[User] = []  # List of Users who are borrowers

    class Config:
        orm_mode = True
        
        
        
        
        
# SELECT 
#   users.*, 
#   books.*  
# FROM users  
# LEFT JOIN book_authors ON users.id = book_authors.user_id  
# JOIN books ON book_authors.book_id = books.id  
# WHERE users.id = 1;
class UserWithAuthoredAndBorrowedBooks(BaseModel):
    id: Optional[int] = None  # ID yang dihasilkan oleh database
    username: str
    email: str
    password: str
    role_id: Optional[int] = 2  # Default value set to 2
    created_at: Optional[datetime.datetime] = None 
    updated_at: Optional[datetime.datetime] = None 
    authored_books: List[Book] = []  # List of Books authored by this user
    borrowed_books: List[Book] = []  # List of Books borrowed by this user

    class Config:
        orm_mode = True
