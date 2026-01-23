from services.gemini import GeminiService
import os

print(f"DEBUG: GEMINI_API_KEY set: {bool(os.getenv('GEMINI_API_KEY'))}")
try:
    g = GeminiService()
    print(f"DEBUG: Type of g: {type(g)}")
    print(f"DEBUG: Is available: {g.is_available}")
    if hasattr(g, 'model'):
        print(f"DEBUG: Model type: {type(g.model)}")
    else:
        print("DEBUG: Attribute 'model' not found in GeminiService instance")
except Exception as e:
    print(f"DEBUG: Exception during initialization: {e}")
