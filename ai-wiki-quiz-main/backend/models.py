from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class QuizQuestion(BaseModel):
    question: str = Field(..., description="The quiz question text")
    options: List[str] = Field(..., min_items=4, max_items=4, description="Four answer options (A-D)")
    answer: str = Field(..., description="The correct answer")
    difficulty: str = Field(..., description="Difficulty level: easy, medium, or hard")
    explanation: str = Field(..., description="Short explanation for the answer")


class KeyEntities(BaseModel):
    people: List[str] = Field(default_factory=list, description="List of people mentioned")
    organizations: List[str] = Field(default_factory=list, description="List of organizations mentioned")
    locations: List[str] = Field(default_factory=list, description="List of locations mentioned")


class QuizOutput(BaseModel):
    """Strict JSON structure that the LLM must return"""
    summary: str = Field(..., description="A concise summary of the Wikipedia article")
    key_entities: KeyEntities = Field(..., description="Key entities extracted from the article")
    sections: List[str] = Field(..., description="List of main section headings from the article")
    quiz: List[QuizQuestion] = Field(..., min_items=5, max_items=10, description="List of 5-10 quiz questions")
    related_topics: List[str] = Field(..., description="Suggested related Wikipedia topics for further reading")


class QuizResponse(BaseModel):
    """API response model"""
    id: int
    url: str
    title: str
    summary: str
    key_entities: Dict
    sections: List[str]
    quiz: List[Dict]
    related_topics: List[str]
    date_generated: datetime


class HistoryItem(BaseModel):
    """Model for history list items"""
    id: int
    url: str
    title: str
    date_generated: datetime


class GenerateQuizRequest(BaseModel):
    """Request model for quiz generation"""
    url: str = Field(..., description="Wikipedia article URL")

