# Nano Banana Image Generator

This Python script generates "Nano Banana" (Gemini 3 Pro Image) images based on the content of a web page.

## Features
- **Web Scraping**: Extracts text from a given URL.
- **Prompt Engineering**: Uses `dspy` with a Gemini text model to create optimized image prompts.
- **Image Generation**: Uses the `google-genai` SDK to call the `gemini-3-pro-image-preview` model.

## Files
- `nano_banana_gen.py`: The main script.
- `requirements.txt`: Python dependencies.
- `debug_models.py`: Helper to list available models.

## Setup & Usage

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: Ensure `google-generativeai` is installed if you encounter module errors.*

2.  **Set API Key**:
    ```bash
    export GOOGLE_API_KEY="your_api_key"
    ```

3.  **Run the Script**:
    ```bash
    python nano_banana_gen.py
    ```
    Enter a URL when prompted. The script will save the output as `generated_image.png`.

## Configuration Notes
- **Billing**: You must enable billing on your Google Cloud project to use `gemini-3-pro-image-preview`.
- **Models**:
    - Image Model: `gemini-3-pro-image-preview` (Nano Banana Pro)
    - Text Model (for dspy): `gemini-2.5-flash` (or similar available text model)

## Troubleshooting
- If you see `models/gemini-X not found`, run `python debug_models.py` to see the exact model names available to your API key and update `nano_banana_gen.py` accordingly.
