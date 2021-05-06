import telebot
import requests
import json
from telebot import types
from threading import Thread
import schedule
city = None
time = "15:58"
bot = telebot.TeleBot('1105108305:AAEhW5-hfSAxtypvGEelbCk11DNvLXcBXPc')
def get_updates():
            url = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&appid=0d7d40be98eaac6a5e34556ab6369891'.format(city))
            jsonresponse = json.loads(url.text)
            return jsonresponse
def runA():
    while True:
        try:
            schedule.every().day.at(time).do(check_weather)
        except:
            pass
def check_weather(message):
     bot.send_message(message.chat.id, "Weather: {}\nTemperature: {}°C\nHumidity: {}%\nPressure: {}\nWind speed: {}km/h".format(get_updates()['weather'][0]['description'], get_updates()['main']['humidity'],float(get_updates()['main']['pressure'])/1.3333,get_updates()['wind']['speed']), reply_markup = keyboard)
@bot.message_handler(content_types=["text"])
def handle_messages(message):  
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard = True)
    global chat_id
    chat_id = message.chat.id
    if message.text == 'Hello':
        button_1 = types.KeyboardButton(text="Choose city")
        button_2 = types.KeyboardButton(text="Find out the weather")
        button_3 = types.KeyboardButton(text="Change alert time")
        keyboard.add(button_1, button_2, button_3)
        bot.send_message(message.chat.id, "Hello", reply_markup = keyboard)
    if message.text == 'Choose city':
        keyboard_hider = types.ReplyKeyboardRemove()
        ask = bot.send_message(message.chat.id, "Write the name of the city (with a capital letter)", reply_markup = keyboard_hider)
        bot.register_next_step_handler(ask,choose_city)
    if message.text == 'Change alert time':
        keyboard_hider = types.ReplyKeyboardRemove()
        ask2 = bot.send_message(message.chat.id, "Write a weather alert time", reply_markup = keyboard_hider)
        bot.register_next_step_handler(ask2,choose_time)
    if message.text == 'Find out the weather':
        if city == None:
            bot.send_message(message.chat.id, "City is not found", reply_markup = keyboard)
        else:
            bot.send_message(message.chat.id, "Weather: {}\nTemperature: {}°C\nHumidity: {}%\nPressure: {}\nWind speed: {}km/h".format(get_updates()['weather'][0]['description'],
                                                                                                                                                       int(get_updates()['main']['temp'])-273,
                                                                                                                                                       get_updates()['main']['humidity'],
                                                                                                                                                       float(get_updates()['main']['pressure'])/1.3333,get_updates()['wind']['speed']), reply_markup = keyboard)
def choose_time(message):
    global time
    time = message.text
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard = True)
    button_1 = types.KeyboardButton(text="Choose city")
    button_2 = types.KeyboardButton(text="Find out the weather")
    button_3 = types.KeyboardButton(text="Change alert time")
    keyboard.add(button_1, button_2, button_3)
    bot.send_message(message.chat.id, "Time changed. The time is {}".format(time), reply_markup = keyboard)
@bot.message_handler(content_type=['text'])
def choose_city(message):
    global city
    city = message.text
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard = True)
    button_1 = types.KeyboardButton(text="Choose city")
    button_2 = types.KeyboardButton(text="Find out the weather")
    button_3 = types.KeyboardButton(text="Change alert time")
    keyboard.add(button_1, button_2, button_3)
    if check():
        bot.send_message(message.chat.id, "The city is selected. The city is {}".format(city), reply_markup = keyboard)
    else:
        mes = bot.send_message(message.chat.id, "City not found. Please try again")
        bot.register_next_step_handler(mes,choose_city)
def check():
    try:
        print(get_updates()['message'])
        return False
    except:
        return True
    

if __name__ == '__main__':
    t1 = Thread(target = runA)
    t1.setDaemon(True)
    t1.start()
    bot.polling(none_stop=True)
