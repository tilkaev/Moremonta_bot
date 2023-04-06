
import difflib


def difflib_searcher(text, possible_values):
    #possible_values = ['ms sql', 'python']

    # Используем модуль difflib для поиска ближайшего совпадения
    closest_match = difflib.get_close_matches(text, possible_values, n=1, cutoff=0.4)

    print(closest_match)
    
    if closest_match:
        return closest_match[0]
        #bot.send_message(chat_id=message.chat.id, text=f"Did you mean {closest_match[0]}?")
    else:
        return None
        #bot.send_message(chat_id=message.chat.id, text="Sorry, I didn't understand your message.")


