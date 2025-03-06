"""
Dynamically generated capability: generate_secure_password
"""

import random
import string
from typing import Optional


def generate_secure_password(length: int = 16, include_uppercase: bool = True,
                            include_lowercase: bool = True, include_digits: bool = True,
                            include_special_chars: bool = True, 
                            special_chars: str = "!@#$%^&*()_-+=<>?/[]{}|") -> str:
    """
    Generate a random secure password with configurable length and character types.
    
    Args:
        length: The length of the password to generate. Defaults to 16.
        include_uppercase: Whether to include uppercase letters. Defaults to True.
        include_lowercase: Whether to include lowercase letters. Defaults to True.
        include_digits: Whether to include digits. Defaults to True.
        include_special_chars: Whether to include special characters. Defaults to True.
        special_chars: String containing special characters to use. Defaults to common special characters.
    
    Returns:
        A randomly generated password string with the specified characteristics.
    
    Raises:
        ValueError: If length is less than 1 or if all character type options are False.
    """
    if length < 1:
        raise ValueError("Password length must be at least 1 character")
    
    # Prepare the character pool based on selected options
    char_pool = ""
    
    if include_uppercase:
        char_pool += string.ascii_uppercase
    if include_lowercase:
        char_pool += string.ascii_lowercase
    if include_digits:
        char_pool += string.digits
    if include_special_chars:
        char_pool += special_chars
    
    if not char_pool:
        raise ValueError("At least one character type must be selected")
    
    # Generate the password
    password = ''.join(random.choice(char_pool) for _ in range(length))
    
    return password