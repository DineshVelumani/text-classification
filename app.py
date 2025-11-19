"""
Flask Web Application for Tamil Semantic & Sentiment Analyzer
100% Offline - No API Required
"""

import sys
import io

# Set UTF-8 encoding for stdout to handle Tamil and emoji characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from flask import Flask, render_template, request, jsonify
from models.text_processor import TamilTextProcessor
from models.sentiment_analyzer_lite import SentimentAnalyzer  # Using lightweight version
from models.semantic_analyzer_multi import MultiLiteratureSemanticAnalyzer  # ALL Tamil literature
import traceback

app = Flask(__name__)

# Initialize analyzers (loaded once at startup)
print("🚀 Initializing Tamil Semantic & Sentiment Analyzer...")
print("=" * 60)

try:
    # Initialize components
    text_processor = TamilTextProcessor()
    print("✅ Text processor ready")
    
    # Initialize semantic analyzer with both databases
    semantic_analyzer = MultiLiteratureSemanticAnalyzer(
        thirukkural_db='database/tamil_literature_db.json',
        kamba_db='database/kamba_ramayanam_db.json'
    )
    print("✅ Multi-literature semantic analyzer ready (Thirukkural + Kamba Ramayanam)")
    
    # DEBUG: Check database
    db_stats = semantic_analyzer.get_statistics()
    print(f"   📊 Database check: {db_stats['total_loaded_verses']} verses from {db_stats['total_books']} books")
    
    sentiment_analyzer = SentimentAnalyzer()
    print("✅ Sentiment analyzer ready")
    
    print("=" * 60)
    print("✅ All systems ready! Application is 100% offline-capable.")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error initializing analyzers: {e}")
    print("\n⚠️  Please run 'python setup_models.py' first to download models.")
    traceback.print_exc()
    exit(1)

