"""
utilities.py

This module contains helper functions that are used across various modules
in the meal planning application.
"""

from typing import Optional
from .special_symbols import digit_emojis

def number_to_emoji(n: int, width: Optional[int] = None) -> str:
    """
    Converts an integer to its emoji representation with optional leading spaces.
    
    Args:
        n (int): The number to convert.
        width (int, optional): The minimum width of the output string. If the emoji
            representation of the number has fewer digits, it will be padded with spaces
            on the left. Defaults to None.
    
    Returns:
        str: The emoji representation of the number with optional leading spaces.
    
    Example:
        >>> number_to_emoji(5)
        '5️⃣'
        >>> number_to_emoji(5, width=2)
        ' 5️⃣'
        >>> number_to_emoji(12, width=4)
        '  1️⃣2️⃣'
    """
    
    
    num_str = str(n)
    emoji_str = ''.join(digit_emojis.get(d, '❓') for d in num_str)  # Use '❓' for unknown digits
    
    if width is not None:
        if len(num_str) < width:
            padding = ' ' * (width - len(num_str))
            emoji_str = padding + emoji_str
    
    return emoji_str
