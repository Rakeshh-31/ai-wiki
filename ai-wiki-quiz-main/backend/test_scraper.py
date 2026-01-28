"""
Test script to scrape a Wikipedia article and display the results.
Run this to test the scraper functionality.
"""
from scraper import scrape_wikipedia
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def main():
    # Default test URL
    default_url = "https://en.wikipedia.org/wiki/Alan_Turing"
    
    # Get URL from command line or use default
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = default_url
        print(f"No URL provided. Using default: {url}\n")
        print("Usage: python test_scraper.py <wikipedia_url>\n")
    
    print("=" * 80)
    print(f"Scraping: {url}")
    print("=" * 80)
    print()
    
    try:
        # Scrape the article
        clean_text, title = scrape_wikipedia(url)
        
        # Display results
        print(f"Title: {title}")
        print()
        print("=" * 80)
        print("Extracted Content (first 2000 characters):")
        print("=" * 80)
        print(clean_text[:2000])
        print()
        print("...")
        print()
        print(f"Total length: {len(clean_text)} characters")
        print()
        print("=" * 80)
        print("Scraping completed successfully!")
        print("=" * 80)
        print()
        print("You can now use this URL in the frontend to generate a quiz!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

