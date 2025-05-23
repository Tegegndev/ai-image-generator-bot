import telebot
from config import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from termcolor import colored
from utils import image_generator_api


bot = telebot.TeleBot(BOT_TOKEN,colorful_logs=True,)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup()
    ABOUT_BUTTON = InlineKeyboardButton(text='About', callback_data='about')
    HELP_BUTTON = InlineKeyboardButton(text='Help', callback_data='help')
    example_button = InlineKeyboardButton(text='Example Prompt', callback_data='example')
    keyboard.add(example_button)
    keyboard.add(ABOUT_BUTTON,HELP_BUTTON)
    welcome_message = f'''
    Selam {message.from_user.first_name}
Welcome to AI Image Generator Bot
just send your prompt and I will generate an image for you
    '''
    
    bot.reply_to(message,welcome_message,reply_markup=keyboard)
    bot.register_next_step_handler(message, ask_prompt)


def ask_prompt(message):
    prompt = message.text
    bot.send_message(message.chat.id, f"generating image")
    print(prompt)
    result = image_generator_api(prompt)
    print(result, message)
    bot.send_photo(message.from_user.id,result)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat_id, 'help here')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'about':
        bot.send_message(call.message.chat.id, 'This is a bot that generates images from text prompts using AI.')
    elif call.data == 'help':
        bot.send_message(call.message.chat.id, 'This is a bot that generates images from text prompts using AI.')
    elif call.data == 'example':
        bot.send_message(call.message.chat.id, 'Example prompt: "A beautiful sunset over the mountains."')
    else:
        bot.send_message(call.message.chat.id, 'Unknown command.')   


#handleforwared messages
@bot.message_handler(content_types=['text'], func=lambda message: message.forward_from)
def handle_forwarded_message(message):
    print(colored(f"Received forwarded message: {message.text}", 'blue'))
    bot.reply_to(message, "I can't process forwarded messages yet.")    

#handle incoming messages
@bot.message_handler(content_types=['text'])
def all_messages(message):
    
    if message.text.startswith('/'):
        print('coomand recieved')
    else:
        print(colored(f"Received message: {message.text}", 'green'))
        ask_prompt(message)
        bot.register_next_step_handler(message, ask_prompt)

if __name__ == '__main__':
        print(colored("Bot is restarted ...", 'yellow'))
        bot.polling(timeout=40)    
            
