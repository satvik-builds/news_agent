"""
Custom tools for the News Digest Agent
"""

import requests
from bs4 import BeautifulSoup


def extract_article_text(url: str) -> dict:
    """
    Fetches a webpage and extracts clean article text.
    
    Args:
        url: The URL of the article to extract
        
    Returns:
        dict with 'success', 'text', and optional 'error'
    """
    try:
        # Fetch the webpage
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe']):
            element.decompose()
        
        # Extract article text
        article_text = ""
        article = soup.find('article')
        if article:
            article_text = article.get_text()
        else:
            main_content = soup.find('main') or soup.find('div', class_=lambda x: x and ('content' in x.lower() or 'article' in x.lower()))
            if main_content:
                article_text = main_content.get_text()
            else:
                paragraphs = soup.find_all('p')
                article_text = ' '.join([p.get_text() for p in paragraphs])
        
        # Clean up text
        lines = article_text.split('\n')
        lines = [line.strip() for line in lines if line.strip()]
        clean_text = '\n'.join(lines)
        
        if len(clean_text) < 100:
            return {
                'success': False,
                'text': '',
                'error': 'Article too short or extraction failed'
            }
        
        return {
            'success': True,
            'text': clean_text,
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'text': '',
            'error': f'Extraction error: {str(e)}'
        }


def save_digest_to_file(digest: str, filename: str) -> dict:
    """
    Saves the digest to a file.
    
    Args:
        digest: The digest content to save
        filename: The filename to save to
        
    Returns:
        dict with status
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(digest)
        return {"status": "success", "message": f"Saved to {filename}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
