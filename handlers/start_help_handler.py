from bot_data import *
from authorization import login

TEXT_HELLO = '''Привет! ʕ ᵔᴥᵔ ʔ 
Я - бот Moremonta 🧑‍🔧🌊

Я могу помочь тебе с ремонтом 🔧 твоего телефона 📱

Вот что я умею:

- Узнать примерную стоимость 💰 услуги 🔧 по переклейке экрана телефона 📱
(PS. Просто отправь мне модель своего телефона и я скажу тебе примерную стоимость 💲)

- Организовать доставку 🛴 телефона 📱 от Вас до мастера и обратно.

- Следить за статусом ✅ выполнения ремонта 🧑‍🔧

В разработке: оплата 💳 услуг через бота.
'''


# START HELP
# Enum State Bot: Start = 1
def start_help_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, TEXT_HELLO)

    user_context_state[chat_id] = StateBot.PhonePriceSearch
    if chat_id in user_context_registration:
        del user_context_registration[chat_id]

    if login(message):
        print("#Authorized", chat_id)


