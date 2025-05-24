# 🖼️ AI Image Generator Bot

Welcome to the **AI Image Generator Bot**! This project leverages state-of-the-art AI models to generate stunning images from text prompts.

## 🚀 Features

- Generate images from natural language descriptions
- Fast and scalable backend

## 📦 Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/ai_image_gen.git
    cd ai_image_gen
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure your API keys and bot settings** in `config.py`.  
   Edit `config.py` to set your `BOT_TOKEN`, `API_URL`, `CHANNEL_USERNAME`, `WEBHOOK_URL`, and other options.

## 🛠️ Usage

- **Start the bot and Flask app:**
  ```bash
  python -m ai_image_gen
  ```
  or, if running directly:
  ```bash
  python __init__.py
  ```
- **Interact via Telegram:**  
  Send a text prompt to the bot and receive generated images in seconds!

## 📝 Example

```
Prompt: "A futuristic cityscape at sunset"
```
![Example Image](assets/example_cityscape.png)

## 🤖 Technologies

- Python
- Telegram Bot API
- AI image generation models (Stable Diffusion, DALL-E, etc.)
- Flask

## 📄 License

MIT License

---

> Made with ❤️ for creative minds.