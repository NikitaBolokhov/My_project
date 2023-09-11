from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import regular_keyboard, inline_keyboard
from lexicon.lexicon_ru import LEXICON_RU
from states.states import FSMforgame
from services.services import (ATTEMPTS,
                               users,
                               get_random_number,
                               show_attempts,
                               get_random_cat,
                               get_random_gif,
                               get_bot_choice,
                               get_winner)

router: Router = Router()


# Этот хэндлер будет срабатывать на команду "/start" вне состояний
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(
        text=f'<b>Привет🖐, {message.chat.first_name}!</b>\n'
             f'{LEXICON_RU["/start"]}')


# Этот хэндлер будет срабатывать на команду "/start" в состоянии 'in_game'
@router.message(CommandStart(), StateFilter(FSMforgame.in_game))
async def process_start_command_in_game(message: Message):
    await message.answer(text=LEXICON_RU['in_game'],
                         reply_markup=regular_keyboard(
                             [LEXICON_RU['name_button_exit']]))


# Этот хэндлер будет срабатывать на команду "/start" в состоянии 'in_ssp'
@router.message(CommandStart(), StateFilter(FSMforgame.in_ssp))
async def process_start_command_in_ssp(message: Message):
    await message.answer(text=LEXICON_RU['in_ssp'],
                         reply_markup=regular_keyboard(
                             [LEXICON_RU['continue_button'],
                              LEXICON_RU['exit']]))


# Этот хэндлер будет срабатывать на команду "/cat" вне состояний
@router.message(Command(commands=["cat"]), StateFilter(default_state))
async def process_cat_command(message: Message):
    result = get_random_cat()
    if result[0]:
        await message.reply_photo(result[1])
    else:
        await message.reply(text=LEXICON_RU['/cat_no'])


# Этот хэндлер будет срабатывать на команду "/cat" в состоянии 'in_game'
@router.message(Command(commands=["cat"]), StateFilter(FSMforgame.in_game))
async def process_cat_command_in_game(message: Message):
    await message.answer(text=LEXICON_RU['in_game'],
                         reply_markup=regular_keyboard(
                             [LEXICON_RU['name_button_exit']]))


# Этот хэндлер будет срабатывать на команду "/cat" в состоянии 'in_ssp'
@router.message(Command(commands=["cat"]), StateFilter(FSMforgame.in_ssp))
async def process_cat_command_in_ssp(message: Message):
    await message.answer(text=LEXICON_RU['in_ssp'],
                         reply_markup=regular_keyboard(
                             [LEXICON_RU['continue_button'],
                              LEXICON_RU['exit']]))


# Этот хэндлер будет срабатывать на команду "/gif" вне состояний
@router.message(Command(commands=["gif"]), StateFilter(default_state))
async def process_gif_command(message: Message):
    result = get_random_gif()
    if result[0]:
        await message.reply_animation(result[1])
    else:
        await message.reply(text=LEXICON_RU['/gif_no'])


# Этот хэндлер будет срабатывать на команду "/gif" в состоянии 'in_game'
@router.message(Command(commands=["gif"]), StateFilter(FSMforgame.in_game))
async def process_gif_command_in_game(message: Message):
    await message.answer(text=LEXICON_RU['in_game'],
                         reply_markup=regular_keyboard(
                             [LEXICON_RU['name_button_exit']]))


# Этот хэндлер будет срабатывать на команду "/gif" в состоянии 'in_ssp'
@router.message(Command(commands=["gif"]), StateFilter(FSMforgame.in_ssp))
async def process_gif_command_in_ssp(message: Message):
    await message.answer(text=LEXICON_RU['in_ssp'],
                         reply_markup=regular_keyboard(
                             [LEXICON_RU['continue_button'],
                              LEXICON_RU['exit']]))


# Этот хэндлер будет срабатывать на команду "/games" вне состояний
@router.message(Command(commands=['games']), StateFilter(default_state))
async def process_game_command(message: Message):
    await message.answer(text=LEXICON_RU['/games'],
                         reply_markup=inline_keyboard(
                             {LEXICON_RU['guess_the_number_button']:
                              'guess_the_number_pressed',
                              LEXICON_RU['rock_scissors_paper_button']:
                              'rock_scissors_paper_pressed'},
                             width=1))


