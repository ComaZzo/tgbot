import schedule
import datetime
import time

from . import db_tg

events_list = []


def user_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)


def events_check(updater, context):
    for event in events_list:
        delta = datetime.datetime(int(event[0][2]), int(event[0][1]), int(event[0][0])) - datetime.datetime.now()
        if delta.days < 0:
            user_event(updater, context, event[1])
            events_list.remove(event)


def user_event(updater, context, event_text):
    context.bot.send_message(updater['message']['chat']['id'], f"You have an event: {event_text}")
    db_tg.action2db(updater['message']['chat']['id'], updater['message']['chat']['username'], "done remind")
    return schedule.CancelJob
