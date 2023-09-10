from config import TOKEN
import telebot
from utils import *
from MSSQL import *
import enum

bot = telebot.TeleBot(TOKEN)
db = MSSQL()

user_context_registration = {}
user_context_state = {}
user_context_confirm_delivery = {}

class StateDelivery(enum.Enum):
    """
    Класс для определения под-состояния и диалога, в состоянии оформаления заказа.

    Под-состояния бота:
    - Сonfirmation: начальное состояние подтверждения данных.
    - EditPhone: состояние изменения данных телефона.
    - EditAddress: состояние изменения данных адреса доставки.
    - Confirmed: состояние подтвержденых данных.
    
    """

    Сonfirmation = 1
    EditPhone = 2
    EditAddress = 3
    Confirmed = 4


class StateBot(enum.Enum):
    """
    Класс для определения состояния и диалога, в котором находится бот.

    Состояния бота:
    - Start: начальное состояние бота.
    - Registration: состояние, в котором происходит регистрация пользователя.
    - Profile: состояние, в котором пользователь может просмотреть и изменить свой профиль.
    ...
    - Admin: состояние администратора.
    """

    Start = 1
    Registration = 2
    Profile = 3
    PhonePriceSearch = 4
    Delivery = 5
    My_Orders = 6
    SupportChat = 7

    Admin = 9



