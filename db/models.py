#db/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(DateTime, index=True, nullable=True, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, index=True, nullable=True, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # One-to-One relationship with Role
    role = relationship("RoleModel", back_populates="user")
    
    # One-to-Many relationship with BookAuthors
    authored_books = relationship("BookAuthorModel", back_populates="author")

    # Many-to-Many relationship with Books through BookBorrows
    borrowed_books = relationship("BookBorrowModel", back_populates="user")

class BookModel(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    year = Column(Integer, index=True)
    created_at = Column(DateTime, index=True, nullable=True, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, index=True, nullable=True, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # One-to-Many relationship with BookAuthors
    authors = relationship("BookAuthorModel", back_populates="book")

    # Many-to-Many relationship with Users through BookBorrows
    borrowers = relationship("BookBorrowModel", back_populates="book")

class BookAuthorModel(Base):
    __tablename__ = 'book_authors'
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'), index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    created_at = Column(DateTime, index=True, nullable=True, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, index=True, nullable=True, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    book = relationship("BookModel", back_populates="authors")
    author = relationship("UserModel", back_populates="authored_books")

class BookBorrowModel(Base):
    __tablename__ = "book_borrows"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'), index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    created_at = Column(DateTime, index=True, nullable=True, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, index=True, nullable=True, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    book = relationship("BookModel", back_populates="borrowers")
    user = relationship("UserModel", back_populates="borrowed_books")
    
class RoleModel(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, index=True, nullable=True, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, index=True, nullable=True, default=datetime.datetime.utcnow)

    # One-to-One relationship with User
    user = relationship("UserModel", back_populates="role", uselist=False)