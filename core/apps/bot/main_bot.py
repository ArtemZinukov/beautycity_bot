from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup
from environs import Env
import os
import re
import datetime
from .models import Master, Client, Service, Salon

slots = ['10:00-11:00',
         '11:00-12:00',
         '12:00-13:00',
         '13:00-14:00',
         '14-00-15:00',
         '15:00-16:00',
         '16:00-17:00',
         '17:00-18:00']

users_info = {}


env = Env()
env.read_env()
token = env.str("TG_BOT_TOKEN")
bot = TeleBot(token)

previous_messages = {}


def send_file(message, file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, 'rb') as file:
        bot.send_document(message.chat.id, file)


def request_user_credentials(message):
    ask_phone(message)
    client, created = Client.objects.get_or_create(tg_id=message.from_user.id)
    client.username = message.from_user.first_name
    client.save()


def ask_phone(message):
    bot.send_message(message.chat.id, 'Введите ваш номер телефона: (Например: +78521503215)')
    bot.register_next_step_handler(message, handle_phone)


def handle_phone(message):
    phone_pattern = r'^(\+7)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
    if re.match(phone_pattern, message.text):
        client = Client.objects.last()
        client.phone_number = message.text
        client.save()
    else:
        bot.send_message(message.chat.id, 'Некорректный формат номера телефона. Пожалуйста, введите снова:')
        bot.register_next_step_handler(message, handle_phone)


@bot.message_handler(commands=['start'])
def get_personal_data_consent(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Согласен')
    message_text = '''
Приветствуем вас в Beautycity - лучшем салоне красоты!
Пожалуйста, ознакомьтесь с файлом и подтвердите свое согласие. 
'''
    send_file(message, 'pd_consent.pdf')
    bot.send_message(message.chat.id, message_text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Согласен')
def handle_consent(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Выбрать салон')
    markup.row('Выбрать мастера')
    markup.row('Связь с салоном')
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Связь с салоном')
def handle_contact_admin(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Вернуться на главную')
    message_text = 'Телефон администратора для связи: +79999999999'
    bot.send_message(message.chat.id, message_text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Выбрать мастера')
def handle_contact_admin(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    masters = Master.objects.all()

    output = []

    for master in masters:
        output.append(master.name)

    markup.max_row_keys = 3
    markup.row(*output)

    markup.row('Вернуться на главную')
    message_text = 'Выберите мастера'
    bot.send_message(message.chat.id, message_text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in [master.name for master in Master.objects.all()])
def choose_service(message):
    master_name = message.text
    master = Master.objects.get(name=master_name)
    services = master.services.all()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    message_text = "Выберите услугу:\n"
    markup_output = []
    for service in services:
        message_text += f"{service.title} - {service.price} рублей\n"
        markup_output.append(service.title)
    markup.max_row_keys = 2
    markup.row(*markup_output)
    markup.row('Назад', 'Вернуться на главную')
    previous_messages[message.chat.id] = 'Выбрать мастера'
    bot.send_message(message.chat.id, message_text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in [service.title for service in Service.objects.all()])
def get_user_data(message):
    request_user_credentials(message)


@bot.message_handler(func=lambda message: message.text == 'Вернуться на главную')
def send_back(message):
    handle_consent(message)


@bot.message_handler(func=lambda message: message.text == 'Назад')
def back_to_previous_message(message):
    previous_message = previous_messages.get(message.chat.id)
    if previous_message == "Выбрать мастера":
        handle_contact_admin(message)


@bot.message_handler(func=lambda message: message.text == 'Выбрать салон')
def choose_salon(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    chat_id = message.chat.id
    users_info[chat_id] = {}

    for salon in Salon.objects.all():
        markup.row(salon.address)
    markup.row("Вернуться на главную")
    message_text = "Выберите салон:"
    bot.send_message(message.chat.id, message_text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in [salon.address for salon in Salon.objects.all()])
def choose_procedure(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    services = Service.objects.all()
    for service in services:
        markup.row(service.title)
    markup.row("Вернуться на главную")
    message_text = "Выберите услугу:\n"
    for service in services:
        message_text += f"{service.title} - {service.price} рублей\n"
    chat_id = message.chat.id
    users_info[chat_id]['salon'] = message.text
    bot.send_message(message.chat.id, message_text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in [service.title for service in Service.objects.all()])
def choose_date(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    today = datetime.date.today()
    markup_output = []
    for day in range(1, 8):
        date = today + datetime.timedelta(days=day)
        markup_output.append(date)
    markup.max_row_keys = 3
    markup.row(*markup_output)
    markup.row("Назад","Вернуться на главную")
    message_text = "Выберите дату:"
    chat_id = message.chat.id
    users_info[chat_id]['service'] = message.text
    bot.send_message(message.chat.id, message_text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in [datetime.date.today() + datetime.timedelta(days=day) for day in range(1, 8)])
def choose_slot(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    chat_id = message.chat.id
    users_info[chat_id]['slots'] = []
    users_info[chat_id]['slots'] = slots

    masters = Master.objects.filter(services__title=users_info[chat_id]['service'], salons__address=users_info[chat_id]['salon'])


def main():

    bot.infinity_polling()



if __name__ == "__main__":
    main()