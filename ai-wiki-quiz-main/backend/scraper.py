import requests
from bs4 import BeautifulSoup
from typing import Tuple
import re


def scrape_wikipedia(url: str) -> Tuple[str, str]:
    """
    Scrape Wikipedia article and extract clean text content.
    
    Args:
        url: Wikipedia article URL
        
    Returns:
        Tuple of (clean_text, title)
    """
    try:
        # Fetch the page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title_elem = soup.find('h1', class_='firstHeading')
        title = title_elem.get_text().strip() if title_elem else "Unknown Title"
        
        # Find main content area using Wikipedia's standard content ID
        content_div = soup.find('div', id='mw-content-text')
        if not content_div:
            raise ValueError("Could not find main content area")
        
        # Remove reference links (sup tags containing citation numbers)
        for sup in content_div.find_all('sup'):
            sup.decompose()
        
        # Remove tables (they contain structured data, not narrative text)
        for table in content_div.find_all('table'):
            table.decompose()
        
        # Remove navigation boxes, infoboxes, edit sections, and other boilerplate
        for element in content_div.find_all(['div', 'span'], class_=re.compile(r'reference|navbox|infobox|mw-editsection|hatnote|thumb|thumbinner|gallery')):
            element.decompose()
        
        # Remove all script, style, nav, and aside elements
        for element in content_div.find_all(['script', 'style', 'nav', 'aside']):
            element.decompose()
        
        # Extract text from paragraphs and headings
        text_parts = []
        
        # Get all headings and paragraphs
        for elem in content_div.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
            text = elem.get_text(separator=' ', strip=True)
            if text and len(text) > 20:  # Filter out very short text
                text_parts.append(text)
        
        # Join all text parts
        clean_text = '\n\n'.join(text_parts)
        
        # Additional cleaning: remove excessive whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text)
        clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text)
        
        # Limit text length to avoid token limits (keep first 8000 characters)
        if len(clean_text) > 8000:
            clean_text = clean_text[:8000] + "..."
        
        if not clean_text or len(clean_text) < 100:
            raise ValueError("Extracted content is too short or empty")
        
        return clean_text, title
        
    except requests.RequestException as e:
        raise ValueError(f"Failed to fetch URL: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error scraping Wikipedia: {str(e)}")

