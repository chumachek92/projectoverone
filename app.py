import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def echo_test(message: telebot.types.Message):
    text = 'Привет! Я Бот-Конвертер валют. \n\
Чтобы начать работу введите команду Боту в следующем формате:\nимя переводимой валюты \
в какую валюту перевести \
количество переводимой валюты\n\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров. \n/help')

        quote, basec, amount = values
        total_base = CryptoConverter.get_price(quote, basec, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        result = round((float(amount) * float(total_base)), 2)
        text = f'Цена {amount} {quote} в {basec} = {result}'
        bot.send_message(message.chat.id, text)


bot.polling()