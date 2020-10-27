from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from .log import logger
from .config import Config

from threading import Thread
import datetime
import re
import schedule
import pandas as pd

from . import get_weather, \
    user_event_handler, \
    db_tg


def university_schedule(updater, context):
    try:
        schedule_df = pd.read_csv("schedule_bot/schedule.csv")
        if updater.message.text in list(schedule_df)[1:]:
            db_tg.action2db(updater['message']['chat']['id'], updater['message']['chat']['username'], "schedule")
            updater.message.reply_text(f"Here you are:\n"
                                       f"{schedule_df[['Time', updater.message.text]].to_string(index=False)}\n")
            if schedule_df.columns[datetime.datetime.today().isoweekday()] == updater.message.text:
                updater.message.reply_text(get_weather.get_weather())
        else:
            db_tg.action2db(updater['message']['chat']['id'], updater['message']['chat']['username'], "invalid")
            updater.message.reply_text("Invalid value.")

    except (FileNotFoundError, TypeError):
        updater.message.reply_text("Can't find schedule. Sorry!")


def start(updater, message):
    updater.message.reply_text('Hi! Bring some information about my commands by /help')
    db_tg.action2db(updater['message']['chat']['id'], updater['message']['chat']['username'], "start")


def command_help(updater, context):
    updater.message.reply_text("You can check my schedule for a different days. Type a week day"
                               " and I will take you schedule for this one.\nFor example: Monday\n"
                               "If you wanna know schedule for today I will send you weather as a bonus :)"
                               "Use /remind <text> to create new date event (date format: DD.MM.YYYY).")
    db_tg.action2db(updater['message']['chat']['id'], updater['message']['chat']['username'], "help")


def command_remind(updater, context):
    db_tg.action2db(updater['message']['chat']['id'], updater['message']['chat']['username'], "remind")
    try:
        message_text = updater.message.text[7:]
        date = re.findall('(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](19\d\d|20\d\d)', message_text)[0]
        message_text = message_text.replace(".".join(date), '')
        if len(date) == 3:
            user_event_handler.events_list.append((date, message_text))
            schedule.every(5).seconds.do(user_event_handler.events_check, updater, context)
            updater.message.reply_text("Ok!")
        else:
            updater.message.reply_text("Invalid date.")
    except IndexError:
        updater.message.reply_text("Invalid event.")

# def echo(updater, context):
#     updater.message.reply_text(updater.message.text)


def main():
    db_tg.db_table_create()

    Config.read_opts()
    updater = Updater(token=Config.TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", command_help))
    dp.add_handler(CommandHandler("remind", command_remind))
    dp.add_handler(MessageHandler(Filters.text, university_schedule))
    # dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()

    schedule_thread = Thread(target=user_event_handler.user_schedule)
    schedule_thread.start()
    schedule_thread.join()
