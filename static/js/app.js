// Tamil Semantic & Sentiment Analyzer - Frontend Logic

// DOM Elements
const tamilInput = document.getElementById('tamilInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const clearBtn = document.getElementById('clearBtn');
const charCount = document.getElementById('charCount');
const resultsSection = document.getElementById('resultsSection');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsContent = document.getElementById('resultsContent');
const errorMessage = document.getElementById('errorMessage');

// Result Elements
const resultHeader = document.getElementById('resultHeader');
const resultVerse = document.getElementById('resultVerse');
const verseText = document.getElementById('verseText');
const resultMeaning = document.getElementById('resultMeaning');
const meaningText = document.getElementById('meaningText');
const summaryText = document.getElementById('summaryText');
const sentimentBadge = document.getElementById('sentimentBadge');
const confidenceFill = document.getElementById('confidenceFill');
const confidenceValue = document.getElementById('confidenceValue');
const sourceBadge = document.getElementById('sourceBadge');

// Event Listeners
tamilInput.addEventListener('input', updateCharCount);
analyzeBtn.addEventListener('click', analyzeText);
clearBtn.addEventListener('click', clearAll);

// Enable Enter key to analyze (Ctrl+Enter)
tamilInput.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
        analyzeText();
    }
});

// Update character count
function updateCharCount() {
    const count = tamilInput.value.length;
    charCount.textContent = count;
}

// Clear all inputs and results
function clearAll() {
    tamilInput.value = '';
    updateCharCount();
    hideResults();
}

// Hide results section
function hideResults() {
    resultsSection.style.display = 'none';
    resultsContent.style.display = 'none';
    errorMessage.style.display = 'none';
}

// Show loading spinner
function showLoading() {
    resultsSection.style.display = 'block';
    loadingSpinner.style.display = 'block';
    resultsContent.style.display = 'none';
    errorMessage.style.display = 'none';
}

// Hide loading spinner
function hideLoading() {
    loadingSpinner.style.display = 'none';
}

// Show error message
function showError(message) {
    hideLoading();
    resultsContent.style.display = 'none';
    errorMessage.style.display = 'block';
    errorMessage.textContent = '❌ ' + message;
}

