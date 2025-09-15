import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def test_gemini():
    try:
        # List available models first (optional)
        print("Available models:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")
        
        # Use the new model name
        model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
        
        # Test prompt
        response = model.generate_content(
            "What is VLOOKUP in Excel? Give a brief answer."
        )
        
        print("\n✅ Gemini API is working!")
        print(f"Response: {response.text[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Make sure you have:")
        print("1. Created .env file in backend folder")
        print("2. Added your GEMINI_API_KEY to .env (no spaces)")
        print("3. Installed required packages")
        return False

if __name__ == "__main__":
    print("Testing Gemini API connection...")
    test_gemini()