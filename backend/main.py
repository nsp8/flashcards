from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import Flashcard, get_db

app = FastAPI()


@app.get("/flashcards/")
def read_flashcards(db: Session = Depends(get_db)):
    # API to get all flashcards
    return db.query(Flashcard).all()


@app.post("/flashcards/")
def create_flashcard(question: str, answer: str, db: Session = Depends(get_db)):
    # API to create a flashcard
    flashcard = Flashcard(question=question, answer=answer)
    db.add(flashcard)
    db.commit()
    db.refresh(flashcard)
    return flashcard


@app.get("/flashcards/{flashcard_id}")
def read_flashcard(flashcard_id: int, db: Session = Depends(get_db)):
    # API to get a specific flashcard
    flashcard = db.query(Flashcard).filter(Flashcard.id == flashcard_id).first()
    if flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return flashcard


@app.delete("/flashcards/{flashcard_id}")
def delete_flashcard(flashcard_id: int, db: Session = Depends(get_db)):
    # API to delete a flashcard
    flashcard = db.query(Flashcard).filter(Flashcard.id == flashcard_id).first()
    if flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    db.delete(flashcard)
    db.commit()
    return {"detail": "Flashcard deleted"}
