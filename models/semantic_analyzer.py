"""
Semantic Analyzer with திருக்குறள் Database
Extracts meaning and literary context from Tamil text.
"""

import json
import os
from typing import Dict, Optional, List
from fuzzywuzzy import fuzz
from .text_processor import TamilTextProcessor

class SemanticAnalyzer:
    """Analyzes semantic meaning of Tamil text using local database."""
    
    def __init__(self, db_path: str = "database/thirukkural_db.json"):
        """
        Initialize semantic analyzer.
        
        Args:
            db_path: Path to திருக்குறள் database
        """
        self.db_path = db_path
        self.processor = TamilTextProcessor()
        self.database = self._load_database()
        
        print(f"✅ Semantic analyzer initialized with {len(self.database)} verses")
    
    def _load_database(self) -> Dict:
        """
        Load திருக்குறள் database from JSON file.
        
        Returns:
            Dictionary containing all verses
        """
        if not os.path.exists(self.db_path):
            print(f"⚠️  Database not found at {self.db_path}, creating sample database...")
            self._create_sample_database()
        
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('thirukkural', {})
        except Exception as e:
            print(f"Error loading database: {e}")
            return {}
    
    def _create_sample_database(self):
        """Create a sample திருக்குறள் database with first 10 verses."""
        sample_data = {
            "thirukkural": {
                "1": {
                    "verse": "அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு",
                    "book": "திருக்குறள்",
                    "section": "கடவுள் வாழ்த்து",
                    "chapter": "கடவுள் வாழ்த்து",
                    "number": "1",
                    "meaning": "அகரம் என்னும் எழுத்து எல்லா எழுத்துகளுக்கும் முதன்மையானது; அதுபோல் ஆதி பகவன் என்று சொல்லப்படும் கடவுள் உலகத்திற்கு முதற்காரணமாக இருக்கிறார்.",
                    "summary": "எழுத்துக்கு அகரம் முதல் போல, உலகிற்கு இறைவன் முதல்."
                },
                "2": {
                    "verse": "கற்க கசடறக் கற்பவை கற்றபின் நிற்க அதற்குத் தக",
                    "book": "திருக்குறள்",
                    "section": "கடவுள் வாழ்த்து",
                    "chapter": "கடவுள் வாழ்த்து",
                    "number": "2",
                    "meaning": "கற்றுக்கொள்ள வேண்டியவற்றைக் குற்றங்கள் நீங்கக் கற்றுக் கொண்டபின், அவற்றின்படி வாழ்ந்து நிற்க வேண்டும்.",
                    "summary": "குற்றமற கற்று, அதன்படி வாழ்க."
                },
                "3": {
                    "verse": "மலர்மிசை ஏகினான் மாணடி சேர்ந்தார் நிலமிசை நீடுவாழ் வார்",
                    "book": "திருக்குறள்",
                    "section": "கடவுள் வாழ்த்து",
                    "chapter": "கடவுள் வாழ்த்து",
                    "number": "3",
                    "meaning": "தாமரை மலரின் மேல் வீற்றிருக்கும் பிரமனால் வணங்கப்பெறும் இறைவனின் திருவடியைச் சார்ந்தவர்கள், இவ்வுலகில் நீண்டகாலம் வாழ்வார்கள்.",
                    "summary": "இறைவன் அடி சேர்ந்தார் நெடுநாள் வாழ்வர்."
                },
                "4": {
                    "verse": "வேண்டுதல் வேண்டாமை இலானடி சேர்ந்தார்க்கு யாண்டும் இடும்பை இல",
                    "book": "திருக்குறள்",
                    "section": "கடவுள் வாழ்த்து",
                    "chapter": "கடவுள் வாழ்த்து",
                    "number": "4",
                    "meaning": "விருப்பு வெறுப்புகள் இல்லாத இறைவனின் திருவடியைச் சேர்ந்தவர்களுக்கு எக்காலத்திலும் துன்பம் இல்லை.",
                    "summary": "இறைவன் அடி சேர்ந்தார்க்கு துன்பம் இல்லை."
                },
                "5": {
                    "verse": "இருள்சேர் இருவினையும் சேரா இறைவன் பொருள்சேர் புகழ்புரிந்தார் மாட்டு",
                    "book": "திருக்குறள்",
                    "section": "கடவுள் வாழ்த்து",
                    "chapter": "கடவுள் வாழ்த்து",
                    "number": "5",
                    "meaning": "இருளைப் போன்ற நன்மை தீமை என்ற இரு வினைகளும், இறைவனின் உண்மையான புகழைப் போற்றுகின்றவர்களிடம் சேராது.",
                    "summary": "இறைவன் புகழ் போற்றுவார்க்கு வினை சேராது."
                },
                "6": {
                    "verse": "பொறிவாயில் ஐந்தவித்தான் பொய்தீர் ஒழுக்க நெறிநின்றார் நீடுவாழ் வார்",
                    "book": "திருக்குறள்",
                    "section": "கடவுள் வாழ்த்து",
                    "chapter": "கடவுள் வாழ்த்து",
                    "number": "6",
                    "meaning": "ஐம்பொறிகளை அடக்கிய இறைவன் காட்டிய பொய்யற்ற ஒழுக்க நெறியில் நின்றவர்கள் நீண்டகாலம் வாழ்வார்கள்.",
                    "summary": "பொய்யற்ற ஒழுக்கத்தில் நிற்பவர் நெடுநாள் வாழ்வர்."
                },
                "7": {
                    "verse": "தனக்குவமை இல்லாதான் தாள்சேர்ந்தார்க்கு அல்லால் மனக்கவலை மாற்றல் அரிது",
                    "book": "திருக்குறள்",
                    "section": "கடவுள் வாழ்த்து",
                    "chapter": "கடவுள் வாழ்த்து",
                    "number": "7",
                    "meaning": "தனக்கு நிகர் இல்லாத இறைவனின் திருவடியைச் சேர்ந்தவர்களைத் தவிர மற்றவர்கள் மனக்கவலையை நீக்கிக்கொள்வது அரிது.",
                    "summary": "இறைவன் அடி சேராதார்க்கு கவலை நீங்காது."
                },
                "8": {
                    "verse": "அறவாழி அந்தணன் தாள்சேர்ந்தார்க்கு அல்லால் பிறவாழி நீந்தல் அரிது",
                    "book": "திருக்குறள்",
                    "section": "கடவுள் வாழ்த்து",
                    "chapter": "கடவுள் வாழ்த்து",
                    "number": "8",
                    "meaning": "அறக்கடல் போன்ற தூயவனான இறைவனின் திருவடியைச் சேர்ந்தவர்களைத் தவிர, மற்றவர்கள் பிறவிக் கடலைக் கடப்பது அரிது.",
                    "summary": "இறைவன் அடி சேராதார் பிறவிக்கடல் கடக்க முடியாது."
                },
                "9": {
                    "verse": "கோளில் பொறியில் குணமிலவே எண்குணத்தான் தாளை வணங்காத் தலை",
                    "book": "திருக்குறள்",
                    "section": "கடவுள் வாழ்த்து",
                    "chapter": "கடவுள் வாழ்த்து",
                    "number": "9",
                    "meaning": "எண்வகை குணங்களை உடைய இறைவனின் திருவடியை வணங்காத தலை, செயல் இல்லாததும், உணர்ச்சி இல்லாததும், பயன் இல்லாததுமாகும்.",
                    "summary": "இறைவன் அடி வணங்காத தலை பயனற்றது."
                },
                "10": {
                    "verse": "குற்றேவல் கொண்டொழுகல் பேதைமை சான்றோர்க்கு அற்றேவல் ஆற்றல் கடை",
                    "book": "திருக்குறள்",
                    "section": "கடவுள் வாழ்த்து",
                    "chapter": "கடவுள் வாழ்த்து",
                    "number": "10",
                    "meaning": "குற்றமுள்ள செயல்களைச் செய்வது அறிவீனம்; அறிஞர்களுக்குக் குற்றமில்லாத தொண்டு செய்வதே மிக உயர்ந்த செயல்.",
                    "summary": "குற்றமற்ற தொண்டே சிறந்த செயல்."
                }
            }
        }
        
        # Create directory if needed
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Save to file
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Sample database created at {self.db_path}")
    
    def _fuzzy_search(self, query: str, threshold: int = 70) -> Optional[Dict]:
        """
        Search for verse using fuzzy matching.
        
        Args:
            query: Search query text
            threshold: Minimum similarity score (0-100)
            
        Returns:
            Best matching verse or None
        """
        best_match = None
        best_score = 0
        
        # Normalize query
        normalized_query = self.processor.normalize_text(query)
        
        for verse_num, verse_data in self.database.items():
            verse_text = verse_data.get('verse', '')
            normalized_verse = self.processor.normalize_text(verse_text)
            
            # Calculate similarity
            score = fuzz.partial_ratio(normalized_query, normalized_verse)
            
            if score > best_score and score >= threshold:
                best_score = score
                best_match = verse_data
                best_match['match_score'] = score
                best_match['verse_number'] = verse_num
        
        return best_match
    
    def analyze(self, text: str) -> Dict:
        """
        Analyze semantic meaning of Tamil text.
        
        Args:
            text: Input Tamil text
            
        Returns:
            Dictionary with semantic analysis
        """
        if not text or len(text.strip()) == 0:
            return {
                'found': False,
                'source': 'unknown',
                'message': 'வெற்று உரை'
            }
        
        # Preprocess text
        cleaned_text = self.processor.preprocess_for_analysis(text)
        
        if not cleaned_text:
            return {
                'found': False,
                'source': 'invalid',
                'message': 'தமிழ் எழுத்துக்கள் இல்லை'
            }
        
        # Search in database
        match = self._fuzzy_search(cleaned_text)
        
        if match:
            # Found in திருக்குறள் database
            return {
                'found': True,
                'source': 'thirukkural',
                'book': match.get('book', 'திருக்குறள்'),
                'section': match.get('section', ''),
                'chapter': match.get('chapter', ''),
                'number': match.get('verse_number', ''),
                'verse': match.get('verse', ''),
                'meaning': match.get('meaning', ''),
                'summary': match.get('summary', ''),
                'confidence': match.get('match_score', 0) / 100
            }
        else:
            # Not found in database - generate generic analysis
            return self._generate_generic_analysis(cleaned_text)
    
    def _generate_generic_analysis(self, text: str) -> Dict:
        """
        Generate generic semantic analysis for unknown text.
        
        Args:
            text: Input text
            
        Returns:
            Generic analysis dictionary
        """
        word_count = self.processor.count_words(text)
        
        return {
            'found': False,
            'source': 'generic',
            'book': 'பொது',
            'section': 'பொது',
            'chapter': '',
            'number': '',
            'verse': text,
            'meaning': f'இந்த உரை {word_count} சொற்களைக் கொண்டுள்ளது. திருக்குறள் தரவுத்தளத்தில் இல்லை.',
            'summary': 'பொதுவான தமிழ் உரை',
            'confidence': 0.3
        }
    
    def search_by_number(self, verse_number: int) -> Optional[Dict]:
        """
        Get verse by குறள் number.
        
        Args:
            verse_number: திருக்குறள் verse number (1-1330)
            
        Returns:
            Verse data or None
        """
        verse_data = self.database.get(str(verse_number))
        if verse_data:
            verse_data['verse_number'] = str(verse_number)
        return verse_data
    
    def get_all_sections(self) -> List[str]:
        """
        Get list of all sections in database.
        
        Returns:
            List of section names
        """
        sections = set()
        for verse_data in self.database.values():
            sections.add(verse_data.get('section', ''))
        return sorted(list(sections))
