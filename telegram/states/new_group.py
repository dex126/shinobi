from aiogram.fsm.state import StatesGroup, State

class NewGroup(StatesGroup):
    waiting_for_group = State()
