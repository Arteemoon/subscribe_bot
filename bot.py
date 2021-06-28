import telebot
from telebot.apihelper import ApiTelegramException
from telebot import types
import time

bot = telebot.TeleBot("1711856004:AAHTlXZzeVdItH7Qt4mNhETqHgDOD4t0PzA")

CHAT_ID = -1001245023687

def is_subscribed(chat_id, user_id):
    try:
        bot.get_chat_member(chat_id, user_id)
        return True
    except ApiTelegramException as e:
        if e.result_json['description'] == 'Bad Request: user not found':
            return False

def process_uploaded_file(message):
    if message.document:
        with open('file_id.txt', 'w') as file:
            file.write(message.document.file_id)

@bot.message_handler(commands=['start'])
def start_message_handler(message):
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        url_button = types.InlineKeyboardButton(text="Ссылка", url="https://t.me/finansyok")
        check_button = types.InlineKeyboardButton(text="Проверить", callback_data="check_subscribe")
        keyboard.add(url_button, check_button)
        bot.send_message(message.chat.id, "Привет, чтобы получить бонус подпишись на канал и введи кодовое слово", reply_markup=keyboard)
    except:
        pass


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if not is_subscribed(CHAT_ID, call.from_user.id):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            url_button = types.InlineKeyboardButton(text="Ссылка", url="https://t.me/finansyok")
            check_button = types.InlineKeyboardButton(text="Проверить", callback_data="check_subscribe")
            keyboard.add(url_button, check_button)
            bot.send_message(call.from_user.id, 'Вы не подписаны, попробуй снова', reply_markup=keyboard)
        else:
            bot.send_message(call.from_user.id, 'Отлично теперь введи секретное слово')
    except:
        pass


@bot.message_handler(commands=['set_keyword'])
def handle_messages(message):
    args = message.text.split('set_keyword ')[-1]
    with open('word.txt', 'w') as file:
        file.write(args)

@bot.message_handler(commands=['upload_file'])
def handle_messages(message):
    try:
        bot.send_message(message.chat.id, 'Отправьте файл')
        bot.register_next_step_handler(message, process_uploaded_file)
    except:
        pass

@bot.message_handler()
def handle_messages(message):
    try:
        with open('word.txt', 'r') as file:
            if  is_subscribed(CHAT_ID, message.chat.id) and message.text == file.read():
                with open('file_id.txt') as file:
                    bot.send_document(message.chat.id, file.read())
            else:
                bot.send_message(message.chat.id, 'Попробуйте снова')
    except:
        pass

if __name__ == '__main__':
    try:
        bot.polling()
    except Exception as e:
        print(e)
        time.sleep(10)
