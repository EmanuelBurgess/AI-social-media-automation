import os
import random
import requests
import pathlib
from google import genai
from google.genai import types

# --- CONFIGURATION ---
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
# Using the stable ID for the demo
MODEL_ID = "gemini-2.5-flash-lite" 

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Default Categories
CATEGORIES = ["Pit Bull", "Dogo Argentinos", "Guardian Dogs"]

def main():
    # 1. Setup workspace
    tmp_dir = pathlib.Path("./fb_tmp")
    tmp_dir.mkdir(exist_ok=True)
    
    # --- LOGIC FOR GITHUB ACTIONS MANUAL INPUT ---
    # This pulls from the 'category_override' input in your YAML
    override = os.getenv("CATEGORY_OVERRIDE")
    if override and override.strip():
        category = override
        print(f"Using manual override category: {category}")
    else:
        category = random.choice(CATEGORIES)
        print(f"Using random category: {category}")

    # 2. Generate Story
    print("Generating Story...")
    story_prompt = f"Write a whimsical, short Facebook story about {category.lower()}. Include a bold headline, 3 paragraphs, and dog-related hashtags."
    
    try:
        response = client.models.generate_content(model=MODEL_ID, contents=story_prompt)
        content = response.text
        if not content:
            raise ValueError("Empty response from model.")
    except Exception as e:
        print(f"Story failed: {e}")
        return

    # Extract headline (first line)
    headline = content.split('\n')[0].strip('# ')
    print(f"Story Generated: {headline}")

    # 3. Generate Image
    print("Generating Image...")
    image_path = tmp_dir / "post_image.jpg"
    image_generated = False
    
    try:
        # Note: Using latest Imagen model version
        img_response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=f"Cinematic realistic photo of a {category} dog in a high-tech office. {headline}. No text in image.",
            config=types.GenerateImagesConfig(number_of_images=1)
        )
        
        if img_response.generated_images:
            img_response.generated_images[0].image.save(str(image_path))
            image_generated = True
            print("Image generated successfully.")
    except Exception as e:
        print(f"Image generation failed: {e}")
        print("Falling back to text-only post.")

    # 4. Upload to Facebook
    print("Uploading to Facebook...")
    
    if image_generated:
        url = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/photos"
        payload = {"caption": content, "access_token": FB_ACCESS_TOKEN}
        with open(image_path, "rb") as img_file:
            files = {"source": img_file}
            fb_res = requests.post(url, data=payload, files=files)
    else:
        url = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/feed"
        payload = {"message": content, "access_token": FB_ACCESS_TOKEN}
        fb_res = requests.post(url, data=payload)

    # 5. Verify Result
    result = fb_res.json()
    if "id" in result:
        print(f"SUCCESS! View post at: https://facebook.com/{result['id']}")
    else:
        print(f"FB Error: {result}")

if __name__ == "__main__":
    main()