@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze Tamil text for semantic meaning and sentiment.
    
    Returns:
        JSON with analysis results
    """
    try:
        # Get input text
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({
                'error': True,
                'message': 'உரையை உள்ளிடவும் (Please enter text)'
            }), 400
        
        # Validate Tamil text
        if not text_processor.is_valid_tamil(text):
            return jsonify({
                'error': True,
                'message': 'தமிழ் எழுத்துக்கள் இல்லை (No Tamil characters found)'
            }), 400
        
        # Perform semantic analysis
        semantic_result = semantic_analyzer.analyze(text)
        
        # Perform sentiment analysis
        sentiment_result = sentiment_analyzer.analyze(text)
        
        # Format response in திருக்குறள் style
        response = format_response(semantic_result, sentiment_result)
        
        return jsonify({
            'error': False,
            'data': response,
            'raw': {
                'semantic': semantic_result,
                'sentiment': sentiment_result
            }
        })
        
    except Exception as e:
        print(f"Error in analysis: {e}")
        traceback.print_exc()
        return jsonify({
            'error': True,
            'message': f'பிழை ஏற்பட்டது: {str(e)}'
        }), 500

def format_response(semantic: dict, sentiment: dict) -> dict:
    """
    Format analysis results in standard output format for ALL Tamil literature.
    
    Args:
        semantic: Semantic analysis results
        sentiment: Sentiment analysis results
        
    Returns:
        Formatted response dictionary with all available fields
    """
    if semantic.get('found', False):
        # Found in Tamil literature database
        header = f"நூல்: {semantic['book']}"
        
        if semantic.get('section'):
            header += f" | பகுதி: {semantic['section']}"
        
        if semantic.get('number'):
            header += f" | பாடல்: {semantic['number']}"
        
        formatted = {
            'header': header,
            'verse': semantic.get('verse', ''),
            'meaning': semantic.get('meaning', ''),
            'summary': semantic.get('summary', ''),
            'sentiment': sentiment.get('sentiment', 'NEUTRAL'),
            'sentiment_confidence': sentiment.get('confidence', 0.0),
            'source': semantic.get('source', 'unknown'),
            'confidence': semantic.get('confidence', 0.0)
        }
        
        # Add all optional rich fields
        if 'english_meaning' in semantic:
            formatted['english_meaning'] = semantic['english_meaning']
        
        if 'theme' in semantic:
            formatted['theme'] = semantic['theme']
        
        if 'moral' in semantic:
            formatted['moral'] = semantic['moral']
        
        if 'author' in semantic:
            formatted['author'] = semantic['author']
        
        if 'characters' in semantic:
            formatted['characters'] = semantic['characters']
        
        if 'book_metadata' in semantic:
            formatted['book_metadata'] = semantic['book_metadata']
        
    else:
        # Not found in database - random text analysis
        formatted = {
            'header': f"நூல்: {semantic.get('book', 'பொது தமிழ் உரை')}",
            'verse': '',  # No verse for random text
            'meaning': semantic.get('meaning', ''),
            'summary': semantic.get('summary', ''),
            'sentiment': semantic.get('sentiment', {}),  # Include full sentiment object
            'source': semantic.get('source', 'random_text'),  # Use actual source
            'confidence': 0.0
        }
        
        # Add optional analysis fields if available
        if 'english_meaning' in semantic:
            formatted['english_meaning'] = semantic['english_meaning']
        
        if 'theme' in semantic:
            formatted['theme'] = semantic['theme']
        
        if 'moral' in semantic:
            formatted['moral'] = semantic['moral']
    
    return formatted

@app.route('/search/<string:book_key>/<int:verse_number>', methods=['GET'])
def search_verse(book_key, verse_number):
    """
    Search for verse by book name and verse number.
    
    Args:
        book_key: Book identifier (e.g., 'thirukkural', 'kambaramayanam')
        verse_number: Verse number
        
    Returns:
        JSON with verse data
    """
    try:
        verse_data = semantic_analyzer.search_by_book_and_number(book_key, verse_number)
        
        if verse_data:
            return jsonify({
                'error': False,
                'data': verse_data
            })
        else:
            return jsonify({
                'error': True,
                'message': f'{book_key} - குறள்/பாட்டு எண் {verse_number} கிடைக்கவில்லை'
            }), 404
            
    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e)
        }), 500

@app.route('/books', methods=['GET'])
def get_books():
    """
    Get list of all available Tamil literature books.
    
    Returns:
        JSON with books list and metadata
    """
    try:
        books = semantic_analyzer.get_all_books()
        return jsonify({
            'error': False,
            'data': books,
            'total_books': len(books)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e)
        }), 500

@app.route('/book/<string:book_key>', methods=['GET'])
def get_book_info(book_key):
    """
    Get metadata for a specific book.
    
    Args:
        book_key: Book identifier
        
    Returns:
        JSON with book metadata
    """
    try:
        metadata = semantic_analyzer.get_book_metadata(book_key)
        if metadata:
            return jsonify({
                'error': False,
                'data': metadata
            })
        else:
            return jsonify({
                'error': True,
                'message': f'நூல் {book_key} கிடைக்கவில்லை'
            }), 404
    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e)
        }), 500

@app.route('/statistics', methods=['GET'])
def get_statistics():
    """
    Get database statistics.
    
    Returns:
        JSON with comprehensive statistics
    """
    try:
        stats = semantic_analyzer.get_statistics()
        return jsonify({
            'error': False,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        JSON with system status
    """
    stats = semantic_analyzer.get_statistics()
    return jsonify({
        'status': 'healthy',
        'offline_mode': True,
        'models_loaded': True,
        'database_loaded': stats['total_books'] > 0,
        'total_books': stats['total_books'],
        'total_verses': stats['total_loaded_verses'],
        'coverage_percent': stats['coverage_percent']
    })

if __name__ == '__main__':
    print("\n🌐 Starting Flask server...")
    print("📱 Open browser: http://localhost:5000")
    print("💡 System is 100% offline - no internet required!")
    print("\nPress Ctrl+C to stop the server.\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
