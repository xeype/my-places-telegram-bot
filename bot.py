import telebot
import configparser
import const
from utils import dbHandler

config = configparser.ConfigParser()
config.read("config.ini")
token = config['Telegram']['TOKEN']

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row(const.ADD_PLACE, const.SHOW_LIST)
    if message.text == const.START_COMMAND:
        bot.send_message(message.chat.id, const.START_OUTPUT, reply_markup=keyboard, parse_mode='markdown')

        us_id = message.from_user.id
        username = message.from_user.username

        dbHandler.db_table_val(us_id, username)
    elif message.text == const.HELP_COMMAND:
        bot.send_message(message.chat.id, const.HELP_OUTPUT, reply_markup=keyboard, parse_mode='markdown')


@bot.message_handler(commands=['add', 'list'])
def handle_add_list(message):
    if message.text == const.ADD_COMMAND:
        sent = bot.send_message(message.chat.id, 'Enter name of the place')
        bot.register_next_step_handler(sent, add_place_request)
    elif message.text == const.LIST_COMMAND:
        bot.send_message(message.chat.id, 'My places', parse_mode='markdown')
    else:
        bot.send_message(message.chat.id, const.UNKNOWN_OUTPUT, parse_mode='markdown')


@bot.message_handler(content_types=['text'])
def handle_button(message):
    if message.text == const.ADD_PLACE:
        sent = bot.send_message(message.chat.id, 'Enter name of the place')
        bot.register_next_step_handler(sent, add_place_request)
    elif message.text == const.SHOW_LIST:
        bot.send_message(message.chat.id, 'List', parse_mode='markdown')
    else:
        bot.send_message(message.chat.id, const.UNKNOWN_OUTPUT, parse_mode='markdown')


def add_place_request(message):
    bot.send_message(message.chat.id, message.text)
    bot.send_message(message.chat.id, 'Thank you!')


bot.infinity_polling()
