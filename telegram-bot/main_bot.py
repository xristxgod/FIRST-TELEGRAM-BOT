import datetime

import telebot
import requests
import json
import lxml.html

import config as cnf
from extensions import (
    ConvertionExceprion,
    CryptoConverter,
    UserDB,
    VGPrice
)


# Подключаем бота
bot = telebot.TeleBot(cnf.TOKEN)

DB = UserDB()

@bot.message_handler(commands=['start', 'help'])
def start_or_help(message: telebot.types.Message):

    ''' Функция команд: /help и /start '''

    text = 'Список всех доступных валют: /values \n' \
           'Конвертировать валюты: /set \n' \
           'Узнать цену акций Virgin Galactic: /get \n'

    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['get'])
def get_vg(message: telebot.types.Message):
    try:
        text = VGPrice.get_vg_price()
    except Exception as e:
        bot.send_message(message.chat.id, e)
    else:
        bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def get_all_values(message: telebot.types.Message):

    ''' Функция команды: /values '''

    text = 'Доступные валюты: \n'
    text += '\n'.join(f'{i+1}. {key}' for i, key in enumerate(cnf.KEYS))
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['set'])
def set(message: telebot.types.Message):

    ''' Функция команды: /set '''
    ''' Вывод двух Keyboards со списками валют'''

    markup = telebot.types.InlineKeyboardMarkup()
    for val, form in cnf.KEYS.items():
        button = telebot.types.InlineKeyboardButton(text=val, callback_data=f'val1 {form}')
        markup.add(button)

    bot.send_message(chat_id=message.chat.id, text='Выберите валюту, из которой будем конвертировать', reply_markup=markup)

    markup = telebot.types.InlineKeyboardMarkup()
    for val, form in cnf.KEYS.items():
        button = telebot.types.InlineKeyboardButton(text=val, callback_data=f'val2 {form}')
        markup.add(button)

    bot.send_message(chat_id=message.chat.id, text='Выберите валюту, в которую будем конвертировать',
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def get_value(call):

    ''' Функция команды: /set '''
    ''' Реакция на изменения валюты '''

    t, st = call.data.split()
    user_id = call.message.chat.id
    if t == 'val1':
        DB.change_from(user_id, st)
    if t == 'val2':
        DB.change_too(user_id, st)

    pair = DB.get_pair(user_id)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'Теперь конвертируем из {pair[0]} в {pair[1]}')

@bot.message_handler(content_types=['text', ])
def get_values(message: telebot.types.Message):

    ''' Функция команды: /set '''
    ''' Вывод цены валюты '''

    pair = DB.get_pair(message.chat.id)
    values = [*pair, message.text.strip()]
    try:

        total = CryptoConverter.convert(values)

    except ConvertionExceprion as c:
        bot.send_message(message.chat.id, f'Ошибка пользователя. \n{c}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду\n{e}')
    else:
        text = f'{values[2]} {values[0]} -- {round(total, 2)} {values[1]}'
        bot.send_message(message.chat.id, text)


# Run bot

bot.polling(none_stop=True, interval=0)



