from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Setup SQLite Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./flashcards.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Flashcard(Base):
    __tablename__ = "flashcards"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    answer = Column(String)


# Create Database
Base.metadata.create_all(bind=engine)


def get_db():
    # Dependency to get DB Session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