# Этот хэндлер будет срабатывать на команду "/games" в состоянии 'in_game'
@router.message(Command(commands=['games']), StateFilter(FSMforgame.in_game))
async def process_game_command_in_game(message: Message):
    await message.answer(text=LEXICON_RU['in_game'],
                         reply_markup=regular_keyboard(
                             [LEXICON_RU['name_button_exit']]))


# Этот хэндлер будет срабатывать на команду "/games" в состоянии 'in_ssp'
@router.message(Command(commands=['games']), StateFilter(FSMforgame.in_ssp))
async def process_game_command_in_ssp(message: Message):
    await message.answer(text=LEXICON_RU['in_ssp'],
                         reply_markup=regular_keyboard(
                             [LEXICON_RU['continue_button'],
                              LEXICON_RU['exit']]))


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'guess_the_number_pressed'
@router.callback_query(F.data == 'guess_the_number_pressed',
                       StateFilter(default_state))
async def process_guess_the_number_press(callback: CallbackQuery):
    if callback.from_user.id not in users:
        users[callback.from_user.id] = {'secret_number': None,
                                        'attempts': None,
                                        'total_games': 0,
                                        'wins': 0}
    await callback.message.delete()
    await callback.message.answer(text=f'{LEXICON_RU["guess_the_number"]} '
                                  f' <b>{ATTEMPTS} попыток</b>.\n\n'
                                  f'Жми <b>Игра</b> и мы начнем😉',
                                  reply_markup=regular_keyboard(
                                          [LEXICON_RU['name_button_game'],
                                           LEXICON_RU['name_button_stat'],
                                           LEXICON_RU['name_button_exit']]))


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'rock_scissors_paper_pressed'
@router.callback_query(F.data == 'rock_scissors_paper_pressed',
                       StateFilter(default_state))
async def process_rock_scissors_paper_press(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON_RU['rock_scissors_paper'],
                                  reply_markup=regular_keyboard(
                                          [LEXICON_RU['yes_button'],
                                           LEXICON_RU['no_button']]))


"""Хэндлеры для игры 'Угадай число'"""


# Этот хэндлер будет срабатывать на кнопку "Статистика"
@router.message(F.text == LEXICON_RU['name_button_stat'],
                StateFilter(default_state))
async def process_stat_command(message: Message):
    await message.answer(
        text=f'Всего игр сыграно: '
             f'<b>{users[message.from_user.id]["total_games"]}</b>\n'
             f'Игр выиграно: <b>{users[message.from_user.id]["wins"]}</b>\n'
             f'<b>Хочешь поиграть?</b>😉',
        reply_markup=regular_keyboard([LEXICON_RU['name_button_game'],
                                       LEXICON_RU['name_button_exit']]))


# Этот хэндлер будет срабатывать на кнопку "Выход" вне состояний
@router.message(F.text == LEXICON_RU['name_button_exit'],
                StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text=LEXICON_RU['exit_button'])


# Этот хэндлер будет срабатывать на кнопку "Выход" в состоянии 'in_game'
@router.message(F.text == LEXICON_RU['name_button_exit'],
                StateFilter(FSMforgame.in_game))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['exit_button'])
    await state.clear()


# Этот хэндлер будет срабатывать на кнопку "Игра" вне состояний
@router.message(F.text == LEXICON_RU['name_button_game'],
                StateFilter(default_state))
async def process_go_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['game_button'])
    users[message.from_user.id]['secret_number'] = get_random_number()
    users[message.from_user.id]['attempts'] = ATTEMPTS
    await state.set_state(FSMforgame.in_game)


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@router.message(
        lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100,
        StateFilter(FSMforgame.in_game))
