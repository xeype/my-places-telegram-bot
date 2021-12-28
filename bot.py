import telebot
import configparser
import const
from utils import dbHandler

config = configparser.ConfigParser()
config.read("config.ini")
token = config['Telegram']['TOKEN']

bot = telebot.TeleBot(token)

keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row(const.ADD_PLACE, const.SHOW_LIST)


class Place:
    name = ''
    rating = 5
    desc = ''

    def add_place_name(self, name):
        self.name = name

    def add_place_rating(self, rating):
        self.rating = rating

    def add_place_desc(self, desc):
        self.desc = desc

    def get_place_name(self):
        return self.name

    def get_rating(self):
        return self.rating

    def get_place_desc(self):
        return self.desc


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, const.START_OUTPUT, reply_markup=keyboard, parse_mode='markdown')

    us_id = message.from_user.id
    username = message.from_user.username
    dbHandler.db_table_val(us_id, username)


@bot.message_handler(commands=['help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, const.HELP_OUTPUT, reply_markup=keyboard, parse_mode='markdown')


@bot.message_handler(commands=['add'])
def handle_add(message):
    sent = bot.send_message(message.chat.id, 'Enter name of the place')
    bot.register_next_step_handler(sent, add_place_name_request)


@bot.message_handler(commands=['list'])
def handle_list(message):
    bot.send_message(message.chat.id, 'My places', parse_mode='markdown')


@bot.message_handler(commands=[''])
def handler_unknown(message):
    bot.send_message(message.chat.id, const.UNKNOWN_OUTPUT, parse_mode='markdown')


@bot.message_handler(content_types=['text'])
def handle_buttons(message):
    if message.text == const.ADD_PLACE:
        handle_add(message)
    elif message.text == const.SHOW_LIST:
        bot.send_message(message.chat.id, 'List', parse_mode='markdown')
    else:
        handler_unknown(message)


def add_place_name_request(message):
    new_place = Place()
    new_place.add_place_name(message.text)
    sent = bot.send_message(message.chat.id, 'Please enter rating (1-5)', parse_mode='markdown')
    bot.register_next_step_handler(sent, add_place_rating_request, new_place)


def add_place_rating_request(message, new_place):
    if message.text.isnumeric():
        new_place.add_place_rating(int(message.text))

    sent = bot.send_message(message.chat.id, 'Please enter description')
    bot.register_next_step_handler(sent, add_place_description_request, new_place)


def add_place_description_request(message, new_place):
    new_place.add_place_desc(message.text)
    dbHandler.add_place(message.from_user.id, new_place.get_place_name(), new_place.get_rating(),
                        new_place.get_place_desc())
    bot.send_message(message.chat.id, 'Place was added')


bot.infinity_polling()
