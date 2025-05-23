import telebot
from config import *

bot = telebot.TeleBot(BOT_TOKEN,colorful_logs=True,)


@bot.message_handler(commands=['start'])
def start(messgae):
    bot.send_message(messgae.chat.id, 'Hello, I am a bot!')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat_id, 'help here')

bot.polling(none_stop=True,restart_on_change=True)    