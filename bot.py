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
    keyboard.row('Add place', 'Show my list')
    if message.text == '/start':
        bot.send_message(message.chat.id, const.start_command, reply_markup=keyboard, parse_mode='markdown')

        us_id = message.from_user.id
        username = message.from_user.username

        dbHandler.db_table_val(us_id, username)
    elif message.text == '/help':
        bot.send_message(message.chat.id, 'How can i help u?', reply_markup=keyboard)


@bot.message_handler(commands=['add', 'list'])
def handle_add_list(message):
    if message.text == '/add':
        bot.send_message(message.chat.id, 'Add place', parse_mode='markdown')
    elif message.text == '/list':
        bot.send_message(message.chat.id, 'My places', parse_mode='markdown')


@bot.message_handler(content_types='text')
def handle_buttons(message):
    if message.text == 'Add place':
        bot.send_message(message.chat.id, 'Add place', parse_mode='markdown')
    elif message.text == 'Show my list':
        bot.send_message(message.chat.id, 'My places', parse_mode='markdown')


bot.infinity_polling()
