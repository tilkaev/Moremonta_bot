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
    Start = 1
    Registration = 2
    Profile = 3

    Admin = 9
