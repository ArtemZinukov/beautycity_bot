from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup
from environs import Env
import os
import re
import datetime
from .models import Master, Client, Service, Salon, Registration

env = Env()
env.read_env()
token = env.str("TG_BOT_TOKEN")
bot = TeleBot(token)

previous_messages = {}
users_info = {}


def send_file(message, file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, 'rb') as file:
        bot.send_document(message.chat.id, file)


def request_user_credentials(message):
    if message.text == 'Вернуться на главную':
        handle_consent(message)
    else:
        chat_id = message.chat.id
        users_info[chat_id]['master'] = message.text
        client, created = Client.objects.get_or_create(tg_id=message.from_user.id)
        client.username = message.from_user.first_name
        client.save()
        if 'master' in users_info[message.chat.id]:
            registration = Registration(
                client=client,
                service=Service.objects.get(title=users_info[message.chat.id]['service']),
                salon=Salon.objects.get(address=users_info[message.chat.id]['salon']),
                service_date=users_info[message.chat.id]['service_date'],
                master=Master.objects.get(name=users_info[message.chat.id]['master']),
                slot=users_info[message.chat.id]['slot']
            )
            registration.save()
        ask_phone(message)


def request_user_credentials_2(message):
    if message.text == 'Вернуться на главную':
        handle_consent(message)
    else:
        chat_id = message.chat.id
        users_info[chat_id]['salon'] = message.text
        client, created = Client.objects.get_or_create(tg_id=message.from_user.id)
        client.username = message.from_user.first_name
        client.save()
        if 'master' in users_info[message.chat.id]:
            registration = Registration(
                client=client,
                service=Service.objects.get(title=users_info[message.chat.id]['service']),
                salon=Salon.objects.get(address=users_info[message.chat.id]['salon']),
                service_date=users_info[message.chat.id]['service_date'],
                master=Master.objects.get(name=users_info[message.chat.id]['master']),
                slot=users_info[message.chat.id]['slot']
            )
            registration.save()
        ask_phone(message)


def ask_phone(message):
    if message.text == 'Вернуться на главную':
        handle_consent(message)
    else:
        bot.send_message(message.chat.id, 'Введите ваш номер телефона: (Например: +78521503215)')
        bot.register_next_step_handler(message, handle_phone)


def handle_phone(message):
    if message.text == 'Вернуться на главную':
        handle_consent(message)
    else:
        phone_pattern = r'^(\+7)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
        if re.match(phone_pattern, message.text):
            client = Client.objects.last()
            client.phone_number = message.text
            client.save()
            bot.send_message(message.chat.id, 'Ваш заказ успешно зарегистрирован!')
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


# Первая ветка ################################################################################
@bot.message_handler(func=lambda message: message.text == 'Выбрать салон')
def running_script_salon(message):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        chat_id = message.chat.id
        users_info[chat_id] = {}

        for salon in Salon.objects.all():
            markup.row(salon.address)
        markup.row("Вернуться на главную")
        message_text = "Выберите салон:"
        bot.send_message(message.chat.id, message_text, reply_markup=markup)
        bot.register_next_step_handler(message, running_script_service_after_salon)


@bot.message_handler(func=lambda message: message.text in [salon.address for salon in Salon.objects.all()])
def running_script_service_after_salon(message):
    if message.text == 'Вернуться на главную':
        handle_consent(message)
    else:
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
        bot.register_next_step_handler(message, running_script_date_after_service)


@bot.message_handler(func=lambda message: message.text in [service.title for service in Service.objects.all()])
def running_script_date_after_service(message):
    if message.text == 'Вернуться на главную':
        handle_consent(message)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        today = datetime.date.today()
        markup_output = []
        for day in range(1, 7):
            date = str(today + datetime.timedelta(days=day))
            markup_output.append(date)
        markup.max_row_keys = 3
        markup.row(*markup_output)
        markup.row("Вернуться на главную")
        message_text = "Выберите дату:"
        chat_id = message.chat.id
        users_info[chat_id]['service'] = message.text
        bot.send_message(message.chat.id, message_text, reply_markup=markup)
        bot.register_next_step_handler(message, running_script_time_after_date)


@bot.message_handler(
    func=lambda message: message.text in [datetime.date.today() + datetime.timedelta(days=day) for day in range(1, 7)])
def running_script_time_after_date(message):
    if message.text == 'Вернуться на главную':
        handle_consent(message)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        chat_id = message.chat.id
        users_info[chat_id]['service_date'] = datetime.datetime.strptime(message.text, '%Y-%m-%d')

        masters = Master.objects.filter(services__title=users_info[chat_id]['service'],
                                        salons__address=users_info[chat_id]['salon'])
        markup_output = []

        for master in masters:
            slots = ['10:00-11:00', '11:00-12:00', '12:00-13:00', '13:00-14:00', '14-00-15:00', '15:00-16:00']
            records = Registration.objects.filter(master__name=master.name,
                                                  salon__address=users_info[chat_id]['salon'],
                                                  service_date=message.text)

            users_info[chat_id][master.name] = slots

            for record in records:
                users_info[chat_id][master.name].remove(record.slot)

            for slot in users_info[chat_id][master.name]:
                if slot not in markup_output:
                    markup_output.append(slot)

        markup_output.sort()
        markup.max_row_keys = 3
        markup.row(*markup_output)
        markup.row("Вернуться на главную")
        message_text = "Выберите время:"
        bot.send_message(message.chat.id, message_text, reply_markup=markup)
        bot.register_next_step_handler(message, running_script_master_after_time)


