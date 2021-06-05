import telebot
import requests
import json

import config as cnf


from extensions import ConvertionExceprion, CryptoConverter

# Подключаем бота
bot = telebot.TeleBot(cnf.TOKEN)




@bot.message_handler(commands=['start', 'help'])
def start_or_help(message: telebot.types.Message):

    ''' Ответ на команды /help и /start '''

    text = 'Список всех доступных валют: /values \n' \
           'Что бы узнать цену валюты в другой валюте:  ' \
           '<имя валюты, цену которой нужно узнать> <имя валюты, в которой надо перевести> <количество первой валюты>' \

    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def get_all_values(message: telebot.types.Message):


    ''' Ответ на команду /values '''

    text = 'Доступные валюты: \n'
    for key in cnf.KEYS:
        text = '\n'.join((text, key, ))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text', ])
def get_values(message: telebot.types.Message):

    ''' Вывод цены криптовалюты в нужной валюте '''

    try:
        values = message.text.title().split(' ')
        if len(values) != 3: raise ConvertionExceprion('Слишком много параметров')
        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionExceprion as c:
        bot.send_message(message.chat.id, f'Ошибка пользователя. \n{c}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

# Run bot
bot.polling(none_stop=True)



