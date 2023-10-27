import telebot
import requests, json
from telebot import types

API = '' #API бота

bot = telebot.TeleBot('') #API вашего бота

@bot.message_handler(commands=["start"])
def start(message):
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id, f'Я на связи, {user_name}! Напиши мне город, чтобы узнать погоду.')

@bot.message_handler(content_types=["text"])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = res.json()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        
        response_message = f'Погода на данный момент: {temperature}°C\n' \
                           f'Влажность: {humidity}%\n' \
                           f'Давление: {pressure} Па'
        bot.reply_to(message, response_message)
    else:
        bot.reply_to(message, 'Город не найден. Пожалуйста, проверьте правильность написания.')
        
@bot.message_handler(commands=["button"])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Кнопка 1")
    item2 = types.KeyboardButton("Кнопка 2")
    markup.add(item1, item2)
    
    bot.send_message(message.chat.id, 'Выберите что вам надо:', reply_markup=markup)

bot.polling()
