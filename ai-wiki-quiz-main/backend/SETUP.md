# Backend Setup Instructions

## Environment Variables

Create a `.env` file in the `backend` directory with the following content:

```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/wiki_quiz
```

### Database Options

**SQLite (Default - Easiest)**:
```env
DATABASE_URL=sqlite:///./quiz_history.db
```

**PostgreSQL**:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/wiki_quiz
```

**MySQL**:
```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/wiki_quiz
```

## Getting Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in your `.env` file

## Installation Steps

1. Create virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file with your API key

5. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

