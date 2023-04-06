from bot_data import *
from authorization import login


# START HELP
#@bot.message_handler(commands=['start', 'help'])
def start_help_handler(message):
    #user_id = message.chat.id
    bot.reply_to(message, "Привет, я бот Moremonta!")

    user_context_state[message.chat.id] = StateBot.Start
    if message.chat.id in user_context_registration:
        del user_context_registration[message.chat.id]

    if login(message):
       print("#Authorized")