def running_script_master_after_time(message):
    if message.text == 'Вернуться на главную':
        handle_consent(message)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        chat_id = message.chat.id
        users_info[chat_id]['slot'] = message.text

        masters = Master.objects.filter(services__title=users_info[chat_id]['service'],
                                        salons__address=users_info[chat_id]['salon'])
        markup_output = []

        for master in masters:
            if master.name in users_info[chat_id]:
                if message.text in users_info[chat_id][master.name]:
                    markup_output.append(master.name)

        markup.max_row_keys = 3
        markup.row(*markup_output)
        markup.row("Вернуться на главную")
        message_text = "Выберите Мастера:"
        bot.send_message(message.chat.id, message_text, reply_markup=markup)
        bot.register_next_step_handler(message, request_user_credentials)


# Вторая ветка #################################################################################
@bot.message_handler(func=lambda message: message.text == 'Выбрать мастера')
def running_script_master(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    chat_id = message.chat.id
    users_info[chat_id] = {}

    output = []

    for master in Master.objects.all():
        output.append(master.name)

    markup.max_row_keys = 3
    markup.row(*output)
    markup.row('Вернуться на главную')
    message_text = 'Выберите мастера'
    bot.send_message(message.chat.id, message_text, reply_markup=markup)
    bot.register_next_step_handler(message, running_script_service_after_master)


@bot.message_handler(func=lambda message: message.text in [master.name for master in Master.objects.all()])
def running_script_service_after_master(message):
    try:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        chat_id = message.chat.id
        users_info[chat_id]['master'] = message.text

        master = Master.objects.get(name=message.text)

        services = master.services.all()

        output = []

        for service in services:
            output.append(service.title)

        markup.max_row_keys = 3
        markup.row(*output)
        markup.row("Вернуться на главную")
        message_text = "Выберите услугу:\n"
        for service in services:
            message_text += f"{service.title} - {service.price} рублей\n"
        bot.send_message(message.chat.id, message_text, reply_markup=markup)
        bot.register_next_step_handler(message, running_script_date_after_service_2)

    except Master.DoesNotExist:
        handle_consent(message)


@bot.message_handler(func=lambda message: message.text in [service.title for service in Service.objects.all()])
def running_script_date_after_service_2(message):
    if message.text == 'Вернуться на главную':
        handle_consent(message)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        today = datetime.date.today()
        markup_output = []
        for day in range(1, 7):
            date = str(today + datetime.timedelta(days=day))
            markup_output.append(date)
        markup.max_row_keys = 3
        markup.row(*markup_output)
        markup.row("Вернуться на главную")
        message_text = "Выберите дату:"
        chat_id = message.chat.id
        users_info[chat_id]['service'] = message.text
        bot.send_message(message.chat.id, message_text, reply_markup=markup)
        bot.register_next_step_handler(message, running_script_time_after_date_2)


@bot.message_handler(
    func=lambda message: message.text in [datetime.date.today() + datetime.timedelta(days=day) for day in range(1, 7)])
def running_script_time_after_date_2(message):
    if message.text == 'Вернуться на главную':
        handle_consent(message)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        chat_id = message.chat.id
        users_info[chat_id]['service_date'] = datetime.datetime.strptime(message.text, '%Y-%m-%d')

        master = Master.objects.filter(name=users_info[chat_id]['master'],
                                       services__title=users_info[chat_id]['service'],)
        markup_output = []

        slots = ['10:00-11:00', '11:00-12:00', '12:00-13:00', '13:00-14:00', '14-00-15:00', '15:00-16:00']
        records = Registration.objects.filter(master__name=master[0].name,
                                              service_date=message.text)

        users_info[chat_id][master[0].name] = slots

        for record in records:
            users_info[chat_id][master[0].name].remove(record.slot)

        for slot in users_info[chat_id][master[0].name]:
            if slot not in markup_output:
                markup_output.append(slot)

        markup_output.sort()
        markup.max_row_keys = 3
        markup.row(*markup_output)
        markup.row("Вернуться на главную")
        message_text = "Выберите время:"
        bot.send_message(message.chat.id, message_text, reply_markup=markup)
        bot.register_next_step_handler(message, running_script_salon_after_time)


def running_script_salon_after_time(message):
    if message.text == 'Вернуться на главную':
        handle_consent(message)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        chat_id = message.chat.id
        users_info[chat_id]['slot'] = message.text

        master = Master.objects.get(name=users_info[chat_id]['master'])
        salons = master.salons.all()

        output = []
        for salon in salons:
            markup.row(salon.address)
        markup.max_row_keys = 3
        markup.row(*output)
        markup.row("Вернуться на главную")
        message_text = "Выберите салон:"
        bot.send_message(message.chat.id, message_text, reply_markup=markup)
        bot.register_next_step_handler(message, request_user_credentials_2)


# Прочее
@bot.message_handler(func=lambda message: message.text == 'Вернуться на главную')
def send_back(message):
    handle_consent(message)


@bot.message_handler(func=lambda message: message.text == 'Назад')
def back_to_previous_message(message):
    previous_message = previous_messages.get(message.chat.id)
    if previous_message == "Выбрать мастера":
        handle_contact_admin(message)


def main():
    bot.infinity_polling()


if __name__ == "__main__":
    main()
