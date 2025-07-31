import re
from typing import List, Tuple, Optional
import unicodedata

def clean_text(text: str) -> str:
    """Clean and normalize text for analysis"""
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text

def extract_year(text: str) -> Optional[int]:
    """Extract year from citation text"""
    # Look for 4-digit years between 1900-2099
    year_pattern = r'\b(19|20)\d{2}\b'
    match = re.search(year_pattern, text)
    
    if match:
        return int(match.group())
    return None

def extract_authors(text: str) -> List[str]:
    """Extract author names from citation text"""
    authors = []
    
    # Pattern for "LastName, FirstName" format
    author_pattern = r'([A-Z][a-z]+),\s*([A-Z]\.?\s*)+(?:[A-Z]\.?\s*)*'
    matches = re.findall(author_pattern, text)
    
    for match in matches:
        if isinstance(match, tuple):
            authors.append(f"{match[0]}, {match[1]}".strip())
        else:
            authors.append(match)
    
    # Also check for "FirstName LastName" format
    if not authors:
        name_pattern = r'([A-Z][a-z]+\s+[A-Z][a-z]+)'
        matches = re.findall(name_pattern, text)
        authors.extend(matches)
    
    return list(set(authors))  # Remove duplicates

def extract_doi(text: str) -> Optional[str]:
    """Extract DOI from citation text"""
    doi_pattern = r'10\.\d{4,}/[-._;()/:\w]+'
    match = re.search(doi_pattern, text)
    
    if match:
        return match.group()
    return None

def extract_isbn(text: str) -> Optional[str]:
    """Extract ISBN from citation text"""
    # ISBN-10 or ISBN-13 with or without hyphens
    isbn_pattern = r'ISBN[-:\s]*([\d-]+X?)'
    match = re.search(isbn_pattern, text, re.IGNORECASE)
    
    if match:
        isbn = match.group(1).replace('-', '').replace(' ', '')
        # Validate ISBN length
        if len(isbn) in [10, 13]:
            return isbn
    return None

def extract_pages(text: str) -> Optional[Tuple[int, int]]:
    """Extract page numbers from citation"""
    # Pattern for page ranges (e.g., "pp. 123-456" or "p. 123")
    page_pattern = r'(?:pp?\.\s*)(\d+)(?:\s*-\s*(\d+))?'
    match = re.search(page_pattern, text)
    
    if match:
        start_page = int(match.group(1))
        end_page = int(match.group(2)) if match.group(2) else start_page
        return (start_page, end_page)
    return None

def is_url(text: str) -> bool:
    """Check if text contains a URL"""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return bool(re.search(url_pattern, text))

def extract_url(text: str) -> Optional[str]:
    """Extract URL from text"""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    match = re.search(url_pattern, text)
    
    if match:
        return match.group()
    return None

def calculate_citation_density(text: str, citation_count: int) -> float:
    """Calculate citation density (citations per 100 words)"""
    word_count = len(text.split())
    if word_count == 0:
        return 0.0
    
    return (citation_count / word_count) * 100

def format_author_name(first: str, last: str, style: str = "apa") -> str:
    """Format author name according to citation style"""
    if style == "apa":
        # APA: LastName, F. M.
        initials = '. '.join([name[0].upper() for name in first.split()]) + '.'
        return f"{last}, {initials}"
    elif style == "mla":
        # MLA: LastName, FirstName MiddleName
        return f"{last}, {first}"
    elif style == "chicago":
        # Chicago: LastName, FirstName MiddleName
        return f"{last}, {first}"
    else:
        return f"{last}, {first}"

def validate_doi(doi: str) -> bool:
    """Validate DOI format"""
    doi_pattern = r'^10\.\d{4,}/[-._;()/:\w]+$'
    return bool(re.match(doi_pattern, doi))

def validate_isbn(isbn: str) -> bool:
    """Validate ISBN-10 or ISBN-13"""
    isbn = isbn.replace('-', '').replace(' ', '')
    
    if len(isbn) == 10:
        # ISBN-10 validation
        try:
            total = sum((i + 1) * int(digit) for i, digit in enumerate(isbn[:-1]))
            check = total % 11
            return (check == 10 and isbn[-1] == 'X') or (str(check) == isbn[-1])
        except:
            return False
    
    elif len(isbn) == 13:
        # ISBN-13 validation
        try:
            total = sum(int(digit) * (1 if i % 2 == 0 else 3) for i, digit in enumerate(isbn[:-1]))
            check = (10 - (total % 10)) % 10
            return str(check) == isbn[-1]
        except:
            return False
    
    return False

def highlight_text(text: str, highlights: List[Tuple[int, int]], style: str = "error") -> str:
    """Create highlighted version of text for display"""
    # Sort highlights by start position
    highlights = sorted(highlights, key=lambda x: x[0])
    
    # Style mapping
    styles = {
        "error": "🔴",
        "warning": "🟡",
        "success": "🟢",
        "info": "🔵"
    }
    
    marker = styles.get(style, "🔴")
    
    # Build highlighted text
    result = []
    last_end = 0
    
    for start, end in highlights:
        # Add text before highlight
        if start > last_end:
            result.append(text[last_end:start])
        
        # Add highlighted text
        result.append(f"{marker} {text[start:end]} {marker}")
        last_end = end
    
    # Add remaining text
    if last_end < len(text):
        result.append(text[last_end:])
    
    return ''.join(result)

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def extract_title(citation: str) -> Optional[str]:
    """Extract title from citation"""
    # Try to find text in quotes (common for articles)
    quote_pattern = r'"([^"]+)"'
    match = re.search(quote_pattern, citation)
    if match:
        return match.group(1)
    
    # Try to find text in italics markers
    italic_pattern = r'_([^_]+)_|\*([^*]+)\*'
    match = re.search(italic_pattern, citation)
    if match:
        return match.group(1) or match.group(2)
    
    return None