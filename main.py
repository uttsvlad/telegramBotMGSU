from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import urlworker

TOKEN = "5118191064:AAGkLtD7YJkPMXV2uZaCp4M0txgEOO5KFQ8"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

BOT_COMMANDS = ["Расписание на сегодня", "Расписание на завтра", "Какая сейчас неделя?", "Какая сейчас пара по счету?",
                "Статья об архитектуре"]
BOT_BUTTONS = []
for command in BOT_COMMANDS:
    BOT_BUTTONS.append(types.KeyboardButton(command))

mgsu_parser = urlworker.ParserFactory.create_mgsu_parser()
articles_parser = urlworker.ParserFactory.create_articles_parser()


@dp.message_handler(commands=['start', 'help'])
async def process_start_command(msg: types.Message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for button in BOT_BUTTONS:
        markup.add(button)
    await bot.send_message(msg.from_user.id, "Выберите нужную кнопку:", reply_markup=markup)


@dp.message_handler(content_types=["text"])
async def message_reply(message):
    if message.text == BOT_COMMANDS[0]:
        await bot.send_message(message.chat.id, "1")

    elif message.text == BOT_COMMANDS[1]:
        await bot.send_message(message.chat.id, "2")

    elif message.text == BOT_COMMANDS[2]:

        text = await mgsu_parser.set_week()
        await bot.send_message(message.chat.id, text)

    elif message.text == BOT_COMMANDS[3]:
        await bot.send_message(message.chat.id, "4")

    elif message.text == BOT_COMMANDS[4]:

        text = await articles_parser.get_random_article()
        await bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    executor.start_polling(dp)
