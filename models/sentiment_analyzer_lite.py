"""
Lightweight Sentiment Analyzer for Quick Start
Uses rule-based approach with option to upgrade to ML models later.
"""

import re
from typing import Dict, Any

class SentimentAnalyzer:
    """Analyzes sentiment of Tamil text using rule-based approach."""
    
    def __init__(self, cache_dir: str = "./cache/xlm-roberta"):
        """
        Initialize sentiment analyzer with rule-based approach.
        """
        print(f"✅ Sentiment analyzer ready (rule-based mode)")
        
        # Sentiment keywords for Tamil
        self.positive_keywords = [
            'நன்று', 'சிறப்பு', 'மகிழ்ச்சி', 'அழகு', 'இனிமை', 'நலம்', 
            'புகழ்', 'வாழ்க', 'பெருமை', 'காதல்', 'அன்பு', 'நட்பு',
            'வெற்றி', 'சந்தோஷம்', 'உவகை', 'மகிழ்வு', 'நகை', 'இன்பம்',
            'வளம்', 'செழிப்பு', 'சிறந்த', 'உயர்ந்த', 'நல்ல', 'நேர்மை'
        ]
        
        self.negative_keywords = [
            'துன்பம்', 'வருத்தம்', 'கோபம்', 'வெறுப்பு', 'பகை', 'சோகம்',
            'அழுகை', 'தீமை', 'குற்றம்', 'தோல்வி', 'வேதனை', 'கவலை',
            'கசப்பு', 'வலி', 'நோய்', 'பாவம்', 'கொடுமை', 'இழப்பு',
            'பயம்', 'அச்சம்', 'தவறு', 'பிழை', 'கெட்ட', 'கேடு'
        ]
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of Tamil text using keyword matching.
        
        Args:
            text: Input Tamil text
            
        Returns:
            Dictionary with sentiment analysis results
        """
        if not text or len(text.strip()) == 0:
            return {
                'sentiment': 'NEUTRAL',
                'confidence': 0.0,
                'method': 'empty_text'
            }
        
        try:
            # Count positive and negative keywords
            positive_count = sum(1 for word in self.positive_keywords if word in text)
            negative_count = sum(1 for word in self.negative_keywords if word in text)
            
            total_keywords = positive_count + negative_count
            
            if total_keywords == 0:
                # No keywords found - analyze context
                return {
                    'sentiment': 'NEUTRAL',
                    'confidence': 0.5,
                    'method': 'rule_based'
                }
            
            if positive_count > negative_count:
                confidence = min(0.7 + (positive_count * 0.05), 0.95)
                return {
                    'sentiment': 'POSITIVE',
                    'confidence': round(confidence, 2),
                    'method': 'rule_based',
                    'details': {
                        'positive_matches': positive_count,
                        'negative_matches': negative_count
                    }
                }
            elif negative_count > positive_count:
                confidence = min(0.7 + (negative_count * 0.05), 0.95)
                return {
                    'sentiment': 'NEGATIVE',
                    'confidence': round(confidence, 2),
                    'method': 'rule_based',
                    'details': {
                        'positive_matches': positive_count,
                        'negative_matches': negative_count
                    }
                }
            else:
                # Equal counts
                return {
                    'sentiment': 'NEUTRAL',
                    'confidence': 0.6,
                    'method': 'rule_based',
                    'details': {
                        'positive_matches': positive_count,
                        'negative_matches': negative_count
                    }
                }
                
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return {
                'sentiment': 'NEUTRAL',
                'confidence': 0.5,
                'method': 'error_fallback'
            }
    
    def batch_analyze(self, texts: list) -> list:
        """
        Analyze sentiment for multiple texts.
        
        Args:
            texts: List of Tamil texts
            
        Returns:
            List of sentiment analysis results
        """
        return [self.analyze(text) for text in texts]
