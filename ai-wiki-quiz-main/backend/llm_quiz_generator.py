from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models import QuizOutput
import os
from dotenv import load_dotenv
import json

load_dotenv()


class QuizGenerator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=api_key,
            temperature=0.7,
            convert_system_message_to_human=True  # Gemini doesn't support SystemMessage
        )
        # Use JsonOutputParser without pydantic_object for v2 compatibility
        # We'll validate manually with Pydantic v2
        self.parser = JsonOutputParser()
        
        # Detailed prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert educational content creator specializing in creating engaging and educational quizzes from Wikipedia articles.

Your task is to analyze the provided Wikipedia article text and generate a comprehensive quiz that:
1. Tests understanding of key concepts, facts, and important details
2. Covers different aspects of the topic (history, significance, key figures, etc.)
3. Includes questions of varying difficulty levels
4. Provides clear, accurate explanations
5. Identifies key entities (people, organizations, locations)
6. Suggests related topics for further learning

IMPORTANT GUIDELINES:
- Generate exactly 5-10 questions (aim for 7-8 questions)
- Each question must have exactly 4 options (A, B, C, D)
- Ensure the correct answer is factually accurate based on the article
- Vary difficulty levels: include easy, medium, and hard questions
- Provide concise but informative explanations (1-2 sentences)
- Extract all key entities mentioned in the article
- Identify main sections/headings from the article
- Suggest 3-5 related Wikipedia topics that would complement this article

OUTPUT FORMAT: You must return valid JSON matching the exact structure specified."""),
            ("human", """Analyze the following Wikipedia article and generate a quiz:

Article Title: {title}

Article Content:
{article_text}

Generate a quiz with the following structure:
- A concise summary (2-3 sentences)
- Key entities (people, organizations, locations)
- Main sections/headings
- 5-10 quiz questions with 4 options each, correct answers, difficulty levels, and explanations
- Related topics for further reading

{format_instructions}""")
        ])
        
        self.chain = self.prompt_template | self.llm | self.parser
    
    def generate_quiz(self, article_text: str, title: str) -> dict:
        """
        Generate quiz from article text using LLM.
        
        Args:
            article_text: Clean text content from Wikipedia
            title: Article title
            
        Returns:
            Dictionary containing quiz data
        """
        try:
            # Get format instructions from the schema
            schema = QuizOutput.model_json_schema()
            format_instructions = f"""You must return a valid JSON object matching this schema:
{json.dumps(schema, indent=2)}

Ensure the response is valid JSON only, no markdown formatting."""
            
            # Format the chain with inputs
            result = self.chain.invoke({
                "article_text": article_text,
                "title": title,
                "format_instructions": format_instructions
            })
            
            # Validate and parse with Pydantic v2
            if isinstance(result, dict):
                # Validate the result against our Pydantic model
                validated_result = QuizOutput.model_validate(result)
                return validated_result.model_dump()
            
            # If it's already a string, parse it
            if isinstance(result, str):
                result = json.loads(result)
                validated_result = QuizOutput.model_validate(result)
                return validated_result.model_dump()
            
            return result
            
        except Exception as e:
            raise ValueError(f"Error generating quiz with LLM: {str(e)}")

