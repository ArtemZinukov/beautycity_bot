from datetime import datetime, timedelta, date

import schedule
import time
from telebot import TeleBot

from environs import Env

from core.apps.bot.models import Registration


env = Env()
env.read_env()
token = env.str("TG_BOT_TOKEN")
bot = TeleBot(token)


def send_reminder(booking):
    client = booking.client
    reminder_message = "Вы так давно не были у нас, пора бы записаться!"
    bot.send_message(client.tg_id, reminder_message)


def check_bookings():
    bookings = Registration.objects.all()
    for booking in bookings:
        booking_time = booking.time_registration
        current_time = datetime.now()
        if current_time == datetime.combine(date.today(), booking_time.time()) + timedelta(minutes=10):
            if not booking.reminder_sent:
                send_reminder(booking)
                booking.reminder_sent = True
                booking.save()


schedule.every(1).minutes.do(check_bookings)


def main():
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(f"Error sending reminder: {e}")


if __name__ == "__main__":
    main()
