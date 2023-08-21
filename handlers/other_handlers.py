from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.keyboards import exit_kb
from services.services import users

router: Router = Router()


# Этот хэндлер будет срабатывать на остальные текстовые сообщения
@router.message()
async def process_other_text_answers(message: Message):
    if message.from_user.id in users and users[message.from_user.id]['in_game']:
        await message.answer(text=LEXICON_RU['in_game'],
                             reply_markup=exit_kb)
    else:
        try:
            await message.copy_to(chat_id=message.chat.id)
        except TypeError:
            await message.reply(text=LEXICON_RU['update_error'])
