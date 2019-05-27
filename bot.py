#!/usr/bin/python
# -*- coding: utf-8 -*-
# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
updater = Updater(token='717381707:AAGlKxbztgPz04I-FGsHzMYsw7Vnptesd6o') # Токен API к Telegram
dispatcher = updater.dispatcher

# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')

def textMessage(bot, update):
    request = apiai.ApiAI('fd8b3bc4ae3b4aa689614aa6f5aef889').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'danil_stepanov_bot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    print(update.message.text)
    if update.message.text == 'Как тебя зовут':
        bot.send_message(chat_id=update.message.chat_id, text='Я Петя! Кожанный ты мешок!')

    elif 'переведи:' in update.message.text:
        answer = update.message.text
        answer.split(':')
        print(answer.split(':')[1])
    else:
        request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
        # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
        print(response)
        if response:
            bot.send_message(chat_id=update.message.chat_id, text=response)
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')

# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
