# Sample Data

This folder contains example Wikipedia URLs and their corresponding JSON API outputs for testing and demonstration purposes.

## Example URLs Tested

1. `https://en.wikipedia.org/wiki/Alan_Turing`
2. `https://en.wikipedia.org/wiki/Quantum_computing`
3. `https://en.wikipedia.org/wiki/Artificial_intelligence`
4. `https://en.wikipedia.org/wiki/Photosynthesis`
5. `https://en.wikipedia.org/wiki/World_War_II`

## JSON Output Structure

Each quiz output follows this structure:

```json
{
  "id": 1,
  "url": "https://en.wikipedia.org/wiki/Alan_Turing",
  "title": "Alan Turing",
  "summary": "A concise summary of the article...",
  "key_entities": {
    "people": ["Alan Turing", "Alonzo Church"],
    "organizations": ["University of Cambridge", "Bletchley Park"],
    "locations": ["United Kingdom"]
  },
  "sections": ["Early life", "World War II", "Legacy"],
  "quiz": [
    {
      "question": "Where did Alan Turing study?",
      "options": [
        "Harvard University",
        "Cambridge University",
        "Oxford University",
        "Princeton University"
      ],
      "answer": "Cambridge University",
      "difficulty": "easy",
      "explanation": "Mentioned in the 'Early life' section."
    }
  ],
  "related_topics": ["Cryptography", "Enigma machine", "Computer science history"],
  "date_generated": "2025-11-07T10:30:00"
}
```

## Testing Instructions

1. Start the backend server
2. Use the API endpoint `POST /generate_quiz` with any of the example URLs
3. Save the response JSON to this folder for reference
4. Test the frontend by entering these URLs in the "Generate Quiz" tab

## Notes

- Actual JSON outputs will be generated when you run the application
- Each quiz contains 5-10 questions with varying difficulty levels
- The system caches results, so duplicate URLs won't trigger new API calls

