#!/usr/bin/env python3
"""Check available Gemini models."""
import sys
sys.path.insert(0, '/home/wrath/Friday AI assist')

from config import GOOGLE_API_KEY
from google import genai

client = genai.Client(api_key=GOOGLE_API_KEY)

print("=== Available Gemini Models ===\n")
try:
    for model in client.models.list():
        print(f"Model Name: {model.name}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"  Supported methods: {model.supported_generation_methods}")
        print()
except Exception as e:
    print(f"Error listing models: {e}")
    print("\nTrying alternative method...")
    
    # Try common model names
    test_models = [
        "gemini-pro",
        "gemini-1.5-pro-latest",
        "gemini-1.5-flash-latest",
        "gemini-1.0-pro",
        "models/gemini-pro",
        "models/gemini-1.5-pro-latest",
        "models/gemini-1.5-flash-latest"
    ]
    
    print("\nTesting common model names:")
    for model_name in test_models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents="Say 'OK'"
            )
            print(f"✓ {model_name} - WORKS!")
        except Exception as e:
            print(f"✗ {model_name} - {str(e)[:80]}")
