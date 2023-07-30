from pydantic import BaseModel
from typing import List


class AuthorBase(BaseModel):
    id: int | None = None
    name: str
    country: str

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    id: int | None = None
    title: str
    year: str

    class Config:
        orm_mode = True


class BookSchema(BookBase):
    authors: List[AuthorBase] | None


class AuthorSchema(AuthorBase):
    books: List[BookBase] | None
