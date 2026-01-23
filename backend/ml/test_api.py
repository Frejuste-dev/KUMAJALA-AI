import requests
import json

def test_translation(text, target_language):
    url = "http://localhost:5000/kumajala-api/v1/translate"
    payload = {
        "text": text,
        "targetLanguage": target_language
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"\n🔍 Testing: '{text}' -> {target_language}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Translation: {data.get('translation')}")
            print(f"Source: {data.get('source')}")
            if 'confidence' in data:
                print(f"Confidence: {data.get('confidence')}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    # Test dictionary fallback
    test_translation("bonjour", "bété")
    test_translation("merci", "baoulé")
    
    # Test Gemini fallback (not in dictionary)
    test_translation("Comment se passe ta journée ?", "bété")
    test_translation("Je suis très content de te voir.", "baoulé")
    test_translation("Où est le marché le plus proche ?", "mooré")
    test_translation("J'aime beaucoup cette musique.", "agni")
