from flask import Flask
from flask import render_template
from main import bot  # changed from .main to main
from config import IN_PRODUCTION, WEBHOOK_URL
from termcolor import colored

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World! This is a Flask app running with the Telegram bot."

if __name__ == "__main__":
    if IN_PRODUCTION:
        print(colored("🌐 Running in production mode with webhook...", 'green'))
        bot.remove_webhook()
        #bot.set_webhook(url=WEBHOOK_URL)
        app.run(host='0.0.0.0')
        print(colored("🤖 Bot is restarted ...", 'yellow'))
    else:
        print(colored("🤖 Running in development mode with polling...", 'green'))
        bot.polling(timeout=40)

