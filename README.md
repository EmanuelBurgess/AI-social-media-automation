

# 🚀 AI Facebook Reel & Story Automator (2026 Edition)

An advanced, production-ready Python automation engine that researches, writes, renders, and publishes high-fidelity **Facebook Reels** and **Stories** using the Google Gemini 3 ecosystem and Facebook Graph API v20.0.

![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![AI Models](https://img.shields.io/badge/AI-Gemini%203%20%7C%20Veo%203.1%20%7C%20Imagen%204-orange.svg)

## ✨ Features

* **Multimodal AI Pipeline**:
    * **Scripting**: Powered by `gemini-3-flash-preview` for high-retention social hooks.
    * **Video**: Cinematic 9:16 vertical video with native audio via `veo-3.1-generate-preview`.
    * **Teasers**: High-resolution 4K story images via `imagen-4.0-generate-001`.
* **Smart Scheduling**: Built-in logic for a hybrid posting strategy (1x Daily Weekdays / 2x Daily Weekends) to maximize ROI.
* **Robust Upload Engine**: Handles the complex 3-step Facebook Resumable Upload protocol (Initialize -> Binary Stream -> Publish).
* **Auto-Cleanup**: Self-managing temporary workspace to keep your host machine clean.

## 🛠️ Tech Stack

* **Language**: Python 3.14+
* **AI SDK**: `google-genai` (2026 Release)
* **API**: Facebook Graph API v20.0
* **Libraries**: `requests`, `pathlib`, `datetime`

## 🚀 Installation

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/your-username/fb-reel-automator.git](https://github.com/your-username/fb-reel-automator.git)
    cd fb-reel-automator
    ```

2.  **Install Dependencies**:
    *Note: Using `--break-system-packages` is required on modern macOS if not using a virtual environment.*
    ```bash
    pip3 install -U google-genai requests --break-system-packages
    ```

3.  **Configure Environment Variables**:
    Add these to your `~/.zshrc` or `~/.bash_profile`:
    ```bash
    export GOOGLE_API_KEY="your_google_key"
    export FB_PAGE_ID="your_page_id"
    export FB_ACCESS_TOKEN="your_long_lived_page_token"
    ```

## 📋 Usage

### Manual Run
Force a post immediately (ignoring the scheduler):
```bash
python3 main.py
