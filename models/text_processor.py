"""
Tamil Text Processor
Handles preprocessing and cleaning of Tamil text input.
"""

import re
from typing import List, Optional

class TamilTextProcessor:
    """Preprocesses and cleans Tamil text for analysis."""
    
    def __init__(self):
        """Initialize Tamil text processor."""
        # Tamil Unicode range: U+0B80 to U+0BFF
        self.tamil_pattern = re.compile(r'[\u0B80-\u0BFF]+')
        
        # Common punctuation and symbols to preserve
        self.keep_symbols = ['.', ',', '!', '?', ';', ':', '-', '(', ')']
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize Tamil text.
        
        Args:
            text: Input Tamil text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Trim
        text = text.strip()
        
        return text
    
    def extract_tamil_only(self, text: str) -> str:
        """
        Extract only Tamil characters from text.
        
        Args:
            text: Input text
            
        Returns:
            Tamil-only text
        """
        tamil_parts = self.tamil_pattern.findall(text)
        return ' '.join(tamil_parts)
    
    def tokenize_words(self, text: str) -> List[str]:
        """
        Tokenize Tamil text into words.
        
        Args:
            text: Input Tamil text
            
        Returns:
            List of Tamil words
        """
        # Split by whitespace
        words = text.split()
        
        # Filter out empty strings
        words = [w for w in words if w.strip()]
        
        return words
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize Tamil text for comparison.
        Removes punctuation and converts to lowercase.
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        # Remove punctuation except Tamil characters and spaces
        text = re.sub(r'[^\u0B80-\u0BFF\s]', '', text)
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Trim
        text = text.strip()
        
        return text
    
    def is_valid_tamil(self, text: str) -> bool:
        """
        Check if text contains valid Tamil characters.
        
        Args:
            text: Input text
            
        Returns:
            True if text contains Tamil characters
        """
        return bool(self.tamil_pattern.search(text))
    
    def count_words(self, text: str) -> int:
        """
        Count Tamil words in text.
        
        Args:
            text: Input text
            
        Returns:
            Number of words
        """
        words = self.tokenize_words(text)
        return len(words)
    
    def preprocess_for_analysis(self, text: str) -> str:
        """
        Full preprocessing pipeline for analysis.
        
        Args:
            text: Raw input text
            
        Returns:
            Preprocessed text ready for analysis
        """
        # Clean
        text = self.clean_text(text)
        
        # Validate
        if not self.is_valid_tamil(text):
            return ""
        
        return text
