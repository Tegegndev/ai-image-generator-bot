import telebot
from config import *
import ssl
import warnings



bot = telebot.TeleBot(BOT_TOKEN,colorful_logs=True,)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, I am a bot! built by tegegn w w')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat_id, 'help here')

if __name__ == '__main__':
    print("Bot is restarted ...")
    bot.polling(none_stop=True,restart_on_change=True,timeout=40)    