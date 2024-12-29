import telebot
from random import randint

bot = telebot.TeleBot('7596099729:AAHLSEVCBLO0RhNVZjNrB1HnHZNHkL6UHC0')

verification_codes = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    code = str(randint(100000, 999999))
    verification_codes[user_id] = code
    
    bot.reply_to(message, f"Добро пожаловать в Эко Долину! \nВаш код верификации: {code}\n\nВведите этот код при регистрации на сайте.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Используйте команду /start для получения кода верификации.")

bot.polling()