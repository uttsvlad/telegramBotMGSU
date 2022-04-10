from cgitb import text
import telebot
from telebot import types
import urlworker
from architecture_articles_parser import get_random_article_from_architect4u
token = "5118191064:AAGkLtD7YJkPMXV2uZaCp4M0txgEOO5KFQ8"
bot = telebot.TeleBot(token)
p = urlworker.Parser("https://mgsu.ru/student/Raspisanie_zanyatii_i_ekzamenov/fayly-raspisaniya-dlya-skachivaniya/")

BOT_COMMANDS = ["Расписание на сегодня", "Расписание на завтра", "Какая сейчас неделя?", "Какая сейчас пара по счету?",
                "Статья об архитектуре"]
BOT_BUTTONS = []
for command in BOT_COMMANDS:
    BOT_BUTTONS.append(types.KeyboardButton(command))

@bot.message_handler(commands=["start"])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for button in BOT_BUTTONS:
        markup.add(button)
    bot.send_message(message.chat.id, "Выберите нужную кнопку:", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def message_reply(message):
    if (message.text == BOT_COMMANDS[0]):
        bot.send_message(message.chat.id, "1")

    elif (message.text == BOT_COMMANDS[1]):
        bot.send_message(message.chat.id, "2")

    elif (message.text == BOT_COMMANDS[2]):
        bot.send_message(message.chat.id, p.set_week())

    elif (message.text == BOT_COMMANDS[3]):
        bot.send_message(message.chat.id, "4")

    elif (message.text == BOT_COMMANDS[4]):
        bot.send_message(message.chat.id, get_random_article_from_architect4u())


bot.infinity_polling()