async def process_numbers_answer(message: Message, state: FSMContext):
    if int(message.text) == users[message.from_user.id]['secret_number']:
        await state.clear()
        await message.answer(text=f"{LEXICON_RU['win']}"
                                  f"{LEXICON_RU['one_more_game']}",
                             reply_markup=regular_keyboard(
                                 [LEXICON_RU['name_button_game'],
                                  LEXICON_RU['name_button_stat'],
                                  LEXICON_RU['name_button_exit']]))
        users[message.from_user.id]['total_games'] += 1
        users[message.from_user.id]['wins'] += 1
    elif int(message.text) > users[message.from_user.id]['secret_number']:
        users[message.from_user.id]['attempts'] -= 1
        if users[message.from_user.id]['attempts'] > 0:
            await message.answer(text=LEXICON_RU['smaller_number'])
        await message.answer(
            show_attempts(users[message.from_user.id]['attempts']))
    elif int(message.text) < users[message.from_user.id]['secret_number']:
        users[message.from_user.id]['attempts'] -= 1
        if users[message.from_user.id]['attempts'] > 0:
            await message.answer(text=LEXICON_RU['larger_number'])
        await message.answer(
            show_attempts(users[message.from_user.id]['attempts']))

    if users[message.from_user.id]['attempts'] == 0:
        await state.clear()
        await message.answer(
            text=f"{LEXICON_RU['lose']} "
                 f"<b>{users[message.from_user.id]['secret_number']}"
                 f"</b>.\n\n"
                 f"{LEXICON_RU['one_more_game']}",
            reply_markup=regular_keyboard(
                [LEXICON_RU['name_button_game'],
                 LEXICON_RU['name_button_stat'],
                 LEXICON_RU['name_button_exit']]))
        users[message.from_user.id]['total_games'] += 1


"""Хэндлеры для игры 'Камень, ножницы, бумага'"""


# Этот хэндлер срабатывает на согласие пользователя играть в игру
@router.message(F.text == LEXICON_RU['yes_button'],
                StateFilter(default_state))
async def process_yes_answer(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['yes'],
                         reply_markup=regular_keyboard(
                                        [LEXICON_RU['rock'],
                                         LEXICON_RU['scissors'],
                                         LEXICON_RU['paper']]))
    await state.set_state(FSMforgame.in_ssp)


# Этот хэндлер срабатывает на отказ пользователя играть в игру
@router.message(F.text == LEXICON_RU['no_button'],
                StateFilter(default_state))
async def process_no_answer(message: Message):
    await message.answer(text=LEXICON_RU['exit_button'])


# Этот хэндлер срабатывает на кнопку "Продолжить" вне состояний
@router.message(F.text == LEXICON_RU['continue_button'],
                StateFilter(default_state))
async def process_continue_answer(message: Message,  state: FSMContext):
    await message.answer(text=LEXICON_RU['yes'],
                         reply_markup=regular_keyboard(
                                        [LEXICON_RU['rock'],
                                         LEXICON_RU['scissors'],
                                         LEXICON_RU['paper']]))
    await state.set_state(FSMforgame.in_ssp)


# Этот хэндлер срабатывает на кнопку "Продолжить" в состоянии 'in_ssp'
@router.message(F.text == LEXICON_RU['continue_button'],
                StateFilter(FSMforgame.in_ssp))
async def process_continue_answer_in_ssp(message: Message):
    await message.answer(text=LEXICON_RU['yes'],
                         reply_markup=regular_keyboard(
                                        [LEXICON_RU['rock'],
                                         LEXICON_RU['scissors'],
                                         LEXICON_RU['paper']]))


# Этот хэндлер будет срабатывать на кнопку "Выйти" вне состояний
@router.message(F.text == LEXICON_RU['exit'],
                StateFilter(default_state))
async def process_exit_command(message: Message):
    await message.answer(text=LEXICON_RU['exit_button'])


# Этот хэндлер будет срабатывать на кнопку "Выйти" в состоянии 'in_ssp'
@router.message(F.text == LEXICON_RU['exit'],
                StateFilter(FSMforgame.in_ssp))
async def process_exit_command_in_ssp(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['exit_button'])
    await state.clear()


# Этот хэндлер срабатывает на любую из игровых кнопок
@router.message(F.text.in_([LEXICON_RU['rock'],
                            LEXICON_RU['paper'],
                            LEXICON_RU['scissors']]),
                StateFilter(FSMforgame.in_ssp))
async def process_game_button(message: Message, state: FSMContext):
    bot_choice = get_bot_choice()
    await message.answer(text=f'{LEXICON_RU["bot_choice"]} '
                              f'- {LEXICON_RU[bot_choice]}')
    winner = get_winner(message.text, bot_choice)
    await message.answer(text=LEXICON_RU[winner],
                         reply_markup=regular_keyboard(
                                      [LEXICON_RU['yes_button'],
                                       LEXICON_RU['no_button']]))
    await state.clear()
