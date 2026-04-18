from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    choosing_platform = State()
    choosing_service = State()
    entering_link = State()
    entering_quantity = State()
    waiting_payment = State()
