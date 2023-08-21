from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from keyboards.keyboards import game_kb, stat_kb, exit_kb
from lexicon.lexicon_ru import LEXICON_RU
from services.services import *

router: Router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart())
async def process_start_command(message: Message):
    if message.from_user.id in users and users[message.from_user.id]['in_game']:
        await message.answer(text=LEXICON_RU['in_game'],
                             reply_markup=exit_kb)
    else:
        await message.answer(text=f'<b>Привет, {message.chat.first_name}!</b>\n '
                                  f'{LEXICON_RU["/start"]}')


# Этот хэндлер будет срабатывать на команду "/menu"
@router.message(Command(commands=["menu"]))
async def process_menu_command(message: Message):
    if message.from_user.id in users and users[message.from_user.id]['in_game']:
        await message.answer(text=LEXICON_RU['in_game'],
                             reply_markup=exit_kb)
    else:
        await message.answer(text=LEXICON_RU['/menu'])


# Этот хэндлер будет срабатывать на команду "/cat"
@router.message(Command(commands=["cat"]))
async def process_cat_command(message: Message):
    if message.from_user.id in users and users[message.from_user.id]['in_game']:
        await message.answer(text=LEXICON_RU['in_game'],
                             reply_markup=exit_kb)
    else:
        result = get_random_cat()
        if result[0]:
            await message.reply_photo(result[1])
        else:
            await message.reply(text=LEXICON_RU['/cat_no'])


# Этот хэндлер будет срабатывать на команду "/gif"
@router.message(Command(commands=["gif"]))
async def process_gif_command(message: Message):
    if message.from_user.id in users and users[message.from_user.id]['in_game']:
        await message.answer(text=LEXICON_RU['in_game'],
                             reply_markup=exit_kb)
    else:
        result = get_random_gif()
        if result[0]:
            await message.reply_animation(result[1])
        else:
            await message.reply(text=LEXICON_RU['/gif_no'])


# Этот хэндлер будет срабатывать на команду "/game"
@router.message(Command(commands=['game']))
async def process_game_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}
    await message.answer(text=f'{LEXICON_RU["/game"]} '
                              f' {ATTEMPTS} попыток',
                         reply_markup=game_kb)


# Этот хэндлер будет срабатывать на кнопку "Статистика"
@router.message(F.text == LEXICON_RU['name_button_stat'])
async def process_stat_command(message: Message):
    await message.answer(text=f'Всего игр сыграно: '
                              f'{users[message.from_user.id]["total_games"]}\n '
                              f'Игр выиграно: {users[message.from_user.id]["wins"]}\n '
                              f'Хочешь поиграть?',
                              reply_markup=stat_kb)


# Этот хэндлер будет срабатывать на кнопку "Выход"
@router.message(F.text == LEXICON_RU['name_button_exit'])
async def process_cancel_command(message: Message):
    await message.answer(text=LEXICON_RU['exit_button'])
    users[message.from_user.id]['in_game'] = False


# Этот хэндлер будет срабатывать на кнопку "Игра"
@router.message(F.text == LEXICON_RU['name_button_game'])
async def process_go_command(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(text=LEXICON_RU['game_button'])
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
    else:
        await message.answer(text=LEXICON_RU['in_game'],
                             reply_markup=exit_kb)


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@router.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer(text=LEXICON_RU['win'],
                                 reply_markup=game_kb)
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer(text=LEXICON_RU['smaller_number'])
            await message.answer(show_attempts(users[message.from_user.id]['attempts']))
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer(text=LEXICON_RU['larger_number'])
            await message.answer(show_attempts(users[message.from_user.id]['attempts']))

        if users[message.from_user.id]['attempts'] == 0:
            await message.answer(text=f"{LEXICON_RU['lose']} "
                                      f"{users[message.from_user.id]['secret_number']}",
                                 reply_markup=game_kb)
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
    else:
        await message.answer(text=LEXICON_RU['want_to_play'],
                             reply_markup=stat_kb)
