from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Flashcard, get_db
from settings import Logger, STREAMLIT_APP_URI

logger = Logger("backend").logger

app = FastAPI()
origins = [
    STREAMLIT_APP_URI,
]

url_match = rf"{STREAMLIT_APP_URI}/?.*|" \

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=url_match,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FlashCardModel(BaseModel):
    question: str
    answer: str


@app.get("/flashcards/")
async def read_flashcards(db: Session = Depends(get_db)):
    # API to get all flashcards
    return db.query(Flashcard).all()


@app.post("/flashcards/")
def create_flashcard(
        flash_card: FlashCardModel,
        db: Session = Depends(get_db)
):
    # API to create a flashcard
    logger.info(f"{flash_card.question=} {flash_card.answer=}")
    flashcard = Flashcard(question=flash_card.question, answer=flash_card.answer)
    logger.info(
        f"flashcard [{flashcard.id}]:"
        f"\nQ: {flashcard.question}"
        f"\nA: {flashcard.answer}"
    )
    db.add(flashcard)
    db.commit()
    db.refresh(flashcard)
    return flashcard


@app.get("/flashcards/{flashcard_id}")
async def read_flashcard(flashcard_id: int, db: Session = Depends(get_db)):
    # API to get a specific flashcard
    flashcard = db.query(Flashcard).filter(Flashcard.id == flashcard_id).first()
    if flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return flashcard


@app.delete("/flashcards/{flashcard_id}")
async def delete_flashcard(flashcard_id: int, db: Session = Depends(get_db)):
    # API to delete a flashcard
    flashcard = db.query(Flashcard).filter(Flashcard.id == flashcard_id).first()
    if flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    db.delete(flashcard)
    db.commit()
    return {"detail": "Flashcard deleted"}


@app.delete("/flashcards/")
async def delete_flashcards(db: Session = Depends(get_db)):
    # API to delete all Flashcards
    flashcards = await read_flashcards(db)
    if not flashcards:
        raise HTTPException(status_code=404, detail="Flashcards not found")
    db.query(Flashcard).delete()
    db.commit()
    return {"detail": "Flashcards deleted"}
