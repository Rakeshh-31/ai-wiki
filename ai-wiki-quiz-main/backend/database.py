from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - Using PostgreSQL (can be changed to MySQL or SQLite)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./quiz_history.db"  # Default to SQLite for easier setup
)

# For PostgreSQL, use: postgresql://postgres:postgres@localhost:5432/wiki_quiz
# For MySQL, use: mysql+pymysql://user:password@localhost:3306/wiki_quiz
# For SQLite (default), use: sqlite:///./quiz_history.db

# SQLite requires different connection args
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    date_generated = Column(DateTime, default=datetime.utcnow)
    scraped_content = Column(Text)  # Raw scraped content for bonus
    full_quiz_data = Column(Text)  # JSON serialized quiz data


def init_db():
    """Initialize the database by creating all tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

