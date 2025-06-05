from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/authors", response_model=List[schemas.Author])
def get_authors(db: Session = Depends(get_db)):
    authors = db.query(models.Author).all()
    return authors

@app.post("/authors", response_model=schemas.Author, status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = models.Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db_author.name = author.name
    db.commit()
    db.refresh(db_author)
    return db_author

@app.delete("/authors/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db.delete(author)
    db.commit()
    return None

@app.get("/books", response_model=List[schemas.Book])
def get_books(author_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(models.Book)
    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)
    books = query.all()
    return books

@app.post("/books", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):

    author = db.query(models.Author).filter(models.Author.id == book.author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()

