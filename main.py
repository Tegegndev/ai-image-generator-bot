import telebot
from config import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from termcolor import colored
from utils import image_generator_api
import time



bot = telebot.TeleBot(BOT_TOKEN, colorful_logs=True,)

def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(colored(f"Error checking channel membership: {e}", 'red'))
        return False

def force_join_channel(message):
    keyboard = InlineKeyboardMarkup()
    join_button = InlineKeyboardButton(
        text="🔗 Join @tegegndev", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")
    check_button = InlineKeyboardButton(
        text="✅ I've Joined", callback_data='check_join')
    keyboard.add(join_button)
    keyboard.add(check_button)
    bot.send_message(
        message.chat.id,
        "🚫 To use this bot, please join our channel first:",
        reply_markup=keyboard
    )

@bot.message_handler(commands=['start'])
def start(message):
    if not is_user_in_channel(message.from_user.id):
        force_join_channel(message)
        return
    keyboard = InlineKeyboardMarkup()
    ABOUT_BUTTON = InlineKeyboardButton(text='ℹ️ About', callback_data='about')
    HELP_BUTTON = InlineKeyboardButton(text='❓ Help', callback_data='help')
    example_button = InlineKeyboardButton(text='💡 Example Prompt', callback_data='example')
    keyboard.add(example_button)
    keyboard.add(ABOUT_BUTTON, HELP_BUTTON)
    welcome_message = f'''
👋 Selam {message.from_user.first_name}!

🖼️ Welcome to AI Image Generator Bot.
Just send your prompt and I will generate an image for you! ✨
    '''
    bot.reply_to(message, welcome_message, reply_markup=keyboard)
    bot.register_next_step_handler(message, ask_prompt)

def send_typing_action(chat_id):
    bot.send_chat_action(chat_id, 'typing')


user_prompts = {}

def ask_prompt(message, prompt=None):
    if not is_user_in_channel(message.from_user.id):
        force_join_channel(message)
        return
    keyboard = InlineKeyboardMarkup()
    generate_again_btn = InlineKeyboardButton(text='🔄 Generate Again', callback_data='generate_again')
    keyboard.add(generate_again_btn)
    if prompt is None:
        prompt = message.text

    # Save to dict the promopt
    user_prompts[message.from_user.id] = prompt

    # Typing effect
    send_typing_action(message.chat.id)
    time.sleep(1.2)

 
    try:
        if hasattr(message, 'reply_to_message') and message.reply_to_message:
            bot.delete_message(message.chat.id, message.reply_to_message.message_id)
    except Exception as e:
        pass

    bot.send_message(message.chat.id, "🎨 Generating your image, please wait...")

    print(prompt)
    result = None
    retries = 3
    for attempt in range(retries):
        try:
            result = image_generator_api(prompt)
            if result:
                break
        except Exception as e:
            print(colored(f"API error: {e}", 'red'))
        time.sleep(1)

    if result:
        # Always send to the chat where the user is, not to from_user.id
        sent_msg = bot.send_photo(message.chat.id, result, reply_markup=keyboard)
        bot.register_next_step_handler(message, ask_prompt, prompt)
    else:
        bot.send_message(message.chat.id, "❌ Failed to generate image. Please try again later.")

@bot.message_handler(commands=['help'])
def help(message):
    help_text = (
        "❓ *How to use AI Image Generator Bot*\n\n"
        "1️⃣ *Send a prompt*: Just type a description of the image you want. Example: _A cat riding a skateboard in space._\n"
        "2️⃣ *Wait for the image*: The bot will generate and send you an AI-created image based on your prompt.\n"
        "3️⃣ *Enhance*: Use the '🚀 Enhance with AI' button to further improve your generated image.\n\n"
        "*Tips:*\n"
        "- Be as descriptive as possible for better results.\n"
        "- Try different prompts for creative outputs.\n\n"
        "💬 *Commands:*\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n\n"
        "For support or feedback, join our channels or contact the developer."
    )
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'about':
        about_text = (
            "ℹ️ *About  Bot*\n\n"
            "This bot generates images from text prompts using AI.\n\n"
            "🌐 *Channels:*\n"
            "• [@tegegndev](https://t.me/tegegndev)\n"
            "• [@yegna_tv](https://t.me/yegna_tv)\n\n"
            "💻 *GitHub:*\n"
            "• [tegegn dev](https://github.com/tegegn-dev)\n"
        )
        bot.send_message(call.message.chat.id, about_text, parse_mode='Markdown', disable_web_page_preview=True)
    elif call.data == 'help':
        bot.send_message(call.message.chat.id, '❓ Send me a prompt and I will generate an AI image for you!')
    elif call.data == 'example':
        bot.send_message(call.message.chat.id, '💡 Example prompt: "A beautiful sunset over the mountains."')
    elif call.data == 'ai' or call.data == 'generate_again':
        # Use the last prompt from user state
        last_prompt = user_prompts.get(call.from_user.id)
        if last_prompt:
            ask_prompt(call.message, prompt=last_prompt)
        else:
            bot.send_message(call.message.chat.id, "❗ Could not find the previous prompt. Please send a new prompt.")
    elif call.data == 'check_join':
        if is_user_in_channel(call.from_user.id):
            bot.send_message(call.message.chat.id, "✅ Thank you for joining! Now you can use the bot.")
            start(call.message)
            # Optionally, you can call start or ask_prompt again here
        else:
            force_join_channel(call.message)
    else:
        bot.send_message(call.message.chat.id, '❗ Unknown command.')

# handle forwarded messages
@bot.message_handler(content_types=['text'], func=lambda message: message.forward_from)
def handle_forwarded_message(message):
    print(colored(f"Received forwarded message: {message.text}", 'blue'))
    bot.reply_to(message, "⚠️ I can't process forwarded messages yet.")

# handle incoming messages
@bot.message_handler(content_types=['text'])
def all_messages(message):
    if message.text.startswith('/'):
        print('Command received')
    else:
        print(colored(f"Received message: {message.text}", 'green'))
        if not is_user_in_channel(message.from_user.id):
            force_join_channel(message)
            return
        ask_prompt(message)
        bot.register_next_step_handler(message, ask_prompt)

if __name__ == '__main__':
    print(colored("🤖 Bot is restarted ...", 'yellow'))
    bot.polling(timeout=40)

