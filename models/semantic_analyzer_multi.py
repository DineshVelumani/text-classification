"""
Enhanced Semantic Analyzer for ALL Tamil Literature
Supports திருக்குறள், கம்பராமாயணம், சிலப்பதிகாரம், and more classical Tamil texts
"""

import json
import os
from typing import Dict, Optional, List
from fuzzywuzzy import fuzz
from .text_processor import TamilTextProcessor

class MultiLiteratureSemanticAnalyzer:
    """Analyzes semantic meaning from ALL Tamil classical literature."""
    
    def __init__(self, thirukkural_db: str = "database/tamil_literature_db.json", 
                 kamba_db: str = "database/kamba_ramayanam_db.json"):
        """
        Initialize semantic analyzer with multiple Tamil literature databases.
        
        Args:
            thirukkural_db: Path to Thirukkural database
            kamba_db: Path to Kamba Ramayanam database
        """
        self.thirukkural_db_path = thirukkural_db
        self.kamba_db_path = kamba_db
        self.processor = TamilTextProcessor()
        
        # Load both databases
        self.thirukkural_db = self._load_database(thirukkural_db)
        self.kamba_db = self._load_database(kamba_db)
        
        # Count total verses
        thirukkural_count = len(self.thirukkural_db.get('verses', []))
        kamba_count = len(self.kamba_db.get('verses', []))
        total_verses = thirukkural_count + kamba_count
        
        print(f"✅ Multi-literature analyzer initialized")
        print(f"   📚 Databases loaded successfully")
        print(f"   📖 திருக்குறள்: {thirukkural_count} verses")
        print(f"   📖 கம்ப ராமாயணம்: {kamba_count} verses")
        print(f"   📖 Total verses: {total_verses}")
        print(f"   🔧 CODE VERSION: v5.0_MULTI_BOOK_SUPPORT")
        print(f"   ⚡ SENTENCE DETECTION: STRICT MODE (98% threshold)")
    
    def _load_database(self, db_path: str) -> Dict:
        """
        Load Tamil literature database.
        
        Args:
            db_path: Path to database file
            
        Returns:
            Dictionary containing Tamil literature
        """
        if not os.path.exists(db_path):
            print(f"⚠️  Database not found at {db_path}")
            return {}
        
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading database {db_path}: {e}")
            return {}
    
    def _fuzzy_search_all_books(self, query: str, threshold: int = 60) -> Optional[Dict]:
        """
        Search across ALL Tamil literature (Thirukkural + Kamba Ramayanam) using fuzzy matching.
        
        Args:
            query: Search query text
            threshold: Minimum similarity score (0-100)
            
        Returns:
            Best matching verse from any book or None
        """
        best_match = None
        best_score = 0
        
        # Normalize query
        normalized_query = self.processor.normalize_text(query)
        query_length = len(normalized_query)
        
        # Count words - sentences typically have 3+ words with verbs
        query_words = normalized_query.split()
        query_word_count = len(query_words)
        
        # 🆕 SENTENCE ANALYSIS: Detect if query is a full modern Tamil sentence
        # Modern sentences have verb endings like: கிறேன், கிறோம், வேன், வீர், தேன், etc.
        # Thirukkural verses use archaic Tamil and poetic structures
        
        # Modern verb endings (present, past, future tenses)
        verb_endings = [
            'கிறேன்', 'கிறாய்', 'கிறார்', 'கிறோம்', 'கிறீர்', 'கிறார்கள்',  # Present continuous
            'கிறது', 'கின்றன',  # Neuter present
            'வேன்', 'வாய்', 'வார்', 'வோம்', 'வீர்', 'வார்கள்',  # Future
            'தேன்', 'தாய்', 'தார்', 'தோம்', 'தீர்', 'தார்கள்',  # Past
            'ந்தேன்', 'ந்தாய்', 'ந்தார்', 'ந்தோம்',  # Past compound forms
            'ட்டேன்', 'ட்டாய்', 'ட்டார்', 'ட்டோம்',  # Past compound forms
            'க்கிறேன்', 'ப்பேன்', 'ப்போம்',  # Compound present/future
        ]
        
        # Modern time indicators
        time_indicators = [
            'இன்று', 'நேற்று', 'நாளை', 'இன்றைக்கு', 'நேற்றைக்கு',
            'காலையில்', 'மாலையில்', 'இரவில்', 'மதியம்',
            'இப்போது', 'அப்போது', 'பிறகு', 'முன்பு'
        ]
        
        # Modern objects/nouns (things that didn't exist in ancient times)
        modern_words = [
            'புத்தகம்', 'பள்ளி', 'கார்', 'பேருந்து', 'ரயில்',
            'கணினி', 'போன்', 'டிவி', 'பணம்', 'ஊர்',
            'வீட்டில்', 'கடை', 'மார்க்கெட்', 'ஆபீஸ்', 'வேலை'
        ]
        
        # Check for modern Tamil indicators
        has_modern_verb = any(
            any(word.endswith(ending) for ending in verb_endings)
            for word in query_words
        )
        has_time_indicator = any(word in time_indicators for word in query_words)
        has_modern_word = any(word in modern_words for word in query_words)
        
        # Sentence detection logic
        is_modern_sentence = has_modern_verb or (has_time_indicator and query_word_count >= 2) or has_modern_word
        
        # If query is just 1-3 words, it's likely random text, not a verse
        # Thirukkural verses are typically longer and more poetic
        is_short_query = query_word_count <= 3
        
        # 🆕 STRUCTURAL PRE-CHECK: Check if query looks like verse structure
        # Before applying strict sentence mode, check if it has verse characteristics
        query_lines = normalized_query.count('\n') + 1
        
        # Thirukkural structure: 2 lines, 6-10 words
        looks_like_thirukkural = (query_lines == 2 and 6 <= query_word_count <= 10)
        
        # Kamba structure: longer verses, multiple lines
        kamba_characters = ['இராமன்', 'சீதை', 'லட்சுமணன்', 'இராவணன்', 'அனுமன்', 'தசரதன்']
        has_kamba_character = any(char in normalized_query for char in kamba_characters)
        looks_like_kamba = (query_word_count > 10 or query_lines > 2 or has_kamba_character)
        
        # If query looks like a verse, DON'T apply strict sentence mode
        looks_like_verse = looks_like_thirukkural or looks_like_kamba
        
        # If it's a modern sentence structure (verb + subject/object)
        # OR a short random query (1-3 words)
        # COMPLETELY REJECT unless it's a near-perfect match (actual verse)
        # BUT: If it looks like a verse structure, allow normal matching
        if not looks_like_verse and ((is_modern_sentence and query_word_count >= 2) or is_short_query):
            # This is a complete modern Tamil sentence or random words, not a verse
            # Only allow if it's 98%+ match (meaning it's actually a verse from database)
            strict_sentence_mode = True
            sentence_threshold = 98  # VERY high threshold - only actual verses pass
        else:
            strict_sentence_mode = False
            sentence_threshold = 70  # Normal threshold
        
        # Balanced thresholds - need to match Thirukkural while filtering random text
        # Lower thresholds to match more verses (especially Kamba verses)
        if query_length > 100:
            threshold = 50  # Long verses (both Thirukkural 2 lines and Kamba)
        elif query_length > 50:
            threshold = 48  # Medium verse fragments
        else:
            threshold = 50  # Short fragments or character names
        
        # Override threshold if sentence detected
        if strict_sentence_mode:
            threshold = sentence_threshold
        
        # Check if query is just a number (verse number search)
        is_number_search = normalized_query.strip().isdigit()
        
        # 🆕 MULTI-BOOK SEARCH: Search both Thirukkural and Kamba Ramayanam
        # Search in priority order: Thirukkural first (shorter, more common), then Kamba Ramayanam
        
        books_to_search = [
            ('thirukkural', self.thirukkural_db, 'திருக்குறள்'),
            ('kamba_ramayanam', self.kamba_db, 'கம்ப ராமாயணம்')
        ]
        
        for book_key, book_db, default_title in books_to_search:
            if not book_db or not book_db.get('verses'):
                continue
            
            verses_to_search = book_db.get('verses', [])
            book_name = book_db.get('metadata', {}).get('title', default_title)
            
            # 🆕 BOOK-SPECIFIC DETECTION: Check for Kamba Ramayanam character names
            kamba_characters = ['இராமன்', 'சீதை', 'லட்சுமணன்', 'இராவணன்', 'அனுமன்', 'தசரதன்', 
                              'அனுமன்', 'பரதன்', 'சுக்ரீவன்', 'விபீஷணன்', 'கைகேயி', 'வாலி',
                              'கும்பகர்ணன்', 'இந்திரஜித்', 'ஜடாயு', 'மாரீசன்']
            has_kamba_character = any(char in normalized_query for char in kamba_characters)
            
            # Thirukkural structure detection: 2 lines with approximately 8 words
            # Count lines and words in the query
            query_lines = normalized_query.count('\n') + 1
            query_words_list = normalized_query.split()
            query_word_count = len(query_words_list)
            
            # Thirukkural characteristics:
            # - Exactly 2 lines (one \n)
            # - 6-10 words total (usually 8)
            # - Each line has 3-5 words
            is_thirukkural_structure = (
                query_lines == 2 and 
                6 <= query_word_count <= 10
            )
            
            # Kamba characteristics:
            # - Variable lines (can be 1-4 lines)
            # - Longer verses (usually more than 10 words)
            # - Contains character names
            is_kamba_structure = (
                has_kamba_character or 
                query_word_count > 10 or
                query_lines > 2
            )
            
            # Apply book-specific boost/penalty based on structure match
            # Use stronger boosts and adjust thresholds based on structure
            if book_key == 'thirukkural' and is_thirukkural_structure:
                kamba_boost = 1.35  # Strong boost for Thirukkural structure match
                threshold = min(threshold, 40)  # Lower threshold for Thirukkural structure
            elif book_key == 'kamba_ramayanam' and is_kamba_structure:
                kamba_boost = 1.30  # Strong boost for Kamba structure/character match
                threshold = min(threshold, 42)  # Lower threshold for Kamba structure
            elif book_key == 'thirukkural' and is_kamba_structure:
                kamba_boost = 0.75  # Stronger penalty for mismatch
            elif book_key == 'kamba_ramayanam' and is_thirukkural_structure:
                kamba_boost = 0.75  # Stronger penalty for mismatch
            else:
                kamba_boost = 1.0  # Neutral
            
            for verse_data in verses_to_search:
                verse_num = str(verse_data.get('verse_number', ''))
                
                # If searching by number, match exactly
                if is_number_search:
                    if normalized_query.strip() == verse_num:
                        return {
                            **verse_data,
                            'match_score': 100,
                            'verse_number': verse_num,
                            'book_key': book_key,
                            'book': book_name
                        }
                    continue
                
                # Search in multiple fields
                verse_text = verse_data.get('verse', '')
                meaning_text = verse_data.get('meaning', '')
                chapter_text = verse_data.get('chapter', verse_data.get('kandam', ''))  # Support both Thirukkural (chapter) and Kamba (kandam)
                
                # Normalize texts
                normalized_verse = self.processor.normalize_text(verse_text)
                normalized_meaning = self.processor.normalize_text(meaning_text)
                normalized_chapter = self.processor.normalize_text(chapter_text)
                
                # Calculate similarity - ONLY verse text and chapter name, NO meaning field
                verse_score = 0
                chapter_score = 0
                
                # Only check verse text if it's not a placeholder
                if not verse_text.startswith('திருக்குறள்') and not verse_text.startswith('[திருக்குறள்'):
                    # First check for exact or near-exact match
                    if normalized_query == normalized_verse:
                        verse_score = 100 * kamba_boost  # Perfect match
                    elif normalized_query in normalized_verse or normalized_verse in normalized_query:
                        # Substring match - this is likely a legitimate verse!
                        # Calculate how much of the query matches the verse
                        query_len = len(normalized_query)
                        verse_len = len(normalized_verse)
                        
                        if query_len >= verse_len * 0.8:
                            # Query is 80%+ of verse length - very likely the verse itself
                            verse_score = 95
                        elif query_len >= verse_len * 0.5:
                            # Query is 50-80% of verse - partial verse
                            verse_score = 85
                        else:
                            # Query is <50% of verse - verify word overlap
                            query_words = set(normalized_query.split())
                            verse_words = set(normalized_verse.split())
                            common_words = query_words.intersection(verse_words)
                            overlap_ratio = len(common_words) / len(query_words) if query_words else 0
                            
                            # Require at least 50% word overlap for short substring matches
                            if overlap_ratio >= 0.5:
                                verse_score = 80
                            else:
                                verse_score = int(70 * overlap_ratio)  # Proportional score
                    else:
                        # Use fuzzy matching for partial matches
                        token_score = fuzz.token_set_ratio(normalized_query, normalized_verse)
                        partial_score = fuzz.partial_ratio(normalized_query, normalized_verse)
                        verse_score = max(token_score, partial_score)
                        
                        # EXCEPTION: If fuzzy score is near-perfect (>=95%), check if it's legitimate
                        # This handles compound words where word boundaries differ
                        # Example: "நின்றாருளஎல்லாம்" vs "நின்றாருள் எல்லாம்"
                        # BUT: Also prevent false positives from substring matches
                        # Example: "நான் செல்வேன்" should NOT match verse with "நான்கும்"
                        if verse_score >= 95:
                            # Check if query length is substantial (at least 60% of verse length)
                            # This ensures it's the actual verse, not random text with coincidental words
                            query_len = len(normalized_query)
                            verse_len = len(normalized_verse)
                            length_ratio = query_len / verse_len if verse_len > 0 else 0
                            
                            if length_ratio >= 0.6:
                                # Query is 60%+ of verse length - likely legitimate match with compound words
                                # Keep the high verse_score
                                pass
                            else:
                                # Query is too short compared to verse - likely substring coincidence
                                # Apply normal word overlap validation
                                query_words = set(normalized_query.split())
                                verse_words = set(normalized_verse.split())
                                common_words = query_words.intersection(verse_words)
                                overlap_ratio = len(common_words) / len(query_words) if query_words else 0
                                
                                # For short queries with coincidental high fuzzy score
                                if len(query_words) <= 3:
                                    if overlap_ratio < 1.0:
                                        verse_score = 0  # Reject - coincidental match
                                else:
                                    if overlap_ratio < 0.6:
                                        verse_score = 0  # Reject - coincidental match
                        else:
                            # CRITICAL: STRICT word overlap validation 
                            # Prevents random text matches while allowing Thirukkural matches
                            # This is the KEY to preventing false positives!
                            query_words = set(normalized_query.split())
                            verse_words = set(normalized_verse.split())
                            common_words = query_words.intersection(verse_words)
                            overlap_ratio = len(common_words) / len(query_words) if query_words else 0
                            
                            # Word overlap validation - balance verse matching with sentence rejection
                            if len(query_words) <= 3:
                                # Short queries (1-3 words) - require high word overlap
                                if overlap_ratio < 0.7:  # At least 70% words must match
                                    verse_score = int(verse_score * overlap_ratio)
                            else:
                                # Longer queries (4+ words)
                                # Allow more flexibility for verse matching
                                if verse_score >= 85:
                                    # Very high fuzzy - but still require actual word matches
                                    if overlap_ratio < 0.4:  # Less than 40% word overlap
                                        verse_score = int(verse_score * overlap_ratio * 1.5)
                                    elif overlap_ratio < 0.6:  # 40-60% overlap
                                        verse_score = int(verse_score * 0.85)  # Small penalty
                                else:
                                    # Medium fuzzy score (70-84) - require 50% word overlap minimum
                                    if overlap_ratio < 0.5:  # Less than 50% overlap
                                        verse_score = int(verse_score * overlap_ratio * 1.2)
                                    elif overlap_ratio < 0.7:  # 50-70% overlap
                                        verse_score = int(verse_score * 0.65)  # Significant penalty
                
                # Search chapter name ONLY for short queries (likely chapter searches)
                if query_length < 30:  # Chapter names are short
                    chapter_score = fuzz.partial_ratio(normalized_query, normalized_chapter)
                    # Require good match for chapter
                    if chapter_score < 70:
                        chapter_score = 0
                
                # Use the best score (NO meaning field included!)
                score = max(verse_score, chapter_score)
                
                # 🆕 SENTENCE REJECTION: If in strict sentence mode and score < 95%, reject
                # Modern sentences should NOT match verses unless it's a near-perfect match
                if strict_sentence_mode and score < 95:
                    score = 0  # Reject - this is a modern sentence, not an actual verse
                
                if score > best_score and score >= threshold:
                    best_score = score
                    best_match = verse_data.copy()
                    best_match['match_score'] = score
                    best_match['verse_number'] = verse_num
                    best_match['book_key'] = book_key
                    best_match['book'] = book_name
                    best_match['boost_applied'] = kamba_boost  # Track which boost was used
        
        # 🆕 CONTINUE SEARCHING ALL BOOKS: Don't return early - search all books
        # and return the match with the HIGHEST boosted score
        # This ensures Kamba verses with character names aren't misidentified as Thirukkural
        
        # 🆕 FINAL SENTENCE CHECK: Even if we found a match, reject if it's clearly a modern sentence
        # and the match score is not extremely high (< 95%)
        if best_match and strict_sentence_mode and best_match.get('match_score', 0) < 95:
            # This is likely a modern sentence that coincidentally matches some verse words
            # Example: "நான் செல்வேன்" might match verse with "நான்" and "செல்"
            return None  # Reject the match
        
        return best_match
    
    def analyze(self, text: str) -> Dict:
        """
        Analyze semantic meaning from ALL Tamil literature.
        
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
        
        # Search across all Tamil literature
        match = self._fuzzy_search_all_books(cleaned_text)
        
        if match:
            # Found in Tamil literature database - return ALL available fields
            result = {
                'found': True,
                'source': match.get('book_key', 'unknown'),
                'book': match.get('tamil_book_name', match.get('book', '')),
                'section': match.get('section', ''),
                'chapter': match.get('chapter', ''),
                'number': match.get('verse_number', ''),
                'verse': match.get('verse', ''),
                'meaning': match.get('meaning', ''),
                'summary': match.get('summary', ''),
                'confidence': match.get('match_score', 0) / 100
            }
            
            # Add optional fields if they exist in the database
            if 'english_meaning' in match:
                result['english_meaning'] = match['english_meaning']
            
            if 'theme' in match:
                result['theme'] = match['theme']
            
            if 'moral' in match:
                result['moral'] = match['moral']
            
            if 'author' in match:
                result['author'] = match['author']
            
            if 'characters' in match:
                result['characters'] = match['characters']
            
            # Add book metadata
            if match.get('book_key'):
                # Get the appropriate database based on book_key
                book_db = self.thirukkural_db if match['book_key'] == 'thirukkural' else self.kamba_db
                book_meta = book_db.get('metadata', {})
                result['book_metadata'] = {
                    'tamil_title': book_meta.get('tamil_title', book_meta.get('title', '')),
                    'english_title': book_meta.get('english_title', ''),
                    'author': book_meta.get('author', ''),
                    'period': book_meta.get('period', ''),
                    'category': book_meta.get('category', '')
                }
            
            return result
        else:
            # Not found in database
            return self._generate_generic_analysis(cleaned_text)
    
    def _generate_generic_analysis(self, text: str) -> Dict:
        """
        Generate analysis for random Tamil text with word meanings and sentiment.
        
        Args:
            text: Input text
            
        Returns:
            Analysis dictionary with word meanings and sentiment
        """
        # Get word-by-word meanings
        meaning = self._generate_contextual_meaning(text)
        
        # Analyze sentiment
        sentiment_result = self._analyze_sentiment(text)
        
        return {
            'found': False,
            'source': 'random_text',
            'book': 'பொது தமிழ் உரை',
            'section': '',
            'chapter': '',
            'number': '',
            'verse': '',
            'meaning': meaning,
            'summary': '',
            'english_meaning': '',
            'theme': '',
            'moral': '',
            'confidence': 0.0,
            'sentiment': sentiment_result  # Add sentiment analysis
        }
        
        # Generate actual meaningful analysis of the text
        meaning = f"""📊 இந்த உரை திருக்குறள் தரவுத்தளத்தில் இல்லை

