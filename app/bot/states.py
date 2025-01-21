from aiogram.fsm.state import State, StatesGroup

class ProductStates(StatesGroup):
    waiting_for_articul = State()
