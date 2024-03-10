from aiogram.fsm.state import State, StatesGroup


class CheckUserIdState(StatesGroup):
    enter_uid = State()