// Display results
function displayResults(data) {
    hideLoading();
    resultsContent.style.display = 'block';
    errorMessage.style.display = 'none';

    // Header
    resultHeader.textContent = data.header;

    // Verse (show ONLY for authentic Thirukkural verses)
    if (data.verse && data.source === 'thirukkural') {
        resultVerse.style.display = 'block';
        verseText.textContent = data.verse;
    } else {
        resultVerse.style.display = 'none';
    }

    // Meaning (show ONLY for authentic Thirukkural verses)
    if (data.source === 'thirukkural') {
        resultMeaning.style.display = 'block';
        meaningText.innerHTML = data.meaning;
    } else {
        // For random text, show meaning in the meaning section
        resultMeaning.style.display = 'block';
        meaningText.innerHTML = data.meaning || '';
    }

    // Summary (show analysis)
    if (data.summary) {
        summaryText.innerHTML = data.summary;
    } else {
        summaryText.innerHTML = '';
    }
    
    // Add English meaning if available (only for Thirukkural)
    if (data.english_meaning && data.source === 'thirukkural') {
        summaryText.innerHTML += '<br><br><strong>English Meaning:</strong><br>' + data.english_meaning;
    }
    
    // Add Theme if available (only for Thirukkural)
    if (data.theme && data.source === 'thirukkural') {
        summaryText.innerHTML += '<br><br><strong>📌 Theme:</strong> ' + data.theme;
    }
    
    // Add Moral if available (only for Thirukkural)
    if (data.moral && data.source === 'thirukkural') {
        summaryText.innerHTML += '<br><br><strong>💡 Moral:</strong> ' + data.moral;
    }
    
    // Add Author if available (only for Thirukkural)
    if (data.author && data.source === 'thirukkural') {
        summaryText.innerHTML += '<br><br><strong>✍️ Author:</strong> ' + data.author;
    }
    
    // Add Characters if available
    if (data.characters && Array.isArray(data.characters) && data.characters.length > 0) {
        summaryText.innerHTML += '<br><br><strong>👥 Characters:</strong> ' + data.characters.join(', ');
    }
    
    // Add Book Metadata if available
    if (data.book_metadata) {
        const meta = data.book_metadata;
        let metaHtml = '<br><br><div style="border-top: 2px solid #ff6b35; padding-top: 10px; margin-top: 10px;">';
        metaHtml += '<strong>📚 Book Information:</strong><br>';
        if (meta.tamil_title) metaHtml += '• Title: ' + meta.tamil_title;
        if (meta.english_title) metaHtml += ' (' + meta.english_title + ')';
        metaHtml += '<br>';
        if (meta.author) metaHtml += '• Author: ' + meta.author + '<br>';
        if (meta.period) metaHtml += '• Period: ' + meta.period + '<br>';
        if (meta.category) metaHtml += '• Category: ' + meta.category;
        metaHtml += '</div>';
        summaryText.innerHTML += metaHtml;
    }
    
    // Sentiment Analysis (for random text)
    if (data.sentiment && data.source === 'random_text') {
        const sent = data.sentiment;
        let sentimentHtml = '<br><br><div style="border-top: 2px solid #4CAF50; padding-top: 10px; margin-top: 10px;">';
        sentimentHtml += '<strong>💭 உணர்வு பகுப்பாய்வு (Sentiment Analysis):</strong><br>';
        sentimentHtml += '• உணர்வு: ' + sent.emoji + ' ' + sent.label + '<br>';
        if (sent.positive_words > 0) {
            sentimentHtml += '• நேர்மறை சொற்கள்: ' + sent.positive_words + '<br>';
        }
        if (sent.negative_words > 0) {
            sentimentHtml += '• எதிர்மறை சொற்கள்: ' + sent.negative_words + '<br>';
        }
        sentimentHtml += '</div>';
        summaryText.innerHTML += sentimentHtml;
    }

    // Old sentiment badge (keep for Thirukkural compatibility)
    const sentiment = data.sentiment && data.sentiment.label ? data.sentiment.label : 'NEUTRAL';
    sentimentBadge.textContent = (data.sentiment && data.sentiment.emoji ? data.sentiment.emoji : '😐') + ' ' + sentiment;
    sentimentBadge.className = 'sentiment-badge sentiment-neutral';

    // Confidence
    const confidence = Math.round(data.sentiment_confidence * 100);
    confidenceFill.style.width = confidence + '%';
    confidenceValue.textContent = confidence + '%';

    // Source badge - Enhanced for all Tamil literature
    if (data.source && data.source !== 'generic' && data.source !== 'unknown') {
        const bookTitles = {
            'thirukkural': 'திருக்குறள்',
            'kambaramayanam': 'கம்பராமாயணம்',
            'silapathikaram': 'சிலப்பதிகாரம்',
            'thevaaram': 'தேவாரம்',
            'thiruvachakam': 'திருவாசகம்',
            'purananuru': 'புறநானூறு',
            'naladiyar': 'நாலடியார்',
            'aathichudi': 'ஆத்திசூடி',
            'konrai_venthan': 'கொன்றை வேந்தன்',
            'thiruvilayadal_puranam': 'திருவிளையாடல் புராணம்'
        };
        
        const bookTitle = bookTitles[data.source] || data.source;
        sourceBadge.textContent = '📚 ' + bookTitle + ' Database';
        sourceBadge.style.background = '#ff6b35';
    } else {
        sourceBadge.textContent = '🤖 AI Analysis';
        sourceBadge.style.background = '#2196f3';
    }

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Get sentiment emoji
function getSentimentEmoji(sentiment) {
    switch (sentiment) {
        case 'POSITIVE':
            return '😊';
        case 'NEGATIVE':
            return '😞';
        case 'NEUTRAL':
            return '😐';
        default:
            return '🤔';
    }
}

// Analyze text
async function analyzeText() {
    const text = tamilInput.value.trim();

    // Validate input
    if (!text) {
        showError('உரையை உள்ளிடவும் (Please enter text)');
        return;
    }

    // Check for Tamil characters
    const tamilRegex = /[\u0B80-\u0BFF]/;
    if (!tamilRegex.test(text)) {
        showError('தமிழ் எழுத்துக்கள் இல்லை (No Tamil characters found)');
        return;
    }

    // Show loading
    showLoading();

    try {
        // Call API
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });

        const result = await response.json();

        if (result.error) {
            showError(result.message);
        } else {
            displayResults(result.data);
        }
    } catch (error) {
        console.error('Error:', error);
        showError('பிழை ஏற்பட்டது (An error occurred): ' + error.message);
    }
}

// Load example text
function loadExample(element) {
    const exampleText = element.querySelector('.example-text').textContent;
    tamilInput.value = exampleText;
    updateCharCount();
    
    // Scroll to input
    tamilInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Optional: Auto-analyze after loading example
    setTimeout(() => {
        analyzeText();
    }, 500);
}

// Check system health on page load
async function checkHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        
        console.log('System Health:', data);
        
        if (!data.models_loaded) {
            console.warn('⚠️ Models not loaded. Please run setup_models.py');
        }
        
        if (!data.database_loaded) {
            console.warn('⚠️ Database not loaded');
        }
        
        console.log(`📚 Loaded ${data.verse_count} thirukkural verses`);
    } catch (error) {
        console.error('Health check failed:', error);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Tamil Semantic & Sentiment Analyzer initialized');
    console.log('💡 100% Offline Mode - No Internet Required!');
    
    updateCharCount();
    checkHealth();
    
    // Focus on input
    tamilInput.focus();
});

// Keyboard shortcuts info
console.log('⌨️ Keyboard Shortcuts:');
console.log('  Ctrl+Enter: Analyze text');
console.log('  Escape: Clear all');

// ESC key to clear
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        clearAll();
    }
});
