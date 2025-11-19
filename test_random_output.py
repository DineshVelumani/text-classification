"""Test random text output"""
import requests

print("Testing Random Text Output")
print("=" * 80)

test_cases = [
    {
        "name": "Random modern sentence",
        "text": "இன்று காலையில் நான் பள்ளிக்கு சென்றேன்",
        "expected": "Should be rejected as random text"
    },
    {
        "name": "Random words",
        "text": "மரம் வீடு கார் பள்ளி",
        "expected": "Should be rejected as random text"
    },
    {
        "name": "Gibberish",
        "text": "அபச தெகு மயி லொறு",
        "expected": "Should be rejected as random text"
    },
    {
        "name": "Single word",
        "text": "அன்பு",
        "expected": "Should be rejected or find very low match"
    }
]

print("\n🧪 Testing what 'பொருள்' (meaning) is returned for random text:\n")

for i, test in enumerate(test_cases, 1):
    print(f"{'='*80}")
    print(f"Test {i}: {test['name']}")
    print(f"Input: {test['text']}")
    print(f"Expected: {test['expected']}")
    print()
    
    try:
        r = requests.post('http://localhost:5000/analyze', 
                         json={'text': test['text']}, 
                         timeout=10)
        
        if r.status_code == 200:
            data = r.json()['data']
            
            print(f"✅ Response:")
            print(f"  Source: {data['source']}")
            print(f"  Confidence: {data['confidence']*100:.1f}%")
            
            if data['source'] == 'random_text':
                print(f"\n  ✅ Correctly detected as random text")
                print(f"\n  📝 Meaning (பொருள்) shown to user:")
                meaning = data.get('meaning', '')
                # Clean HTML tags
                clean_meaning = meaning.replace('<strong>', '').replace('</strong>', '').replace('<br>', '\n')
                print(f"  {clean_meaning}")
            else:
                print(f"\n  ⚠️  Detected as: {data['source']}")
                print(f"  Book: {data.get('header', 'N/A')}")
                print(f"  Verse: {data.get('verse', 'N/A')[:60]}...")
                
        else:
            print(f"❌ HTTP Error: {r.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()

print("=" * 80)
print("\n💡 Summary:")
print("Random text should be detected with source='random_text' and confidence=0%")
print("The 'meaning' field should indicate that the text is not in the database.")
