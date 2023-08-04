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
    await message.answer('Привет!\nМеня зовут Кото-бот!\nНапиши /menu и узнай, что я умею')


# Этот хэндлер будет срабатывать на команду "/menu"
@dp.message(Command(commands=["menu"]))
async def process_help_command(message: Message):
    await message.answer('Обычно я играю в попугая и повторяю за тобой, но не всегда:\n '
                         'нажми /cat и я порадую тебя котик(ом/ами)\n '
                         'нажми /gif и я кину в тебя гифкой')

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

# Этот хэндлер будет срабатывать на команду "/gif"
@dp.message(Command(commands=["gif"]))
async def process_help_command(message: Message):
    gif_response = requests.get('https://yesno.wtf/api')
    if gif_response.status_code == 200:
        gif_link = gif_response.json()['image']
        await message.reply_animation(gif_link)
    else:
        await message.reply('Сорян гифок не будет '
                            'Попробуй снова немного позже')

# Этот хэндлер будет срабатывать на любые ваши сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    try:
        await message.copy_to(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Данный тип апдейтов не поддерживается '
                                 'методом send_copy')


if __name__ == '__main__':
    dp.run_polling(bot)
