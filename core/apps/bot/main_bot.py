from telebot import TeleBot
from telebot import types
from telebot.types import ReplyKeyboardMarkup
from environs import Env
import os


env = Env()
env.read_env()
token = env.str("TG_BOT_TOKEN")
bot = TeleBot(token)

previous_messages = {}


def send_file(message, file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, 'rb') as file:
        bot.send_document(message.chat.id, file)


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
    previous_messages[message.chat.id] = "Выберите действие:"


@bot.message_handler(func=lambda message: message.text == 'Связь с салоном')
def handle_contact_admin(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Вернуться на главную')
    message_text = 'Телефон администратора для связи: 79999999999'
    bot.send_message(message.chat.id, message_text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Вернуться на главную')
def send_back(message):
    handle_consent(message)


# @bot.message_handler(func=lambda message: message.text == 'Назад')
# def back_to_previous_message(message):
#     previous_message = previous_messages.get(message.chat.id)
#     if previous_message == "Правила пользования":
#         handle_rules_message(message)

def choose_salon(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Салон_1', 'Салон_2', 'Салон_3')
    bot.send_message(message.chat.id, 'Выберите салон:', reply_markup=markup)


def main():
    bot.infinity_polling()




if __name__ == "__main__":
    main()
