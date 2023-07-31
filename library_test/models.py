from database import Base  # type: ignore
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    year = Column(String, nullable=False)
    authors = relationship("Author",
                           secondary="book_authors",
                           back_populates="books",
                           cascade="all, delete")



class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    books = relationship("Book", secondary="book_authors", back_populates="authors")  # noqa 501
