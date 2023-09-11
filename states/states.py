from aiogram.fsm.state import State, StatesGroup


# Класс, наследуемый от StatesGroup, для группы состояний FSM
class FSMforgame(StatesGroup):
    in_game = State()         # режим игры 'Угадай число'
    in_ssp = State()          # режим игры 'Камень, ножницы, бумага'
