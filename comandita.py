import re
from time import sleep

import requests
from telegram.error import Unauthorized
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.updater import Updater
from telegram.ext.dispatcher import Dispatcher
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.bot import Bot

updater = Updater(
    "1536716016:AAGDdwMXhDQoxia_9FaR0d-buchH8j8z9c0",
    use_context=True,
)


OPEN_WEATHER_MAP_APP_ID = "1234"


dispatcher: Dispatcher = updater.dispatcher


def mimimi(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    try:
        response = re.sub('[aeou]', 'i', update.message.reply_to_message.text, flags=re.I)
    except AttributeError:
        bot.send_message(
            chat_id=update.effective_chat.id,
            text="No puedo hacer mimimi sin citar un mensaje... 😢",
        )
        return
    response = re.sub('[AEOU]', 'I', response, flags=re.I)
    response = re.sub('[áéóú]', 'í', response, flags=re.I)
    response = re.sub('[ÁÉÓÚ]', 'Í', response, flags=re.I)
    response = re.sub('[àèòù]', 'ì', response, flags=re.I)
    response = re.sub('[ÀÈÒÙ]', 'Ì', response, flags=re.I)
    response = re.sub('[äëöü]', 'ï', response, flags=re.I)
    response = re.sub('[ÄËÖÜ]', 'Ï', response, flags=re.I)

    bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
    )


def sentenciador(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="Esto tiene, por lo menos, 3 días.",
    )


def star(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    try:
        bot.send_message(
            chat_id=update.message.from_user.id,
            text=update.message.reply_to_message.text,
        )
    except Unauthorized:
        bot.send_message(
            chat_id=update.effective_chat.id,
            text="Antes de poder enviarte mensajes "
                 "tienes que iniciar una conversación "
                 "conmigo en https://t.me/comandita_bot",
        )
    except AttributeError:
        bot.send_message(
            chat_id=update.effective_chat.id,
            text="Cita un mensaje que quieras guardar ⭐️",
        )


def weather_in_korea(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="Dormida... 😡"
    )
    sleep(2)
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="No, en serio, ahora te digo."
    )
    sleep(1)
    query = {
        "q": "Seoul",
        "appid": OPEN_WEATHER_MAP_APP_ID,
        "units": "metric",
    }
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params=query,
    )
    weather_data = response.json()
    weather_text = ", ".join([weather.get("main", "") for weather in weather_data.get("weather", [])])
    temperature = weather_data.get("main", {})
    temp = temperature.get("temp", 0)
    feels_like = temperature.get("feels_like", 0)
    temp_min = temperature.get("temp_min", 0)
    temp_max = temperature.get("temp_max", 0)
    bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Weather: {weather_text}\n"
             f"Temp: {temp}ºC\n"
             f"Feels like: {feels_like}ºC\n"
             f"Min: {temp_min}ºC\n"
             f"Max: {temp_max}ºC",
    )


dispatcher.add_handler(CommandHandler("mimimi", mimimi))
dispatcher.add_handler(CommandHandler("sentenciador", sentenciador))
dispatcher.add_handler(CommandHandler("star", star))
dispatcher.add_handler(CommandHandler("tiempoencorea", weather_in_korea))
updater.start_polling()
