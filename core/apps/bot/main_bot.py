from telebot import TeleBot
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


def main():
    bot.infinity_polling()


if __name__ == "__main__":
    main()
