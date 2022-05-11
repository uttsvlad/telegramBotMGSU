import telebot
import res
import urlworker
from telebot import types
import jsonworker


bot = telebot.TeleBot(res.TOKEN)

BOT_BUTTONS = []
for command in res.BOT_COMMANDS:
    BOT_BUTTONS.append(types.KeyboardButton(command))

mgsu_parser = urlworker.ParserFactory.create_mgsu_parser()
articles_parser = urlworker.ParserFactory.create_articles_parser()
directions = []


@bot.message_handler(commands=["start"])
def process_start_command(msg: types.Message):
    jsonworker.check_registration(msg)
    bot.send_message(msg.from_user.id, f"Здравствуйте, {msg.from_user.first_name}! \n" +
                     "Выберите нужную кнопку:",
                     reply_markup=get_default_markup())


def get_default_markup():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for button in BOT_BUTTONS:
        markup.add(button)
    return markup


def get_keyboard_markup_from_list(elements_list):
    buttons = []
    for course in elements_list:
        buttons.append(types.KeyboardButton(course))

    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(types.KeyboardButton(res.BACK_EMOJI))
    for button in buttons:
        markup.add(button)
    return markup


def get_inline_markup_from_dict_with_callback_data(dictionary):
    markup = types.InlineKeyboardMarkup()
    for key in dictionary.keys():
        markup.add(types.InlineKeyboardButton(key, callback_data=dictionary.get(key)))
    return markup


def get_inline_markup_from_dict_with_urls(dictionary):
    markup = types.InlineKeyboardMarkup()
    for key in dictionary.keys():
        markup.add(types.InlineKeyboardButton(key, url=dictionary.get(key)))
    return markup


def send_courses_info(mes, course):
    course_result = {}

    if course == res.COURSES[0]:
        course_result = mgsu_parser.get_ege_courses()
    elif course == res.COURSES[1]:
        course_result = mgsu_parser.get_architect_course()
        bot.send_photo(mes.chat.id, course_result.pop("image"))
    course_text = course_result.pop("text")
    course_markup = types.InlineKeyboardMarkup()
    for key in course_result.keys():
        course_markup.add(types.InlineKeyboardButton(text=key, url=course_result.get(key)))
    bot.send_message(mes.chat.id, text=course_text, reply_markup=course_markup)


@bot.message_handler(content_types=["text"])
def message_reply(message):
    if message.text == res.BOT_COMMANDS[0]:
        result_list = mgsu_parser.get_door_opened__day()
        text = ""
        for data in result_list:
            text += (data + "\n\n")
        reg_markup = types.InlineKeyboardMarkup()
        reg_url = mgsu_parser.get_door_opened_day_reg_url()
        article_btn = types.InlineKeyboardButton(text=res.REGISTRATION, url=reg_url)
        reg_markup.add(article_btn)
        bot.send_message(message.chat.id, text, reply_markup=reg_markup)

    elif message.text == res.BOT_COMMANDS[1]:
        olympics_dict = mgsu_parser.get_olympics()
        bot.send_message(message.chat.id, res.OLYMPICS,
                         reply_markup=get_inline_markup_from_dict_with_urls(olympics_dict))

    elif message.text == res.BOT_COMMANDS[2]:
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
        def form_callback_query(lvl):
            if lvl.data == "asp":
                bot.answer_callback_query(lvl.id, res.LEVELS[2])
                bot.send_message(lvl.message.chat.id, mgsu_parser.get_info_about_direction("asp"))

            else:
                bot.answer_callback_query(lvl.id)
                bot.send_message(lvl.message.chat.id, res.CHOOSE_DIRECTION,
                                 reply_markup=get_directions_markup(lvl.data))

        bot.send_message(message.chat.id, res.CHOOSE_LEVEL,
                         reply_markup=get_inline_markup_from_dict_with_callback_data(res.LEVELS_DICT))

    elif message.text == res.BOT_COMMANDS[3]:
        bot.send_message(message.chat.id, text=res.CHOOSE_COURSE,
                         reply_markup=get_keyboard_markup_from_list(res.COURSES))

    elif message.text == res.BOT_COMMANDS[4]:
        result = mgsu_parser.get_students_houses_with_img()
        bot.send_photo(message.chat.id, result[0])
        bot.send_message(message.chat.id, result[1])

    elif message.text == res.BOT_COMMANDS[5]:
        bot.send_message(message.chat.id, text=res.CHOOSE_LEVEL, reply_markup=get_keyboard_markup_from_list(res.LEVELS))

    elif message.text == res.BOT_COMMANDS[6]:
        article_url = articles_parser.get_random_article()
        article_markup = types.InlineKeyboardMarkup()
        article_btn = types.InlineKeyboardButton(text=res.READ, url=article_url)
        article_markup.add(article_btn)
        bot.send_message(message.chat.id, res.READ_EMOJI, reply_markup=article_markup)

    elif message.text == res.BOT_COMMANDS[7]:
        text = mgsu_parser.get_week()
        bot.send_message(message.chat.id, text)
    elif message.text == res.BACK_EMOJI:
        bot.send_message(message.chat.id, res.BACK_IN_MENU, reply_markup=get_default_markup())

    elif message.text in mgsu_parser.directions_result_dict:
        bot.send_message(message.chat.id, mgsu_parser.get_info_about_direction(message.text))

    elif message.text in res.COURSES:
        send_courses_info(message, message.text)

    elif message.text in res.LEVELS:
        level = message.text
        level_dict = {}
        if level == res.LEVELS[0]:
            level_dict = res.BAC_ADD_INFO
        elif level == res.LEVELS[1]:
            level_dict = res.MAG_ADD_INFO
        elif level == res.LEVELS[2]:
            level_dict = res.ASP_ADD_INFO
        bot.send_message(message.chat.id, "Дополнительная информация (" + level + "):",
                         reply_markup=get_inline_markup_from_dict_with_urls(level_dict))


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