� உரையின் பொருள்:
{contextual_meaning}

💡 கருத்து: {self._identify_theme(text)}

🎯 தொகுப்பு:
{summary}

⭐ நீதி/படிப்பினை:
{moral}

� குறிப்பு: 
• இது திருக்குறள் அல்ல - பொது தமிழ் உரை
• திருக்குறள் தேட: குறள் எண் (1-1330) அல்லது அதிகாரம் பெயரை உள்ளிடவும்
• தரவுத்தளம்: {self._get_total_verses():,} திருக்குறள்கள்"""
        
        return {
            'found': False,
            'source': 'random_text',
            'book': 'பொது தமிழ் உரை',
            'section': '',
            'chapter': '',
            'number': '',
            'verse': text,
            'meaning': contextual_meaning,
            'summary': f"""<strong>உரையின் பொருள்:</strong><br>{contextual_meaning}<br><br><strong>கருத்து:</strong> {self._identify_theme(text)}<br><br><strong>விரிவு:</strong><br>{summary}<br><br><strong>படிப்பினை:</strong><br>{moral}<br><br><hr><strong>குறிப்பு:</strong> இது திருக்குறள் அல்ல. திருக்குறள் தேட: குறள் எண் (1-1330)""",
            'english_meaning': '',
            'theme': '',
            'moral': '',
            'confidence': 0.0
        }
    
    def _get_database_stats(self) -> str:
        """Get database statistics as a formatted string"""
        # Count verses from both databases
        thirukkural_count = len(self.thirukkural_db.get('verses', []))
        kamba_count = len(self.kamba_db.get('verses', []))
        total_verses = thirukkural_count + kamba_count
        
        return f"திருக்குறள்: {thirukkural_count:,} பாடல்கள், கம்ப ராமாயணம்: {kamba_count:,} பாடல்கள் (மொத்தம்: {total_verses:,})"
    
    def _get_total_verses(self) -> int:
        """Get total number of verses across all books"""
        return len(self.thirukkural_db.get('verses', [])) + len(self.kamba_db.get('verses', []))
    
    def _extract_moral(self, text: str) -> str:
        """Extract moral/lesson from text based on keywords"""
        morals = {
            'அறம்': 'நீதியான வாழ்க்கை வாழ வேண்டும்',
            'கல்': 'கல்வியே மனிதனின் உண்மையான செல்வம்',
            'காதல்': 'உண்மையான அன்பு தூய்மையானது',
            'நன்றி': 'உதவி செய்தவரை மறக்கக்கூடாது',
            'நட்பு': 'நல்ல நண்பர்கள் வாழ்வின் அரும்பொருள்',
            'பொறாமை': 'பொறாமை தீய குணம், தவிர்க்க வேண்டும்',
            'பொய்': 'வாய்மையே வெல்லும், பொய் தோற்கும்',
            'செல்வம்': 'பொருள் சேர்த்து பயன்படுத்த வேண்டும்',
            'கோபம்': 'கோபம் மனிதனின் எதிரி',
            'பொறுமை': 'பொறுமை கொண்டு செயல்பட வேண்டும்',
        }
        
        for keyword, moral in morals.items():
            if keyword in text:
                return moral
        
        return 'தமிழ் இலக்கியம் வாழ்க்கைக்கு வழிகாட்டும் ஒளி'
    
    def _guess_literature_source(self, text: str) -> str:
        """Guess which Tamil literature this might be from based on style"""
        text_lower = text.lower()
        
        # Check for திருக்குறள் patterns (short, 2 lines)
        if any(word in text_lower for word in ['கல்', 'கற்', 'அறம்', 'நன்றி']):
            if len(text) < 150:
                return 'திருக்குறள் (அனுமானம்)'
        
        # Check for epic style (long narratives)
        if any(word in text_lower for word in ['இராமன்', 'சீதை', 'கண்ணகி', 'கோவலன்', 'மாதவி']):
            return 'காப்பியம் (சிலப்பதிகாரம்/கம்பராமாயணம்)'
        
        # Check for ஆத்திசூடி style (very short moral)
        if len(text) < 40 and any(word in text_lower for word in ['விரும்பு', 'செய்', 'கூடாது']):
            return 'ஆத்திசூடி அல்லது நாலடியார் (அனுமானம்)'
        
        # Check for சங்க இலக்கியம் style
        if any(word in text_lower for word in ['யாதும்', 'யாவரும்', 'ஊரே', 'நாடு', 'மக்கள்']):
            return 'சங்க இலக்கியம் (புறநானூறு/எட்டுத்தொகை)'
        
        # Check for devotional
        if any(word in text_lower for word in ['சிவன்', 'பெருமான்', 'கடவுள்', 'திருவடி']):
            return 'பக்தி இலக்கியம் (தேவாரம்/திருவாசகம்)'
        
        return 'தமிழ் இலக்கியம் (பொது)'
    
    def _generate_contextual_meaning(self, text: str) -> str:
        """Generate actual word-by-word meaning of the text"""
        # Comprehensive Tamil to English/meaning dictionary
        word_meanings = {
            # Pronouns
            'நான்': 'I', 'நாம்': 'we (inclusive)', 'நாங்கள்': 'we', 'எங்கள்': 'our', 'என்': 'my',
            'நீ': 'you (singular)', 'நீங்கள்': 'you (plural)', 'உங்கள்': 'your',
            'அவன்': 'he', 'அவள்': 'she', 'அவர்': 'they/he/she (respectful)', 'அவர்கள்': 'they',
            'இவன்': 'this person (male)', 'இவள்': 'this person (female)', 'இவர்': 'this person (respectful)',
            'யார்': 'who', 'எது': 'which/what', 'என்ன': 'what', 'எப்படி': 'how', 'ஏன்': 'why',
            'எங்கே': 'where', 'எப்போது': 'when', 'எவ்வளவு': 'how much',
            
            # Time words
            'இன்று': 'today', 'நேற்று': 'yesterday', 'நாளை': 'tomorrow', 
            'மறுநாள்': 'day after tomorrow', 'நேற்று முன்தினம்': 'day before yesterday',
            'காலை': 'morning', 'மதியம்': 'afternoon', 'மாலை': 'evening', 'இரவு': 'night',
            'இப்போது': 'now', 'பிறகு': 'later', 'முன்': 'before', 'பின்': 'after',
            'எப்போதும்': 'always', 'சில நேரங்களில்': 'sometimes', 'அரிதாக': 'rarely',
            
            # Food & Eating
            'சாப்பாடு': 'food', 'உணவு': 'food/meal', 'உண்ண': 'to eat',
            'சாப்பிட்டேன்': 'I ate', 'சாப்பிட்டான்': 'he ate', 'சாப்பிட்டாள்': 'she ate', 'சாப்பிட்டார்': 'ate (respectful)',
            'சாப்பிடுவேன்': 'will eat', 'சாப்பிடுகிறேன்': 'am eating', 'சாப்பிடுகிறான்': 'is eating (he)',
            'குடித்தேன்': 'drank', 'குடிக்கிறேன்': 'am drinking', 'குடிப்பேன்': 'will drink',
            'சமைத்தேன்': 'cooked', 'சமைக்கிறேன்': 'am cooking', 'சமைப்பேன்': 'will cook',
            'தண்ணீர்': 'water', 'பால்': 'milk', 'சாதம்': 'rice', 'காய்கறி': 'vegetables',
            
            # Movement verbs
            'செல்ல': 'to go', 'சென்றேன்': 'I went', 'சென்றான்': 'he went', 'சென்றாள்': 'she went',
            'போ': 'go', 'போக': 'to go', 'போகிறேன்': 'am going', 'போகிறான்': 'is going (he)', 
            'போகிறாள்': 'is going (she)', 'போகிறார்': 'is going (respectful)', 'போகிறார்கள்': 'are going',
            'போனேன்': 'I went', 'போனான்': 'he went', 'போனாள்': 'she went', 'போனார்': 'went (respectful)',
            'போவேன்': 'will go', 'போவான்': 'will go (he)', 'போவாள்': 'will go (she)', 'போவார்': 'will go (respectful)',
            'வா': 'come', 'வர': 'to come', 'வருகிறேன்': 'am coming', 'வருகிறான்': 'is coming (he)',
            'வருகிறாள்': 'is coming (she)', 'வருகிறார்': 'is coming (respectful)',
            'வந்தேன்': 'I came', 'வந்தான்': 'he came', 'வந்தாள்': 'she came', 'வந்தார்': 'came (respectful)',
            'வருவேன்': 'will come', 'வருவான்': 'will come (he)', 'வருவாள்': 'will come (she)',
            'செல்கிறேன்': 'am going', 'செல்வேன்': 'will go', 'செல்லாமல்': 'without going',
            'ஓடினேன்': 'ran', 'ஓடுகிறேன்': 'am running', 'ஓடுவேன்': 'will run',
            'ஓடுகிறான்': 'is running (he)', 'ஓடுகிறாள்': 'is running (she)',
            'நடந்தேன்': 'walked', 'நடக்கிறேன்': 'am walking', 'நடப்பேன்': 'will walk',
            'நடக்கிறது': 'is happening/walking', 'நடந்தது': 'happened',
            
            # Common verbs with subject variations
            'பெய்யுது': 'is raining', 'பெய்கிறது': 'is raining', 'பெய்யும்': 'will rain',
            'பெய்தது': 'rained', 'பெய்ய': 'to rain',
            'இருக்கிறேன்': 'am (there)', 'இருக்கிறான்': 'is (there - he)', 'இருக்கிறாள்': 'is (there - she)',
            'இருக்கிறது': 'is (there - thing)', 'இருக்கிறார்': 'is (there - respectful)',
            'இருந்தேன்': 'was (I)', 'இருந்தான்': 'was (he)', 'இருந்தாள்': 'was (she)', 'இருந்தது': 'was (thing)',
            'இருப்பேன்': 'will be', 'இருப்பான்': 'will be (he)', 'இருப்பாள்': 'will be (she)',
            
            # Common nouns with cases
            'பையன்': 'boy', 'பையன்கள்': 'boys', 'பெண்': 'girl', 'பெண்கள்': 'girls',
            'மனிதன்': 'man', 'மனிதர்கள்': 'people', 'பெண்மணி': 'woman',
            'குழந்தை': 'child', 'குழந்தைகள்': 'children', 'குட்டி': 'small child/baby',
            'மாணவன்': 'student (male)', 'மாணவி': 'student (female)', 'மாணவர்கள்': 'students',
            'ஆசிரியர்': 'teacher', 'தலைவர்': 'leader/head', 'நண்பன்': 'friend (male)',
            'தோழன்': 'friend/companion (male)', 'தோழி': 'friend (female)',
            
            # Body parts
            'தலை': 'head', 'கை': 'hand/arm', 'கால்': 'leg/foot', 'கண்': 'eye', 'கண்கள்': 'eyes',
            'காது': 'ear', 'மூக்கு': 'nose', 'வாய்': 'mouth', 'பல்': 'tooth', 'நாக்கு': 'tongue',
            'முகம்': 'face', 'மூளை': 'brain', 'இதயம்': 'heart', 'வயிறு': 'stomach',
            
            # Animals
            'நாய்': 'dog', 'பூனை': 'cat', 'பசு': 'cow', 'குதிரை': 'horse', 'யானை': 'elephant',
            'சிங்கம்': 'lion', 'புலி': 'tiger', 'குரங்கு': 'monkey', 'பறவை': 'bird',
            'மீன்': 'fish', 'பாம்பு': 'snake', 'கோழி': 'chicken', 'ஆடு': 'goat/sheep',
            
            # Food items
            'சாதம்': 'cooked rice', 'சோறு': 'rice/food', 'இட்லி': 'idli', 'தோசை': 'dosa',
            'சாம்பார்': 'sambar', 'ரசம்': 'rasam', 'கூட்டு': 'kootu/curry',
            'பொரியல்': 'poriyal/stir-fry', 'வடை': 'vada', 'பொங்கல்': 'pongal',
            'அப்பளம்': 'papad', 'ஊறுகாய்': 'pickle', 'இனிப்பு': 'sweet/dessert',
            'காபி': 'coffee', 'டீ': 'tea', 'பால்': 'milk', 'தண்ணீர்': 'water',
            'சாறு': 'juice', 'பழம்': 'fruit', 'காய்கறி': 'vegetable',
            
            # Places
            'பள்ளி': 'school', 'பள்ளிக்கு': 'to school', 'பள்ளியில்': 'at school',
            'கல்லூரி': 'college', 'பல்கலைக்கழகம்': 'university',
            'அலுவலகம்': 'office', 'அலுவலகத்தில்': 'at office', 'அலுவலகத்திற்கு': 'to office',
            'வீடு': 'house/home', 'வீட்டில்': 'at home', 'வீட்டிற்கு': 'to home',
            'கடை': 'shop', 'சந்தை': 'market', 'மருத்துவமனை': 'hospital',
            'கோவில்': 'temple', 'தேவாலயம்': 'church', 'மசூதி': 'mosque',
            'பூங்கா': 'park', 'கடற்கரை': 'beach', 'மலை': 'mountain',
            
            # Actions & Verbs (Daily Use)
            'பார்த்தேன்': 'I saw/watched', 'பார்க்கிறேன்': 'am seeing', 'பார்ப்பேன்': 'will see',
            'படித்தேன்': 'I read/studied', 'படிக்கிறேன்': 'am reading', 'படிப்பேன்': 'will read',
            'எழுதினேன்': 'I wrote', 'எழுதுகிறேன்': 'am writing', 'எழுதுவேன்': 'will write',
            'பேசினேன்': 'I spoke', 'பேசுகிறேன்': 'am speaking', 'பேசுவேன்': 'will speak',
            'விளையாடினேன்': 'I played', 'விளையாடுகிறேன்': 'am playing', 'விளையாடுவேன்': 'will play',
            'தூங்கினேன்': 'I slept', 'தூங்குகிறேன்': 'am sleeping', 'தூங்குவேன்': 'will sleep',
            'எழுந்தேன்': 'I woke up', 'எழுகிறேன்': 'am waking up', 'எழுவேன்': 'will wake up',
            'வேலை செய்தேன்': 'I worked', 'வேலை செய்கிறேன்': 'am working', 'வேலை செய்வேன்': 'will work',
            'கற்றேன்': 'I learned', 'கற்கிறேன்': 'am learning', 'கற்பேன்': 'will learn',
            'கொடுத்தேன்': 'I gave', 'கொடுக்கிறேன்': 'am giving', 'கொடுப்பேன்': 'will give',
            'எடுத்தேன்': 'I took', 'எடுக்கிறேன்': 'am taking', 'எடுப்பேன்': 'will take',
            'வாங்கினேன்': 'I bought', 'வாங்குகிறேன்': 'am buying', 'வாங்குவேன்': 'will buy',
            'விற்றேன்': 'I sold', 'விற்கிறேன்': 'am selling', 'விற்பேன்': 'will sell',
            
            # More Common Daily Verbs
            'செய்': 'do/make', 'செய்தேன்': 'I did', 'செய்கிறேன்': 'am doing', 'செய்வேன்': 'will do',
            'செய்கிறதே': 'is doing', 'செய்யாமல்': 'without doing', 'செய்து': 'having done',
            'வீழ்ந்தேன்': 'I fell', 'வீழ்கிறேன்': 'am falling', 'வீழ்வேன்': 'will fall',
            'வீழ்ந்திடாமல்': 'without falling', 'வீழ்ந்திடாதே': 'don\'t fall',
            'தாங்கினேன்': 'I bore/endured', 'தாங்குகிறேன்': 'am bearing', 'தாங்குவேன்': 'will bear',
            'தாங்கிக்கொள்ள': 'to bear/endure', 'தாங்கிக்கொண்டு': 'bearing/enduring',
            'உதவினேன்': 'I helped', 'உதவுகிறேன்': 'am helping', 'உதவுவேன்': 'will help',
            'கேட்டேன்': 'I asked/heard', 'கேட்கிறேன்': 'am asking/hearing', 'கேட்பேன்': 'will ask/hear',
            'சொன்னேன்': 'I said', 'சொல்கிறேன்': 'am saying', 'சொல்வேன்': 'will say',
            'நினைத்தேன்': 'I thought', 'நினைக்கிறேன்': 'am thinking', 'நினைப்பேன்': 'will think',
            'விரும்பினேன்': 'I wanted/liked', 'விரும்புகிறேன்': 'am wanting', 'விரும்புவேன்': 'will want',
            'முயற்சித்தேன்': 'I tried', 'முயற்சிக்கிறேன்': 'am trying', 'முயற்சிப்பேன்': 'will try',
            'நம்பினேன்': 'I believed', 'நம்புகிறேன்': 'am believing', 'நம்புவேன்': 'will believe',
            'மறந்தேன்': 'I forgot', 'மறக்கிறேன்': 'am forgetting', 'மறப்பேன்': 'will forget',
            'நிறுத்தினேன்': 'I stopped', 'நிறுத்துகிறேன்': 'am stopping', 'நிறுத்துவேன்': 'will stop',
            'தொடர்ந்தேன்': 'I continued', 'தொடர்கிறேன்': 'am continuing', 'தொடர்வேன்': 'will continue',
            
            # Common words & Adjectives
            'ஆம்': 'yes', 'இல்லை': 'no', 'சரி': 'okay/correct', 'தவறு': 'wrong/mistake',
            'நல்ல': 'good', 'கெட்ட': 'bad', 'பெரிய': 'big', 'சிறிய': 'small',
            'புதிய': 'new', 'பழைய': 'old', 'இளம்': 'young', 'வயதான': 'old (age)',
            'வேகமாக': 'fast', 'மெதுவாக': 'slow', 'அதிகம்': 'more', 'குறைவு': 'less',
            'உயரம்': 'tall/height', 'தாழ்வு': 'short/low',
            'அழகான': 'beautiful', 'அழகு': 'beauty', 'நேர்மை': 'honesty', 'உண்மை': 'truth',
            'பொய்': 'lie', 'தெளிவு': 'clarity', 'சுத்தம்': 'cleanliness', 'தூய்மை': 'purity',
            'எளிது': 'easy', 'எளிமை': 'simplicity', 'கடினம்': 'difficult', 'சிரமம்': 'difficulty',
            
            # Daily Needs & Activities (Extended)
            'சாப்பிட்டேன்': 'I ate', 'சாப்பிடுகிறேன்': 'am eating', 'சாப்பிடுவேன்': 'will eat',
            'சாப்பிடுகிறான்': 'is eating (he)', 'சாப்பிடுகிறாள்': 'is eating (she)', 'சாப்பிடுகிறது': 'is eating (it)',
            'குடித்தேன்': 'I drank', 'குடிக்கிறேன்': 'am drinking', 'குடிப்பேன்': 'will drink',
            'குடிக்கிறான்': 'is drinking (he)', 'குடிக்கிறாள்': 'is drinking (she)',
            'சமைத்தேன்': 'I cooked', 'சமைக்கிறேன்': 'am cooking', 'சமைப்பேன்': 'will cook',
            'கழுவினேன்': 'I washed', 'கழுவுகிறேன்': 'am washing', 'கழுவுவேன்': 'will wash',
            'துடைத்தேன்': 'I cleaned/wiped', 'துடைக்கிறேன்': 'am cleaning', 'துடைப்பேன்': 'will clean',
            'வாழ்ந்தேன்': 'I lived', 'வாழ்கிறேன்': 'am living', 'வாழ்வேன்': 'will live',
            'வாழ்கிறான்': 'is living (he)', 'வாழ்கிறாள்': 'is living (she)',
            'நடந்தேன்': 'I walked', 'நடக்கிறேன்': 'am walking', 'நடப்பேன்': 'will walk',
            'ஓடினேன்': 'I ran', 'ஓடுகிறேன்': 'am running', 'ஓடுவேன்': 'will run',
            'குதித்தேன்': 'I jumped', 'குதிக்கிறேன்': 'am jumping', 'குதிப்பேன்': 'will jump',
            'உட்கார்ந்தேன்': 'I sat', 'உட்காருகிறேன்': 'am sitting', 'உட்காருவேன்': 'will sit',
            'நின்றேன்': 'I stood', 'நிற்கிறேன்': 'am standing', 'நிற்பேன்': 'will stand',
            'படுத்தேன்': 'I lay down', 'படுக்கிறேன்': 'am lying down', 'படுப்பேன்': 'will lie down',
            'தூங்குகிறான்': 'is sleeping (he)', 'தூங்குகிறாள்': 'is sleeping (she)',
            'விளையாடுகிறான்': 'is playing (he)', 'விளையாடுகிறாள்': 'is playing (she)',
            'படிக்கிறான்': 'is reading (he)', 'படிக்கிறாள்': 'is reading (she)',
            'எழுதுகிறான்': 'is writing (he)', 'எழுதுகிறாள்': 'is writing (she)',
            'பேசுகிறான்': 'is speaking (he)', 'பேசுகிறாள்': 'is speaking (she)',
            
            # Emotions & States (Basic)
            'சந்தோஷம்': 'happiness', 'மகிழ்ச்சி': 'joy', 'வருத்தம்': 'sorrow', 'கோபம்': 'anger',
            'அச்சம்': 'fear', 'ஆச்சரியம்': 'surprise', 'காதல்': 'love', 'வெறுப்பு': 'hatred',
            'நோய்': 'disease', 'ஆரோக்கியம்': 'health', 'நன்றாக': 'well', 'மோசமாக': 'badly',
            'அமைதி': 'peace/calm', 'அன்பு': 'love', 'பாசம்': 'affection',
            'பொறாமை': 'jealousy', 'நம்பிக்கை': 'hope/trust', 'ஏமாற்றம்': 'disappointment',
            'மகிழ்வு': 'delight', 'துக்கம்': 'sorrow/sadness', 'கவலை': 'worry/anxiety', 'பயம்': 'fear',
            
            # Greetings & Common Phrases
            'வணக்கம்': 'greetings/hello', 'வாருங்கள்': 'welcome/come', 'போகலாம்': 'let\'s go',
            'வாங்க': 'come (informal)', 'போங்க': 'go (formal)', 'இருங்கள்': 'stay/be',
            'தயவுசெய்து': 'please', 'நன்றி': 'thank you', 'மன்னிக்கவும்': 'sorry/excuse me',
            'பரவாயில்லை': 'it\'s okay/no problem', 'சரிதான்': 'that\'s right', 'தெரியாது': 'don\'t know',
            'தெரியும்': 'know/known', 'புரியுது': 'understand', 'புரியல': 'don\'t understand',
            
            # Literature words
            'அறம்': 'virtue/righteousness', 'பொருள்': 'wealth/meaning', 'இன்பம்': 'pleasure',
            'கல்': 'education/learning', 'கல்வி': 'education', 'அறிவு': 'knowledge',
            'வேந்தன்': 'king/ruler', 'செல்வம்': 'wealth', 'நன்றி': 'gratitude',
            'நட்பு': 'friendship', 'போர்': 'war', 'உண்மை': 'truth', 'பொய்': 'lie',
            'துன்பம்': 'suffering',
            
            # Colors
            'சிவப்பு': 'red', 'நீலம்': 'blue', 'பச்சை': 'green', 'மஞ்சள்': 'yellow',
            'வெள்ளை': 'white', 'கருப்பு': 'black', 'சாம்பல்': 'grey', 'பழுப்பு': 'brown',
            'ஆரஞ்சு': 'orange', 'இளஞ்சிவப்பு': 'pink', 'ஊதா': 'purple',
            
            # Weather & Nature
            'வானம்': 'sky', 'மேகம்': 'cloud', 'மழை': 'rain', 'காற்று': 'wind',
            'வெயில்': 'sun/sunshine', 'குளிர்': 'cold', 'வெப்பம்': 'heat',
            'மரம்': 'tree', 'பூ': 'flower', 'பழம்': 'fruit', 'கடல்': 'sea',
            'மலை': 'mountain', 'ஆறு': 'river', 'ஏரி': 'lake', 'வயல்': 'field',
            
            # Numbers
            'ஒன்று': 'one', 'இரண்டு': 'two', 'மூன்று': 'three', 'நான்கு': 'four', 'ஐந்து': 'five',
            'ஆறு': 'six', 'ஏழு': 'seven', 'எட்டு': 'eight', 'ஒன்பது': 'nine', 'பத்து': 'ten',
            
            # Family
            'அம்மா': 'mother', 'அப்பா': 'father', 'தாய்': 'mother', 'தந்தை': 'father',
            'அண்ணா': 'elder brother', 'அக்கா': 'elder sister', 'தம்பி': 'younger brother',
            'தங்கை': 'younger sister', 'மகன்': 'son', 'மகள்': 'daughter',
            
            # Conjunctions & Prepositions
            'மற்றும்': 'and', 'அல்லது': 'or', 'ஆனால்': 'but', 'என்பதால்': 'because',
            'அதனால்': 'therefore', 'உடன்': 'with', 'இல்லாமல்': 'without',
            'மேல்': 'above/on', 'கீழ்': 'below/under', 'உள்ளே': 'inside', 'வெளியே': 'outside',
            'முன்': 'front/before', 'பின்': 'back/after', 'அருகில்': 'near', 'தூரம்': 'far',
            'எனவே': 'therefore', 'ஏனெனில்': 'because', 'இருப்பினும்': 'however',
            'ஆகையால்': 'hence', 'மேலும்': 'moreover/also', 'அதேபோல்': 'likewise',
            'க்கு': 'to (suffix)', 'இல்': 'in/at (suffix)', 'ஆல்': 'by (suffix)',
            
            # Possessives & Demonstratives
            'இது': 'this', 'அது': 'that', 'என்னுடைய': 'my', 'உன்னுடைய': 'your',
            'அவனுடைய': 'his', 'அவளுடைய': 'her', 'நம்முடைய': 'our',
            'இவை': 'these', 'அவை': 'those', 'எல்லாம்': 'all/everything',
            'சில': 'some/few', 'பல': 'many', 'அனைத்தும்': 'everything',
            
            # Time & Place
            'இன்று': 'today', 'நேற்று': 'yesterday', 'நாளை': 'tomorrow',
            'இப்போது': 'now', 'பின்பு': 'later/then', 'முன்பு': 'before/earlier',
            'காலை': 'morning', 'மதியம்': 'afternoon', 'மாலை': 'evening', 'இரவு': 'night',
            'வாரம்': 'week', 'மாதம்': 'month', 'வருடம்': 'year',
            'இங்கே': 'here', 'அங்கே': 'there', 'எங்கே': 'where',
            'வீடு': 'house/home', 'பள்ளி': 'school', 'கடை': 'shop', 'ஊர்': 'town/village',
            
            # Emotions & Mental States (Extended) - Sentiment Words
            'மகிழ்ச்சி': 'happiness/joy', 'சந்தோஷம்': 'joy/happiness', 'மகிழ்வு': 'delight',
            'துக்கம்': 'sorrow/sadness', 'கவலை': 'worry/anxiety', 'பயம்': 'fear',
            'கோபம்': 'anger', 'வருத்தம்': 'regret/sadness', 'ஏமாற்றம்': 'disappointment',
            'அமைதி': 'peace/calm', 'அன்பு': 'love', 'பாசம்': 'affection',
            'வெறுப்பு': 'hatred', 'பொறாமை': 'jealousy', 'நம்பிக்கை': 'hope/trust',
            'ஆர்வம்': 'interest/enthusiasm', 'உற்சாகம்': 'excitement', 'சோர்வு': 'tiredness/fatigue',
            'அலுப்பு': 'boredom/weariness', 'ஆச்சரியம்': 'wonder/surprise', 'மரியாதை': 'respect',
            'தைரியம்': 'courage/bravery', 'வெட்கம்': 'shyness/shame',
            'சிரிப்பு': 'laughter/smile', 'அழுகை': 'crying/tears', 'கண்ணீர்': 'tears',
            'இனிமை': 'sweetness/pleasantness', 'கசப்பு': 'bitterness', 'வலி': 'pain',
            'நோய்': 'disease/sickness', 'ஆரோக்கியம்': 'health', 'நலம்': 'wellness',
            'வெற்றி': 'success/victory', 'தோல்வி': 'failure/defeat', 'வளர்ச்சி': 'growth',
            'இழப்பு': 'loss', 'கஷ்டம்': 'difficulty/hardship', 'சிரமம்': 'difficulty',
            'மகிழ்ந்து': 'happily', 'வருந்தி': 'sadly', 'கோபமாக': 'angrily',
            
            # Mental & Physical Burden
            'பாரம்': 'burden/weight', 'சுமை': 'load/burden', 'பளு': 'weight/burden',
            'மனபாரம்': 'mental burden/stress', 'மனசுமை': 'mental burden',
            'மனபாரங்கள்': 'mental burdens/stresses', 'மனபாரங்களால்': 'due to mental burdens',
            'சுமைகள்': 'burdens/loads', 'பாரங்கள்': 'weights/burdens',
            'மனஅழுத்தம்': 'stress/mental pressure', 'மன இறுக்கம்': 'mental tension',
            
            # Abstract Concepts
            'நீதி': 'justice', 'உண்மை': 'truth', 'பொய்': 'lie/false',
            'அறம்': 'virtue/righteousness', 'தர்மம்': 'righteousness/duty',
            'நன்மை': 'goodness/benefit', 'தீமை': 'evil/harm',
            'கல்வி': 'education/learning', 'அறிவு': 'knowledge/wisdom',
            'புத்தி': 'intelligence/wisdom', 'ஞானம்': 'wisdom/enlightenment',
        }
        
        # Split text into words
        words = text.split()
        word_explanations = []
        
        # Analyze each word
        for word in words:
            # Remove punctuation for matching
            clean_word = word.strip('.,!?;:')
            
            if clean_word in word_meanings:
                word_explanations.append(f"{clean_word} = {word_meanings[clean_word]}")
        
        # Build the meaning output
        meaning_parts = []
        
        # For random text, show clean word-by-word meanings
        # No need for long explanations or sentence structure analysis
        
        if word_explanations:
            # Found words in dictionary - show them
            meaning_parts.append("<strong>சொற்கள் பொருள்:</strong>")
            meaning_parts.append("<br>".join(word_explanations))
        else:
            # No words found in dictionary
            meaning_parts.append("<strong>சொல்:</strong> " + " ".join(text.split()))
            meaning_parts.append("<br><strong>குறிப்பு:</strong> இந்த சொல் தரவுத்தளத்தில் இல்லை")
        
        return "<br>".join(meaning_parts)
    
    def _analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of Tamil text based on keywords.
        
        Args:
            text: Input Tamil text
            
        Returns:
            Dictionary with sentiment analysis
        """
        # Sentiment keywords
        positive_words = {
            'மகிழ்ச்சி', 'சந்தோஷம்', 'மகிழ்வு', 'இன்பம்', 'அன்பு', 'பாசம்', 
            'நம்பிக்கை', 'தைரியம்', 'ஆர்வம்', 'உற்சாகம்', 'அமைதி', 'நன்மை',
            'நல்ல', 'அழகான', 'சிறந்த', 'மரியாதை', 'நன்றி', 'நட்பு',
            'சிரிப்பு', 'மகிழ்', 'சந்தோஷ', 'இனிமை', 'வெற்றி', 'வளர்ச்சி',
            'ஆரோக்கியம்', 'நலம்', 'செல்வம்', 'புகழ்', 'பெருமை', 'ஆனந்தம்',
            'மகிழ்ந்து', 'சந்தோஷமாக', 'நன்றாக', 'அருமை', 'சிறப்பு',
            'அற்புதம்', 'இனிய', 'நல்வாழ்வு', 'சுகம்', 'இன்', 'பயன்',
            'ஊக்கம்', 'ஆதரவு', 'பாராட்டு', 'வாழ்த்து', 'போற்று'
        }
        
        negative_words = {
            'துக்கம்', 'கவலை', 'பயம்', 'கோபம்', 'வருத்தம்', 'ஏமாற்றம்',
            'வெறுப்பு', 'பொறாமை', 'சோர்வு', 'அலுப்பு', 'வெட்கம்', 'துன்பம்',
            'மனபாரம்', 'மனசுமை', 'மனஅழுத்தம்', 'தீமை', 'கெட்ட', 'மோசமாக',
            'வலி', 'நோய்', 'தோல்வி', 'இழப்பு', 'கஷ்டம்', 'சிரமம்',
            'அழுகை', 'கண்ணீர்', 'கசப்பு', 'வேதனை', 'வருந்தி', 'கோபமாக',
            'பாரம்', 'சுமை', 'பளு', 'மன இறுக்கம்', 'அச்சம்', 'பீதி',
            'வெறுப்பு', 'வெறுக்', 'பகை', 'எதிர்', 'கெடு', 'அழி',
            'நஷ்டம்', 'தண்டனை', 'குற்றம்', 'பாவம்', 'தவறு'
        }
        
        neutral_words = {
            'செய்', 'போ', 'வா', 'இரு', 'பார்', 'கேள்', 'சொல்', 'எழுது',
            'படி', 'சாப்பிடு', 'குடி', 'தூங்கு', 'நட', 'ஓடு', 'இன்று',
            'நேற்று', 'நாளை', 'இப்போது', 'பிறகு', 'முன்பு'
        }
        
        # Count sentiment words
        words = text.split()
        positive_count = sum(1 for word in words if any(pos in word for pos in positive_words))
        negative_count = sum(1 for word in words if any(neg in word for neg in negative_words))
        neutral_count = sum(1 for word in words if any(neu in word for neu in neutral_words))
        
        total_sentiment_words = positive_count + negative_count
        
        # Determine sentiment
        if total_sentiment_words == 0:
            sentiment = 'நடுநிலை (Neutral)'
            emoji = '😐'
            score = 0.5
        elif positive_count > negative_count:
            sentiment = 'நேர்மறை (Positive)'
            emoji = '😊'
            score = 0.7 + (positive_count / (total_sentiment_words * 2))
        elif negative_count > positive_count:
            sentiment = 'எதிர்மறை (Negative)'
            emoji = '😞'
            score = 0.3 - (negative_count / (total_sentiment_words * 2))
        else:
            sentiment = 'கலப்பு (Mixed)'
            emoji = '😐'
            score = 0.5
        
        return {
            'label': sentiment,
            'emoji': emoji,
            'score': round(score, 2),
            'positive_words': positive_count,
            'negative_words': negative_count,
            'neutral_words': neutral_count
        }
    
    def _interpret_sentence(self, text: str, word_dict: dict) -> str:
        """Interpret the overall meaning of the sentence"""
        text_lower = text.lower()
        words = text.split()
        
        # Build comprehensive sentence meaning based on words found
        meanings_found = []
        subject = ""
        action = ""
        time = ""
        place = ""
        object_ref = ""
        
        # Extract subject
        if 'நான்' in text:
            subject = "நான் (I)"
        elif 'நீ' in text or 'நீங்கள்' in text:
            subject = "நீ/நீங்கள் (you)"
        elif 'அவன்' in text:
            subject = "அவன் (he)"
        elif 'அவள்' in text:
            subject = "அவள் (she)"
        elif 'அவர்' in text:
            subject = "அவர் (they/he/she)"
        elif 'நாங்கள்' in text:
            subject = "நாங்கள் (we)"
        
        # Extract time reference
        if 'இன்று' in text:
            time = "இன்று (today)"
        elif 'நேற்று' in text:
            time = "நேற்று (yesterday)"
        elif 'நாளை' in text:
            time = "நாளை (tomorrow)"
        elif 'காலை' in text:
            time = "காலையில் (in the morning)"
        elif 'மாலை' in text:
            time = "மாலையில் (in the evening)"
        elif 'இரவு' in text:
            time = "இரவில் (at night)"
        
        # Extract action
        if 'சாப்பிட்டேன்' in text or 'சாப்பிட்டான்' in text or 'சாப்பிட்டாள்' in text or 'சாப்பிட்டார்' in text:
            action = "சாப்பிட்டது (ate)"
            object_ref = "உணவு (food)"
        elif 'சாப்பிடுவேன்' in text or 'சாப்பிடுவான்' in text:
            action = "சாப்பிடுவது (will eat)"
            object_ref = "உணவு (food)"
        elif 'சாப்பிடுகிறேன்' in text or 'சாப்பிடுகிறான்' in text:
            action = "சாப்பிடுகிறது (is eating)"
            object_ref = "உணவு (food)"
        elif 'சென்றேன்' in text or 'சென்றான்' in text or 'சென்றாள்' in text:
            action = "சென்றது (went)"
        elif 'செல்கிறேன்' in text or 'செல்கிறான்' in text:
            action = "செல்கிறது (is going)"
        elif 'செல்வேன்' in text or 'செல்வான்' in text:
            action = "செல்வது (will go)"
        elif 'வந்தேன்' in text or 'வந்தான்' in text or 'வந்தாள்' in text:
            action = "வந்தது (came)"
        elif 'வருகிறேன்' in text or 'வருகிறான்' in text:
            action = "வருகிறது (is coming)"
        elif 'வருவேன்' in text or 'வருவான்' in text:
            action = "வருவது (will come)"
        elif 'படித்தேன்' in text or 'படித்தான்' in text:
            action = "படித்தது (read/studied)"
        elif 'படிக்கிறேன்' in text or 'படிக்கிறான்' in text:
            action = "படிக்கிறது (is reading/studying)"
        elif 'படிப்பேன்' in text or 'படிப்பான்' in text:
            action = "படிப்பது (will read/study)"
        elif 'பார்த்தேன்' in text or 'பார்த்தான்' in text:
            action = "பார்த்தது (saw/watched)"
        elif 'பார்க்கிறேன்' in text or 'பார்க்கிறான்' in text:
            action = "பார்க்கிறது (is watching)"
        elif 'எழுதினேன்' in text or 'எழுதினான்' in text:
            action = "எழுதியது (wrote)"
        elif 'விளையாடினேன்' in text or 'விளையாடினான்' in text:
            action = "விளையாடியது (played)"
        
        # Extract place
        if 'பள்ளி' in text:
            place = "பள்ளியில் (at school)"
        elif 'கல்லூரி' in text:
            place = "கல்லூரியில் (at college)"
        elif 'அலுவலகம்' in text:
            place = "அலுவலகத்தில் (at office)"
        elif 'வீடு' in text:
            place = "வீட்டில் (at home)"
        
        # Build comprehensive meaning
        meaning_parts = []
        
        if subject:
            meaning_parts.append(f"**யார்:** {subject}")
        if action:
            meaning_parts.append(f"**என்ன செய்தது:** {action}")
        if object_ref:
            meaning_parts.append(f"**எதை:** {object_ref}")
        if time:
            meaning_parts.append(f"**எப்போது:** {time}")
        if place:
            meaning_parts.append(f"**எங்கே:** {place}")
        
        # Create full sentence interpretation
        sentence_interpretation = []
        
        if subject and action:
            # Build natural sentence
            if 'சாப்பிட்ட' in text:
                tamil_meaning = f"{subject.split('(')[0].strip()} {object_ref.split('(')[0].strip() if object_ref else ''} {action.split('(')[0].strip()}"
                english_meaning = f"{subject.split('(')[1].strip(')')} {action.split('(')[1].strip(')')} {object_ref.split('(')[1].strip(')') if object_ref else ''}"
                
                if time:
                    tamil_meaning += f" {time.split('(')[0].strip()}"
                    english_meaning += f" {time.split('(')[1].strip(')')}"
                
                sentence_interpretation.append(f"<strong>வாக்கிய பொருள்:</strong>")
                sentence_interpretation.append(f"தமிழ்: {tamil_meaning}")
                sentence_interpretation.append(f"English: {english_meaning}")
            elif 'சென்ற' in text or 'செல்' in text:
                if place:
                    sentence_interpretation.append(f"<strong>வாக்கிய பொருள்:</strong>")
                    sentence_interpretation.append(f"{subject.split('(')[0].strip()} {place.split('(')[0].strip()} {action.split('(')[0].strip()}")
                    sentence_interpretation.append(f"({subject.split('(')[1].strip(')')} {action.split('(')[1].strip(')')} {place.split('(')[1].strip(')')})")
            elif 'படித்த' in text or 'படிக்' in text:
                sentence_interpretation.append(f"<strong>வாக்கிய பொருள்:</strong>")
                sentence_interpretation.append(f"{subject.split('(')[0].strip()} {action.split('(')[0].strip()}")
                sentence_interpretation.append(f"({subject.split('(')[1].strip(')')} {action.split('(')[1].strip(')')})")
        
        if meaning_parts:
            result = "<br>".join(meaning_parts)
            if sentence_interpretation:
                result += "<br><br>" + "<br>".join(sentence_interpretation)
            return result
        
        # Fallback - provide general translation attempt
        # For single words, show simple translation
        if len(words) == 1:
            word = words[0]
            clean_word = word.strip('.,!?;:')
            
            # Check if word exists in dictionary
            if clean_word in word_dict:
                return f"""<strong>சொல்:</strong> {clean_word}
<br><strong>பொருள்:</strong> {word_dict[clean_word]}"""
            else:
                # Try to provide some meaning even if not in dictionary
                return f"""<strong>சொல்:</strong> {clean_word}
<br><strong>குறிப்பு:</strong> இந்த சொல்லின் பொருள் தரவுத்தளத்தில் இல்லை"""
        
        # For multiple words, build word-by-word meaning
        word_translations = []
        for word in words:
            clean_word = word.strip('.,!?;:')
            if clean_word in word_dict:
                word_translations.append(f"{clean_word} ({word_dict[clean_word]})")
            else:
                word_translations.append(clean_word)
        
        translation_text = " ".join(word_translations) if word_translations else text
        
        return f"""<strong>வாக்கியம்:</strong> {text}
<br><strong>மொழிபெயர்ப்பு:</strong> {translation_text}"""
    
    def _analyze_themes(self, text: str) -> str:
        """Analyze actual themes/topics in the text"""
        # Topic-based analysis
        if 'சாப்பாடு' in text or 'சாப்பிட' in text:
            return "உணவு (Food)"
        
        if 'பள்ளி' in text or 'படி' in text or 'கல்வி' in text:
            return "கல்வி (Education)"
        
        if 'அலுவலகம்' in text or 'வேலை' in text:
            return "வேலை (Work)"
        
        if 'காலை' in text or 'மாலை' in text or 'இரவு' in text:
            return "நேரம் (Time)"
        
        if 'காதல்' in text or 'அன்பு' in text:
            return "காதல் (Love)"
        
        if 'நட்பு' in text or 'நண்பன்' in text:
            return "நட்பு (Friendship)"
        
        if 'அறம்' in text or 'நீதி' in text:
            return "அறநெறி (Virtue)"
        
        if 'செல்வம்' in text or 'பணம்' in text:
            return "செல்வம் (Wealth)"
        
        if 'இன்பம்' in text or 'மகிழ்ச்சி' in text:
            return "இன்பம் (Joy)"
        
        if 'துன்பம்' in text or 'வருத்தம்' in text:
            return "துன்பம் (Sorrow)"
        
        # Daily activities
        if any(word in text for word in ['செல்', 'வர', 'போ']):
            return "அன்றாட செயல்கள் (Daily activities)"
        
        return "பொதுவான தமிழ் உரை (General Tamil text)"
    
    def _simple_translate(self, text: str) -> str:
        """Simple keyword-based translation hints"""
        translations = {
            'அறம்': 'virtue/righteousness',
            'கல்': 'learning/education',
            'காதல்': 'love',
            'இன்பம்': 'joy/pleasure',
            'துன்பம்': 'sorrow/pain',
            'செல்வம்': 'wealth',
            'நன்றி': 'gratitude',
            'வேந்தன்': 'king',
            'மக்கள்': 'people',
        }
        
        found = []
        for tamil, english in translations.items():
            if tamil in text:
                found.append(f"{tamil}={english}")
        
        if found:
            return f"Keywords: {', '.join(found[:3])}"
        
        return "Tamil literary verse (database match not found - add this verse for accurate translation)"
    
    def _identify_theme(self, text: str) -> str:
        """Identify theme from keywords"""
        if any(w in text for w in ['அறம்', 'நீதி', 'தர்மம்']):
            return "Ethics & Morality"
        if any(w in text for w in ['கல்', 'கற்']):
            return "Education & Knowledge"
        if any(w in text for w in ['காதல்', 'அன்பு']):
            return "Love & Affection"
        if any(w in text for w in ['போர்', 'வெற்றி']):
            return "War & Victory"
        if any(w in text for w in ['கடவுள்', 'இறை']):
            return "Devotion & Spirituality"
        
        return "General Tamil Literature"
    
    def search_by_book_and_number(self, book_key: str, verse_number: int) -> Optional[Dict]:
        """
        Get verse by book name and verse number.
        
        Args:
            book_key: Book identifier (e.g., 'thirukkural', 'kamba_ramayanam')
            verse_number: Verse number
            
        Returns:
            Verse data or None
        """
        # Select appropriate database
        book_db = self.thirukkural_db if book_key == 'thirukkural' else self.kamba_db
        
        verses = book_db.get('verses', [])
        for verse_data in verses:
            if verse_data.get('verse_number') == verse_number:
                result = verse_data.copy()
                result['verse_number'] = str(verse_number)
                result['book_key'] = book_key
                return result
        return None
    
    def get_all_books(self) -> List[Dict]:
        """
        Get list of all available Tamil literature books.
        
        Returns:
            List of book metadata
        """
        books = []
        
        # Add Thirukkural
        tk_metadata = self.thirukkural_db.get('metadata', {})
        tk_verse_count = len(self.thirukkural_db.get('verses', []))
        books.append({
            'key': 'thirukkural',
            'title': tk_metadata.get('title', 'திருக்குறள்'),
            'author': tk_metadata.get('author', 'திருவள்ளுவர்'),
            'verse_count': tk_verse_count,
            'description': tk_metadata.get('description', '')
        })
        
        # Add Kamba Ramayanam
        kr_metadata = self.kamba_db.get('metadata', {})
        kr_verse_count = len(self.kamba_db.get('verses', []))
        books.append({
            'key': 'kamba_ramayanam',
            'title': kr_metadata.get('title', 'கம்ப ராமாயணம்'),
            'author': kr_metadata.get('author', 'கம்பர்'),
            'verse_count': kr_verse_count,
            'description': kr_metadata.get('description', '')
        })
        
        return books
    
    def get_book_metadata(self, book_key: str) -> Optional[Dict]:
        """
        Get metadata for a specific book.
        
        Args:
            book_key: Book identifier
            
        Returns:
            Book metadata or None
        """
        if book_key == 'thirukkural':
            return self.thirukkural_db.get('metadata')
        elif book_key == 'kamba_ramayanam':
            return self.kamba_db.get('metadata')
        return None
    
    def search_by_author(self, author: str) -> List[str]:
        """
        Find books by author name.
        
        Args:
            author: Author name in Tamil
            
        Returns:
            List of book keys by this author
        """
        books = []
        
        # Check Thirukkural
        tk_metadata = self.thirukkural_db.get('metadata', {})
        if author in tk_metadata.get('author', ''):
            books.append('thirukkural')
        
        # Check Kamba Ramayanam
        kr_metadata = self.kamba_db.get('metadata', {})
        if author in kr_metadata.get('author', ''):
            books.append('kamba_ramayanam')
        
        return books
    
    def get_statistics(self) -> Dict:
        """
        Get database statistics.
        
        Returns:
            Statistics dictionary
        """
        # Count verses from both databases
        tk_verses = len(self.thirukkural_db.get('verses', []))
        kr_verses = len(self.kamba_db.get('verses', []))
        total_loaded_verses = tk_verses + kr_verses
        
        # Get expected totals
        tk_metadata = self.thirukkural_db.get('metadata', {})
        kr_metadata = self.kamba_db.get('metadata', {})
        tk_expected = tk_metadata.get('total_verses', tk_verses)
        kr_expected = kr_metadata.get('total_verses', kr_verses)
        total_expected_verses = tk_expected + kr_expected
        
        coverage_percent = round(total_loaded_verses / total_expected_verses * 100, 2) if total_expected_verses > 0 else 0
        
        return {
            'total_books': 2,
            'total_loaded_verses': total_loaded_verses,
            'total_expected_verses': total_expected_verses,
            'coverage_percent': coverage_percent,
            'books': self.get_all_books()
        }