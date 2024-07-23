from telebot import TeleBot
from telebot import types
from telebot.types import ReplyKeyboardMarkup
from environs import Env


env = Env()
env.read_env()
token = env.str("TG_BOT_TOKEN")
bot = TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Привет")
    start_message = '''
Привет!
Какой-то текст!

'''
    bot.send_message(message.chat.id, start_message, reply_markup=markup)

def choose_salon(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Салон_1', 'Салон_2', 'Салон_3')
    bot.send_message(message.chat.id, 'Выберите салон:', reply_markup=markup)


def main():
    bot.infinity_polling()




if __name__ == "__main__":
    main()
