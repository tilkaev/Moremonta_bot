from utils import *
from bot_data import *

from start_help_handler import start_help_handler
from show_profile_handler import show_profile_handler
from registration_handler_state import registration_handler_state
from callback_handler import callback_handler
from echo_all_handler import echo_all_handler
from find_phone_price_handler import find_phone_price_handler
from support_chat_handler import support_chat_handler
from delivery_handler import delivery_handler


def check_user_state(message, state):
    return (
        message.chat.id in user_context_state
        and user_context_state[message.chat.id] == state
    )


# Enum State Bot: Start = 1
# Обработчик команд /start и /help
bot.message_handler(commands=["start", "help"]
)(start_help_handler)


# Enum State Bot: Registration = 2
# Обработчик сообщений в состоянии регистрации
bot.message_handler(
    func=lambda message: check_user_state(message, StateBot.Registration)
)(registration_handler_state)

# Enum State Bot: Profile = 3
# Обработчик команды /profile
bot.message_handler(commands=["profile"]
)(show_profile_handler)

# Enum State Bot: PhonePriceSearch = 4
# Обработчик сообщений
bot.message_handler(
    func=lambda message: check_user_state(message, StateBot.PhonePriceSearch)
)(find_phone_price_handler)

# Enum State Bot: Delivery = 5
# Обработчик сообщений
bot.message_handler(
    func=lambda message: check_user_state(message, StateBot.Delivery)
)(delivery_handler)

# Enum State Bot: SupportChat = 6
# Обработчик сообщений
bot.message_handler(
    func=lambda message: check_user_state(message, StateBot.SupportChat)
)(support_chat_handler)


# Обработчик callback-запросов (для других целей)
bot.callback_query_handler(func=lambda call: True
)(callback_handler)

# Эхо-обработчик для всех остальных сообщений
bot.message_handler(func=lambda message: True
)(echo_all_handler)


if __name__ == "__main__":
    bot.polling(none_stop=True)
