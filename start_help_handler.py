from bot_data import *
from authorization import login


# START HELP
# Enum State Bot: Start = 1
def start_help_handler(message):
    chat_id = message.chat.id
    bot.reply_to(message, "Привет, я бот Moremonta!")

    user_context_state[chat_id] = StateBot.Start
    if chat_id in user_context_registration:
        del user_context_registration[chat_id]

    if login(message):
        print("#Authorized", chat_id)
