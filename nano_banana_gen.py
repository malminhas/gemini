import os
import requests
from bs4 import BeautifulSoup
import dspy
from google import genai
from google.genai import types

# --- Configuration ---
# You can set these as environment variables or replace them directly here.
API_KEY = os.environ.get("GOOGLE_API_KEY")
PRO_MODEL_ID = "gemini-3-pro-image-preview"

# --- 1. Web Scraping ---
def scrape_webpage(url):
    """Scrapes the main text content from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Simple extraction: get all paragraph text
        # In a real app, you might want more sophisticated extraction
        paragraphs = soup.find_all('p')
        text_content = " ".join([p.get_text() for p in paragraphs])
        
        # Truncate if too long to avoid token limits in the prompt step
        return text_content[:10000] 
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# --- 2. Dspy Prompt Engineering ---
class PageToImagePrompt(dspy.Signature):
    """Generates a detailed image generation prompt based on web page content."""
    
    page_content = dspy.InputField(desc="The text content of a web page.")
    image_prompt = dspy.OutputField(desc="A detailed, creative prompt for an AI image generator describing a visual representation of the page's core theme.")

def generate_image_prompt(page_text):
    """Uses dspy to create an optimized image prompt."""
    # Configure dspy to use a text model for reasoning (using a standard Gemini model)
    # Note: dspy.Google requires `google-generativeai` but we are using `google-genai` for the image part.
    # dspy's Google provider might need the older lib or specific setup. 
    # For simplicity in this script, we assume the user has a dspy-compatible LM set up.
    # If not, we'll configure a default one here using the same API key if possible, 
    # or rely on the user's environment.
    
    # Using Gemini 1.5 Flash for the text reasoning part as it's fast and cheap
    # Updated to use dspy.LM which supports Gemini via the 'gemini/' prefix
    # Using 'gemini-1.5-flash-latest' to avoid versioning issues
    lm = dspy.LM("gemini/gemini-2.5-flash", api_key=API_KEY)
    dspy.settings.configure(lm=lm)

    generate_prompt = dspy.ChainOfThought(PageToImagePrompt)
    result = generate_prompt(page_content=page_text)
    return result.image_prompt

# --- 3. Nano Banana Image Generation ---
def generate_nano_banana_image(prompt, output_file="generated_image.png"):
    """Generates an image using the Nano Banana (Gemini 3 Pro Image) model."""
    # print(f"Generating image with prompt: {prompt}") # Removed per user request
    
    client = genai.Client(api_key=API_KEY)
    
    try:
        response = client.models.generate_content(
            model=PRO_MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['Image'],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                )
            )
        )
        
        for part in response.parts:
            if image := part.as_image():
                image.save(output_file)
                print(f"Image saved to {output_file}")
                return output_file
                
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

# --- Main Execution ---
if __name__ == "__main__":
    # Example usage
    target_url = input("Enter a URL to turn into an image: ")
    
    print("Scraping webpage...")
    content = scrape_webpage(target_url)
    
    if content:
        print("Generating prompt with dspy...")
        try:
            image_prompt = generate_image_prompt(content)
            print(f"Generated Prompt: {image_prompt}")
            
            print("Calling Nano Banana...")
            generate_nano_banana_image(image_prompt)
            
        except Exception as e:
            print(f"An error occurred during the process: {e}")
    else:
        print("Failed to retrieve content.")
