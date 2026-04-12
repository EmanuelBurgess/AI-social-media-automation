import os
import random
import requests
import pathlib
from google import genai
from google.genai import types

# --- CONFIGURATION ---
# Ensure these environment variables are set in your terminal or .env file
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
MODEL_ID = "gemini-2.5-flash-lite"

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Categories
CATEGORIES = ["Dogs"]

def main():
    # 1. Setup workspace
    tmp_dir = pathlib.Path("./fb_tmp")
    tmp_dir.mkdir(exist_ok=True)
    
    category = random.choice(CATEGORIES)
    print(f"Category: {category}")

    # 2. Generate Story
    print("Generating Story...")
    story_prompt = f"Write a whimsical story about {category.lower()} for Facebook. Include a bold headline, 3-5 engaging paragraphs, and relevant hashtags."
   
    
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
    print("Story Generated.")

    # 3. Generate Image
    print("Generating Image...")
    image_path = tmp_dir / "post_image.jpg"
    image_generated = False
    
    try:
        # Note: Using Imagen 3 via GenAI SDK
        img_response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=f"Cinematic realistic photo for: {headline}. No words in generated image.",
            config=types.GenerateImagesConfig(number_of_images=1)
        )
        
        if img_response.generated_images:
            # Save the first image found
            img_response.generated_images[0].image.save(str(image_path))
            image_generated = True
            print("Image generated and verified.")
    except Exception as e:
        print(f"Image generation failed or not supported: {e}")
        print("Falling back to text-only mode.")

    # 4. Upload to Facebook
    print("Uploading...")
    
    if image_generated:
        # Post with Photo
        url = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/photos"
        payload = {"caption": content, "access_token": FB_ACCESS_TOKEN}
        with open(image_path, "rb") as img_file:
            files = {"source": img_file}
            fb_res = requests.post(url, data=payload, files=files)
    else:
        # Post Text Only
        url = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/feed"
        payload = {"message": content, "access_token": FB_ACCESS_TOKEN}
        fb_res = requests.post(url, data=payload)

    # 5. Verify
    result = fb_res.json()
    if "id" in result:
        print("SUCCESS! Post is live.")
        print(f"Post ID: {result['id']}")
    else:
        print(f"FB Error: {result}")

    # Cleanup is handled automatically if you use temporary directories, 
    # but for this script, we'll leave the folder or delete it manually:
    # import shutil; shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    main()
    