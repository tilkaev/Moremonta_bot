from bot_data import *
from authorization import login
from models import *
from data_operations import get_device_by_id, get_price_by_device_id




def search_device_by_name(name_phone) -> list:

    query = "select * from Devices where Devices.name like ?"
    params = f"%{str(name_phone).replace(' ', '%')}%"
    result_devices = db.execute_query(query, params)

    phones = []
    for i in result_devices:
        device = Device()
        device.id = i[0]
        device.name = i[1]
        phones.append(device)

    print("#", name_phone, result_devices)
    return phones


def send_price_by_device_id(message, device_id):

    services = get_price_by_device_id(device_id)
    device = get_device_by_id(device_id)
    print(services)

    text_out = ""
    for service in services:
        text_out += f"\n✅ {service._service_name}: {service.price}₽"

    keyboard = types.InlineKeyboardMarkup()
    delivery_button = types.InlineKeyboardButton(text=f"Заказать доставку 🛴", callback_data=f"[DELIVERY][device_id]{device.id}")
    callback_button = types.InlineKeyboardButton(text=f"ОТМЕНА", callback_data="[BACK]")
    keyboard.add(delivery_button)
    keyboard.add(callback_button)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=f"⚒️ {device.name} ⚒️\n{text_out}", reply_markup=keyboard) 
    """
    result = f"⚒️ {result_devices_converted[0]} ⚒️\n\n✅ Замена стекла (с гарантией): {result_devices[0][1]}\n✅ Разборка/сборка устройства: 700"
    bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=result, reply_markup=keyboard)"""


def find_phone_price_handler(message):
    chat_id = message.chat.id

    if login(message) == False:
       return


    if len(message.text) >50:
        bot.reply_to(message, f"Напишите пожалуйста название или модель корректно!")
        return

    """
    query_profile = "select Mprice.name, Mprice.price from Brands Br, MasterPrice Mprice where Br.id = Mprice.brand_id and Mprice.name like ?"
    params = f"%{str(message.text).replace(' ', '%')}%"
    result_devices = db.execute_query(query_profile, params)

    result_devices_converted = [i[0] for i in result_devices]
    print("#", message.text, result_devices_converted)"""


    result_devices = search_device_by_name(message.text)

    if len(result_devices) > 10:
        bot.reply_to(message, f"{message.text} - не могу найти телефон в базе!")

    elif len(result_devices) > 1:
        #result =  difflib_searcher(message.text, query_devices)
        #bot.reply_to(message, "{0}\n - выберите из этого списка!".format( "\n".join(query_devices) ))

        keyboard = types.InlineKeyboardMarkup()
        for device in result_devices:
            callback_button = types.InlineKeyboardButton(text=f"{device.name}", callback_data=f"[DEVICE_ID]{device.id}")
            keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text=f"ОТМЕНА", callback_data="[BACK]")
        keyboard.add(callback_button)

        bot.send_message(message.chat.id, "Выберите подоходящий телефон:", reply_markup=keyboard)
                
    elif len(result_devices) == 1:
        send_price_by_device_id(message, result_devices[0][0])


    else:
        bot.reply_to(message, f"{message.text} - такого телефона нету в базе!")
        

        
    '''
    # First finding brand
    query_brands = db.select("select name, id from Brands")
    print(query_brands)
    temp = [i[0] for i in query_brands]
    result =  difflib_searcher(message.text.split()[0], temp)
    
    if result is None:
        bot.reply_to(message, f"{message.text} - не могу найти телефон в базе!")
        return
    
    index = 0
    for i, item in enumerate(query_brands):
        if item[0] == result:
            index = item[1]
            break
    
    # Second finding device
    #query_devices = db.select(f"select name from Devices where brand_id = {index}")
    query_devices = db.select("select Ds.name from Brands Br, Devices Ds where brand_id = {0} and  Br.id = Ds.brand_id and Ds.name like '%{1}%'".format(index, message.text.replace(" ", "%")))
    query_devices = [i[0] for i in query_devices]
    print(query_devices) 
    result =  difflib_searcher(message.text, query_devices)
    
    if result is None:
        bot.reply_to(message, f"{message.text} - не могу найти телефон в базе!")
        return

    bot.reply_to(message, "{0} - такой телефона есть в базе!".format(result[0]))'''

    '''
    query = "select Ds.name from Brands Br, Devices Ds where Br.id = Ds.brand_id and Ds.name like '%{0}%'".format(str(message.text).replace(" ", "%"))
    result = db.select(query)
    
    if result != [] and len(result)<=10:
        bot.reply_to(message, "{0} - такой телефона есть в базе!".format(result[0]))
    else:
        bot.reply_to(message, "{0} - такого телефона нет в базе!".format(message.text))'''