import telebot
from config import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from termcolor import colored

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

if __name__ == '__main__':
    import time
    while True:
        try:
            print(colored("Bot is restarted ...", 'yellow'))
            bot.polling(none_stop=True,restart_on_change=True,timeout=40)    
        except:
            print("Bot got an error trying again after 3sec ...")
            time.sleep(3)
