import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
API_TOKEN: str = '6594894121:AAFMgwvN3saHhWBZKKEDA1SH6m8bmkfa3vU'
API_CATS_URL: str = 'https://api.thecatapi.com/v1/images/search'

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Кото-бот!\nНапиши /help и узнай, что я умею')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer('Обычно я играю в попугая и повторяю за тобой '
                        'Но если нажмешь /cat, я порадую тебя котик(ом/ами)')

# Этот хэндлер будет срабатывать на команду "/cat"
@dp.message(Command(commands=["cat"]))
async def process_help_command(message: Message):
    cat_response = requests.get(API_CATS_URL)
    if cat_response.status_code == 200:
        cat_link = cat_response.json()[0]['url']
        await message.reply_photo(cat_link)
    else:
        await message.reply('Сорян котов не будет '
                            'Попробуй снова немного позже')

# Этот хэндлер будет срабатывать на любые ваши сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Данный тип апдейтов не поддерживается '
                                 'методом send_copy')


if __name__ == '__main__':
    dp.run_polling(bot)
