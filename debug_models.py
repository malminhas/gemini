import os
import google.generativeai as genai

API_KEY = os.environ.get("GOOGLE_API_KEY")

if not API_KEY:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    exit(1)

genai.configure(api_key=API_KEY)

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
