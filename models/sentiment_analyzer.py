"""
Sentiment Analyzer using XLM-RoBERTa
Performs offline sentiment classification for Tamil text.
"""

import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
from typing import Dict, Tuple, Any
import os

class SentimentAnalyzer:
    """Analyzes sentiment of Tamil text using XLM-RoBERTa."""
    
    def __init__(self, cache_dir: str = "./cache/xlm-roberta"):
        """
        Initialize sentiment analyzer.
        
        Args:
            cache_dir: Directory containing cached model files
        """
        self.cache_dir = cache_dir
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        print(f"Loading XLM-RoBERTa model from {cache_dir}...")
        
        try:
            # Load tokenizer and model from cache
            print("Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                "xlm-roberta-base",
                cache_dir=cache_dir
            )
            
            print("Loading model (this may take a minute)...")
            self.model = AutoModel.from_pretrained(
                "xlm-roberta-base",
                cache_dir=cache_dir
            )
            
            print("Moving model to device...")
            self.model.to(self.device)
            self.model.eval()
            
            print("✅ XLM-RoBERTa model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("Please run 'python setup_models.py' first to download models.")
            raise
        
        # Sentiment keywords for Tamil (simple rule-based enhancement)
        self.positive_keywords = [
            'நன்று', 'சிறப்பு', 'மகிழ்ச்சி', 'அழகு', 'இனிமை', 'நலம்', 
            'புகழ்', 'வாழ்க', 'பெருமை', 'காதல்', 'அன்பு', 'நட்பு',
            'வெற்றி', 'சந்தோஷம்', 'உவகை', 'மகிழ்வு', 'நகை'
        ]
        
        self.negative_keywords = [
            'துன்பம்', 'வருத்தம்', 'கோபம்', 'வெறுப்பு', 'பகை', 'சோகம்',
            'அழுகை', 'தீமை', 'குற்றம்', 'தோல்வி', 'வேதனை', 'கவலை',
            'கசப்பு', 'வலி', 'நோய்', 'பாவம்', 'கொடுமை'
        ]
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """
        Get sentence embedding from XLM-RoBERTa.
        
        Args:
            text: Input Tamil text
            
        Returns:
            Numpy array of embeddings
        """
        # Tokenize
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )
        
        # Move to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Get embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Use [CLS] token embedding (first token)
            embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()
        
        return embedding
    
    def _rule_based_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Simple rule-based sentiment detection based on keywords.
        
        Args:
            text: Input Tamil text
            
        Returns:
            Tuple of (sentiment, confidence)
        """
        positive_count = sum(1 for word in self.positive_keywords if word in text)
        negative_count = sum(1 for word in self.negative_keywords if word in text)
        
        if positive_count > negative_count:
            confidence = min(0.7 + (positive_count * 0.1), 0.95)
            return "POSITIVE", confidence
        elif negative_count > positive_count:
            confidence = min(0.7 + (negative_count * 0.1), 0.95)
            return "NEGATIVE", confidence
        else:
            return "NEUTRAL", 0.5
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of Tamil text.
        
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
            # Get embedding-based analysis
            embedding = self._get_embedding(text)
            
            # Simple heuristic: use mean of embedding values to determine sentiment
            # Positive values tend toward positive sentiment
            embedding_mean = float(np.mean(embedding))
            
            # Get rule-based sentiment
            rule_sentiment, rule_confidence = self._rule_based_sentiment(text)
            
            # Combine both methods
            if embedding_mean > 0.1:
                embedding_sentiment = "POSITIVE"
                embedding_confidence = min(abs(embedding_mean) * 2, 0.9)
            elif embedding_mean < -0.1:
                embedding_sentiment = "NEGATIVE"
                embedding_confidence = min(abs(embedding_mean) * 2, 0.9)
            else:
                embedding_sentiment = "NEUTRAL"
                embedding_confidence = 0.5
            
            # Weighted combination (rule-based gets more weight for clarity)
            if rule_sentiment == embedding_sentiment:
                final_sentiment = rule_sentiment
                final_confidence = (rule_confidence + embedding_confidence) / 2
            else:
                # Rule-based takes precedence
                final_sentiment = rule_sentiment
                final_confidence = rule_confidence
            
            return {
                'sentiment': final_sentiment,
                'confidence': round(final_confidence, 2),
                'method': 'hybrid',
                'details': {
                    'rule_based': rule_sentiment,
                    'embedding_based': embedding_sentiment
                }
            }
            
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            # Fallback to rule-based only
            sentiment, confidence = self._rule_based_sentiment(text)
            return {
                'sentiment': sentiment,
                'confidence': round(confidence, 2),
                'method': 'rule_based_fallback'
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
