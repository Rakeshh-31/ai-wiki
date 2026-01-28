from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json
from datetime import datetime

from database import init_db, get_db, Quiz
from models import GenerateQuizRequest, QuizResponse, HistoryItem
from scraper import scrape_wikipedia
from llm_quiz_generator import QuizGenerator

app = FastAPI(title="AI Wiki Quiz Generator API")

# CORS middleware to allow React frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],  # Vite ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Initialize quiz generator (lazy initialization to handle errors better)
quiz_generator = None

def get_quiz_generator():
    global quiz_generator
    if quiz_generator is None:
        try:
            quiz_generator = QuizGenerator()
        except Exception as e:
            print(f"Error initializing QuizGenerator: {str(e)}")
            raise
    return quiz_generator


@app.get("/")
def root():
    return {"message": "AI Wiki Quiz Generator API", "status": "running"}


@app.post("/generate_quiz", response_model=QuizResponse)
def generate_quiz(request: GenerateQuizRequest, db: Session = Depends(get_db)):
    """
    Generate a quiz from a Wikipedia URL.
    
    1. Scrapes the Wikipedia article
    2. Generates quiz using LLM
    3. Stores in database
    4. Returns the quiz data
    """
    try:
        # Validate URL
        if not request.url.startswith("https://en.wikipedia.org/wiki/"):
            raise HTTPException(status_code=400, detail="Invalid Wikipedia URL. Must be from en.wikipedia.org")
        
        # Check if URL already exists in database (caching)
        existing_quiz = db.query(Quiz).filter(Quiz.url == request.url).first()
        if existing_quiz:
            # Return existing quiz
            quiz_data = json.loads(existing_quiz.full_quiz_data)
            return QuizResponse(
                id=existing_quiz.id,
                url=existing_quiz.url,
                title=existing_quiz.title,
                date_generated=existing_quiz.date_generated,
                **quiz_data
            )
        
        # Scrape Wikipedia
        try:
            scraped_content, title = scrape_wikipedia(request.url)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Scraping error: {str(e)}")
        
        # Generate quiz using LLM
        try:
            print(f"Generating quiz for: {title}")
            generator = get_quiz_generator()
            quiz_data = generator.generate_quiz(scraped_content, title)
            print(f"Quiz generated successfully for: {title}")
        except ValueError as e:
            print(f"Quiz generation error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Quiz generation error: {str(e)}")
        except Exception as e:
            print(f"Unexpected error during quiz generation: {str(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Quiz generation error: {str(e)}")
        
        # Store in database
        quiz_record = Quiz(
            url=request.url,
            title=title,
            scraped_content=scraped_content,  # Store raw content for bonus
            full_quiz_data=json.dumps(quiz_data)  # Serialize quiz data to JSON string
        )
        db.add(quiz_record)
        db.commit()
        db.refresh(quiz_record)
        
        # Return response
        return QuizResponse(
            id=quiz_record.id,
            url=quiz_record.url,
            title=quiz_record.title,
            date_generated=quiz_record.date_generated,
            **quiz_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/history", response_model=List[HistoryItem])
def get_history(db: Session = Depends(get_db)):
    """
    Get list of all previously generated quizzes.
    Returns id, url, title, and date_generated.
    """
    try:
        quizzes = db.query(Quiz).order_by(Quiz.date_generated.desc()).all()
        return [
            HistoryItem(
                id=quiz.id,
                url=quiz.url,
                title=quiz.title,
                date_generated=quiz.date_generated
            )
            for quiz in quizzes
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")


@app.get("/quiz/{quiz_id}", response_model=QuizResponse)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """
    Get a specific quiz by ID.
    Deserializes the full_quiz_data from JSON string back to object.
    """
    try:
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        # Deserialize the JSON string back to dict
        quiz_data = json.loads(quiz.full_quiz_data)
        
        return QuizResponse(
            id=quiz.id,
            url=quiz.url,
            title=quiz.title,
            date_generated=quiz.date_generated,
            **quiz_data
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error parsing quiz data")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching quiz: {str(e)}")

