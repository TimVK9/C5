import telebot
import time
from config import TOKEN, keys
from extensions import APIException, Convert

bot = telebot.TeleBot(TOKEN, skip_pending=True)


@bot.message_handler(commands=['start', 'help'])
def function_name(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Привет, {message.chat.username}.')
    time.sleep(1)
    bot.send_message(message.chat.id, f'\n \n Посмотреть доступные для конвертации валюты  \n\n➡️ /values')


@bot.message_handler(commands=['values'])
def function_name(message: telebot.types.Message):
    text = '💰 Доступные валюты: \n'
    for i in keys:
        text = '\n▶️ '.join((text, i))
    bot.send_message(message.chat.id, f'{text} \n\n❇️ Введите значения через запятую- '
                                      f'валюта, в какую валюту конвертировать, колличество\n')


@bot.message_handler(content_types=['text'])
def conv(message: telebot.types.Message):
    try:

        inp = message.text.lower().split(', ')

        if len(inp) != 3:
            raise APIException('Проверьте параметры! ')

        base, quote, amount = inp
        j = Convert.get_price(base, quote, amount)

    except APIException as e:
        bot.send_message(message.chat.id, f'Что-то пошло не так! \n{e}')

    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать!\n{e}')
    else:

        text = f'Цена {amount} {base} в {quote} - {j} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
