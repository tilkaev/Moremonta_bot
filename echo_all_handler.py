from bot_data import *


# ALL MESSAGE
#@bot.message_handler(func=lambda message: True)
def echo_all_handler(message):

    query_profile = "select Ds.name from Brands Br, Devices Ds where Br.id = Ds.brand_id and Ds.name like ?"
    params = f"%{str(message.text).replace(' ', '%')}%"
    result_devices = db.execute_query(query_profile, params)

    result_devices = [i[0] for i in result_devices]
    print("#", result_devices)

    if len(result_devices) > 10:
        bot.reply_to(message, f"{message.text} - не могу найти телефон в базе!")

    elif len(result_devices) > 1:
        #result =  difflib_searcher(message.text, query_devices)
        #bot.reply_to(message, "{0}\n - выберите из этого списка!".format( "\n".join(query_devices) ))

        keyboard = types.InlineKeyboardMarkup()
        for device in result_devices:
            callback_button = types.InlineKeyboardButton(text=f"{device}", callback_data=f"[DEVICE]{device}")
            keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text=f"ОТМЕНА", callback_data="[BACK]")
        keyboard.add(callback_button)

        sent_message = bot.send_message(message.chat.id, "Выберите подоходящий телефон:", reply_markup=keyboard)
                
    elif len(result_devices) == 1:
        bot.reply_to(message, "{0} - этот телефон есть в базе!".format(result_devices[0]))

    else:
        bot.reply_to(message, "{0} - такого телефона нету в базе!".format(message.text))
        

        
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
