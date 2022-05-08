import telebot

import res
import urlworker
from telebot import types

bot = telebot.TeleBot(res.TOKEN)

BOT_BUTTONS = []
for command in res.BOT_COMMANDS:
    BOT_BUTTONS.append(types.KeyboardButton(command))

mgsu_parser = urlworker.ParserFactory.create_mgsu_parser()
articles_parser = urlworker.ParserFactory.create_articles_parser()
directions = []


@bot.message_handler(commands=["start", "help"])
def process_start_command(msg: types.Message):
    bot.send_message(msg.from_user.id, f"Здравствуйте, {msg.from_user.first_name}! \n" +
                     "Выберите нужную кнопку:",
                     reply_markup=get_default_markup())


def get_default_markup():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for button in BOT_BUTTONS:
        markup.add(button)
    return markup


@bot.message_handler(content_types=["text"])
def message_reply(message):
    if message.text == res.BOT_COMMANDS[0]:
        result_list = mgsu_parser.get_door_opened__day()
        text = ""
        for data in result_list:
            text += (data + "\n\n")
        reg_markup = types.InlineKeyboardMarkup()
        reg_url = mgsu_parser.get_door_opened_day_reg_url()
        article_btn = types.InlineKeyboardButton(text="Регистрация", url=reg_url)
        reg_markup.add(article_btn)
        bot.send_message(message.chat.id, text, reply_markup=reg_markup)

    elif message.text == res.BOT_COMMANDS[1]:
        def get_levels_markup():
            levels_markup = types.InlineKeyboardMarkup()
            levels_markup.row_width = 1
            levels_markup.add(types.InlineKeyboardButton(res.BAC_OCH, callback_data="bac_och"),
                              types.InlineKeyboardButton(res.BAC_ZAOCH, callback_data="bac_zaoch"),
                              types.InlineKeyboardButton(res.BAC_OCH_ZAOCH, callback_data="bac_och_zaoch"),
                              types.InlineKeyboardButton(res.MAG_OCH, callback_data="mag_och"),
                              types.InlineKeyboardButton(res.MAG_ZAOCH, callback_data="mag_zaoch"),
                              types.InlineKeyboardButton(res.ASP, callback_data="asp"))
            return levels_markup

        def get_directions_markup(answer):
            directions_markup = types.ReplyKeyboardMarkup()
            directions_dict = mgsu_parser.get_directions(answer)
            directions_markup.add(types.KeyboardButton(res.BACK_EMOJI))
            for direction in directions_dict.keys():
                directions.append(direction)
                directions_markup.add(
                    types.KeyboardButton(direction))
            return directions_markup

        @bot.callback_query_handler(func=lambda call: True)
        def form_callback_query(level):
            if level.data == "asp":
                bot.answer_callback_query(level.id, res.ASP)
                bot.send_message(level.message.chat.id, mgsu_parser.get_info_about_direction("asp"))

            else:
                bot.answer_callback_query(level.id)
                bot.send_message(level.message.chat.id, res.CHOOSE_DIRECTION,
                                 reply_markup=get_directions_markup(level.data))

        bot.send_message(message.chat.id, res.CHOOSE_LEVEL, reply_markup=get_levels_markup())

    elif message.text == res.BOT_COMMANDS[2]:
        result = mgsu_parser.get_students_houses_with_img()
        bot.send_photo(message.chat.id, result[1])
        bot.send_message(message.chat.id, result[0])

    elif message.text == res.BOT_COMMANDS[3]:
        text = mgsu_parser.get_week()
        bot.send_message(message.chat.id, text)

    elif message.text == res.BOT_COMMANDS[4]:
        article_url = articles_parser.get_random_article()
        article_markup = types.InlineKeyboardMarkup()
        article_btn = types.InlineKeyboardButton(text="Читать", url=article_url)
        article_markup.add(article_btn)
        bot.send_message(message.chat.id, res.READ_EMOJI, reply_markup=article_markup)

    elif message.text == res.BACK_EMOJI:
        bot.send_message(message.chat.id, "Вы вернулись в меню", reply_markup=get_default_markup())

    elif directions.__contains__(message.text):
        bot.send_message(message.chat.id, mgsu_parser.get_info_about_direction(message.text),
                         reply_markup=get_default_markup())


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
