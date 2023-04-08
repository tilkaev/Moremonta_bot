from config import TOKEN
import telebot
from utils import *
from MSSQL import *
import enum

bot = telebot.TeleBot(TOKEN)
db = MSSQL()

user_context_registration = {}
user_context_state = {}


class StateBot(enum.Enum):
    """
    Класс для определения состояния и диалога, в котором находится бот.

    Состояния бота:
    - Start: начальное состояние бота.
    - Registration: состояние, в котором происходит регистрация пользователя.
    - Profile: состояние, в котором пользователь может просмотреть и изменить свой профиль.
    - Admin: состояние администратора.
    """

    Start = 1
    Registration = 2
    Profile = 3
    PhonePriceSearch = 4
    SupportChat = 5

    Admin = 9


class State(enum.Enum):
    Start = 1
    Registration = 2
    Profile = 3

    Admin = 9
