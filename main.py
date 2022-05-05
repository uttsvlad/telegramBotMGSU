import telebot
import urlworker
from telebot import types

TOKEN = "5118191064:AAGkLtD7YJkPMXV2uZaCp4M0txgEOO5KFQ8"

bot = telebot.TeleBot(TOKEN)

BOT_COMMANDS = ["Ближайший день открытых дверей", "", "Какая учебная неделя идет?", "",
                "Статья об архитектуре"]
BOT_BUTTONS = []
for command in BOT_COMMANDS:
    BOT_BUTTONS.append(types.KeyboardButton(command))

mgsu_parser = urlworker.ParserFactory.create_mgsu_parser()
articles_parser = urlworker.ParserFactory.create_articles_parser()


@bot.message_handler(commands=['start', 'help'])
def process_start_command(msg: types.Message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for button in BOT_BUTTONS:
        markup.add(button)
    bot.send_message(msg.from_user.id, "Выберите нужную кнопку:", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def message_reply(message):
    if message.text == BOT_COMMANDS[0]:
        result_list = mgsu_parser.get_opened_doors_day()
        text = ""
        for data in result_list:
            text += data + "\n\n"
        bot.send_message(message.chat.id, text)

    elif message.text == BOT_COMMANDS[1]:
        bot.send_message(message.chat.id, "2")

    elif message.text == BOT_COMMANDS[2]:
        text = mgsu_parser.set_week()
        bot.send_message(message.chat.id, text)

    elif message.text == BOT_COMMANDS[3]:
        bot.send_message(message.chat.id, "4")

    elif message.text == BOT_COMMANDS[4]:
        text = articles_parser.get_random_article()
        bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)