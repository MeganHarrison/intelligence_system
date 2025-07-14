#!/usr/bin/env python3
"""
Development startup script for Strategic Intelligence Dashboard API
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI dependencies available")
        return True
    except ImportError:
        print("❌ FastAPI dependencies not found")
        print("Please install: pip install fastapi uvicorn[standard] websockets pydantic")
        return False

def main():
    """Start the API server"""
    print("🚀 Strategic Intelligence Dashboard API Server")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 Install missing dependencies with:")
        print("pip install -r ../requirements.txt")
        return 1
    
    # Set environment variables for development
    os.environ.setdefault('CONFIG_PROFILE', 'development')
    
    # Start the server
    server_file = Path(__file__).parent / "api_server.py"
    
    print("Starting server...")
    print("📡 API Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/api/docs")
    print("🔌 WebSocket: ws://localhost:8000/ws/{client_id}")
    print("🎯 Frontend: http://localhost:8051")
    print("\nPress Ctrl+C to stop the server")
    print("💡 Note: Some warnings about intelligence components are normal")
    print("   Core API functionality will work, advanced features initialize async")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, str(server_file)
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        return 0
    except Exception as e:
        print(f"❌ Server error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())