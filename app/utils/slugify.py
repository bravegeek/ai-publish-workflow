"""
Utility functions for string manipulation, particularly for generating URL-friendly slugs.
"""
import re
import unicodedata
from typing import Optional

def slugify(text: str, separator: str = '-', max_length: int = 100) -> str:
    """
    Convert a string to a URL-friendly slug.
    
    Args:
        text: The text to convert to a slug
        separator: The separator to use between words (default: '-')
        max_length: Maximum length of the resulting slug (default: 100)
        
    Returns:
        A URL-friendly slug string
        
    Example:
        >>> slugify("Hello World! How are you?")
        'hello-world-how-are-you'
    """
    if not text:
        return ""
    
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', str(text))
    
    # Convert to lowercase and remove special characters
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    
    # Replace whitespace and dashes with the separator
    text = re.sub(r'[\s-]+', separator, text)
    
    # Remove any leading/trailing separators
    text = text.strip(separator)
    
    # Truncate to max_length if needed
    if max_length > 0 and len(text) > max_length:
        text = text[:max_length].rsplit(separator, 1)[0]  # Don't cut in the middle of a word
    
    return text

def unique_slug(db_session, model, slug: str, field: str = 'slug', separator: str = '-') -> str:
    """
    Generate a unique slug by appending a number if the slug already exists.
    
    Args:
        db_session: Database session
        model: SQLAlchemy model class to check for existing slugs
        slug: The base slug to make unique
        field: The field name to check for uniqueness (default: 'slug')
        separator: Separator to use between slug and number (default: '-')
        
    Returns:
        A unique slug
    """
    if not slug:
        raise ValueError("Slug cannot be empty")
    
    # Make sure the slug is URL-friendly
    slug = slugify(slug, separator=separator)
    
    # Check if the slug already exists
    query = {field: slug}
    existing = db_session.query(model).filter_by(**query).first()
    
    if not existing:
        return slug
    
    # If it exists, append a number and try again
    i = 1
    while True:
        new_slug = f"{slug}{separator}{i}"
        query[field] = new_slug
        if not db_session.query(model).filter_by(**query).first():
            return new_slug
        i += 1
