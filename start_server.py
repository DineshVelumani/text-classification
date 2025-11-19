"""
Start the Tamil Semantic Analyzer Server
"""
import subprocess
import sys

print("🚀 Starting Tamil Semantic Analyzer Server...")
print("=" * 70)

try:
    # Start the server
    subprocess.run([sys.executable, "app.py"], check=True)
except KeyboardInterrupt:
    print("\n\n⏹️  Server stopped by user")
except Exception as e:
    print(f"\n❌ Server error: {e}")
    sys.exit(1)
