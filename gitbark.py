import os
import requests
from google import genai
from google.genai import types

# 1. Setup Environment Variables
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CATEGORY = os.getenv("CATEGORY_OVERRIDE", "Dogs")

def main():
    # --- STEP 1: Generate Story (Gemini) ---
    client = genai.Client(api_key=GOOGLE_API_KEY)
    story_prompt = f"Write a short, whimsical 2-sentence Facebook post about: {CATEGORY}. Use emojis."
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite", 
        contents=story_prompt
    )
    story_text = response.text
    print(f"Story Generated: {story_text}")

    # --- STEP 2: Generate Image (Imagen) ---
    image_generated = False
    image_path = "generated_image.png"
    
    try:
        # Utilizing Imagen 3 via Vertex AI / AI Studio
        img_response = client.models.generate_images(
            model="imagen-3.0-generate-001",
            prompt=f"A cinematic, high-quality photo of {CATEGORY} in a playful setting.",
            config=types.GenerateImagesConfig(number_of_images=1)
        )
        
        # Save the image locally for upload
        img_response.generated_images[0].image.save(image_path)
        image_generated = True
        print("✅ Image generated successfully.")
    except Exception as e:
        print(f"⚠️ Image generation failed: {e}")
        print("Falling back to text-only post.")

    # --- STEP 3: Upload to Facebook ---
    print("Uploading to Facebook...")
    
    if image_generated:
        # Use /me/photos to post directly to the Page's timeline
        fb_url = "https://graph.facebook.com/v20.0/me/photos"
        payload = {
            'message': story_text,
            'access_token': FB_ACCESS_TOKEN
        }
        files = {
            'source': open(image_path, 'rb')
        }
        fb_response = requests.post(fb_url, data=payload, files=files)
    else:
        # Fallback to text-only if image generation fails
        fb_url = "https://graph.facebook.com/v20.0/me/feed"
        payload = {
            'message': story_text,
            'access_token': FB_ACCESS_TOKEN
        }
        fb_response = requests.post(fb_url, data=payload)

    # --- STEP 4: Verify Result ---
    result = fb_response.json()
    if "id" in result or "post_id" in result:
        print(f"🚀 SUCCESS! Post is live. ID: {result.get('id', result.get('post_id'))}")
    else:
        print(f"❌ FB Error: {result}")

if __name__ == "__main__":
    main()