from typing import Optional

def encode_description(description: str ) -> Optional[str]:
    """
    Encode description text to UTF-8 and decode back to ensure proper encoding
    
    Args:
        description (str | None): The description text to encode
        
    Returns:
        str | None: UTF-8 encoded and decoded description, or None if input is None
    """
    if description is None:
        return None
    
    try:
        # Encode to UTF-8 and decode back to ensure proper encoding
        return description.encode('utf-8').decode('utf-8')
    except UnicodeError:
        # If there's an encoding error, try to handle common cases
        return description.encode('utf-8', errors='replace').decode('utf-8') 
        