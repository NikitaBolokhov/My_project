from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.keyboards import regular_keyboard
from states.states import FSMforgame

router: Router = Router()


# Этот хэндлер будет срабатывать на остальные текстовые сообщения вне состояний
@router.message(StateFilter(default_state))
async def process_other_text_answers(message: Message):
    try:
        await message.copy_to(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text=LEXICON_RU['update_error'])


# Этот хэндлер будет срабатывать на остальные текстовые сообщения
# в состоянии 'in_game'
@router.message(StateFilter(FSMforgame.in_game))
async def process_other_text_answers_in_game(message: Message):
    await message.answer(text=LEXICON_RU['in_game'],
                         reply_markup=regular_keyboard(
                             [LEXICON_RU['name_button_exit']]))


# Этот хэндлер будет срабатывать на остальные текстовые сообщения
# в состоянии 'in_ssp'
@router.message(StateFilter(FSMforgame.in_ssp))
async def process_other_text_answers_in_ssp(message: Message):
    await message.answer(text=LEXICON_RU['in_ssp'],
                         reply_markup=regular_keyboard(
                             [LEXICON_RU['continue_button'],
                              LEXICON_RU['exit']]))
