import models  # type: ignore
from schema import BookSchema, AuthorSchema  # type: ignore
from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from database import engine, get_db  # type: ignore

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/books",
          response_model=BookSchema,
          status_code=status.HTTP_201_CREATED)
def create_book(book: BookSchema, db: Session = Depends(get_db)):
    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.post("/authors",
          response_model=AuthorSchema,
          status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorSchema, db: Session = Depends(get_db)):
    new_author = models.Author(**author.dict())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


@app.post("/books/{book_id}/authors/{author_id}/")
def add_author_to_book(book_id: int,
                       author_id: int,
                       db: Session = Depends(get_db)):
    book = db.query(models.Book).\
        filter(models.Book.id == book_id).\
        first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    author = db.query(models.Author).\
        filter(models.Author.id == author_id).\
        first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    book.authors.append(author)
    db.commit()
    return {"message": "Author added to book successfully"}


@app.post("/authors/{author_id}/books/{book_id}/")
def add_book_to_author(author_id: int,
                       book_id: int,
                       db: Session = Depends(get_db)):
    author = db.query(models.Author).\
        filter(models.Author.id == author_id).\
        first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    book = db.query(models.Book).\
        filter(models.Book.id == book_id).\
        first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    author.books.append(book)
    db.commit()
    return {"message": "Book added to author successfully"}


@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).\
        options(joinedload(models.Book.authors)).\
        all()
    return books


@app.get("/authors")
def get_authors(db: Session = Depends(get_db)):
    authors = db.query(models.Author).\
        options(joinedload(models.Author.books)).\
        all()
    return authors


@app.get("/books/{id}", response_model=BookSchema)
def get_book(id: int, db: Session = Depends(get_db)):
    book = (
        db.query(models.Book)
        .options(joinedload(models.Book.authors))
        .where(models.Book.id == id)
        .one()
    )

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"book with id {id} was not found",
        )
    return book


@app.get("/authors/{id}", response_model=AuthorSchema)
def get_author(id: int, db: Session = Depends(get_db)):
    author = (
        db.query(models.Author)
        .options(joinedload(models.Author.books))
        .where(models.Author.id == id)
        .one()
    )

    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"author with id {id} was not found",
        )
    return author


@app.delete("/cleardb", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_tables():
    models.Base.metadata.drop_all(bind=engine)
