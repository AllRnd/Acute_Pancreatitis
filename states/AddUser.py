from aiogram.dispatcher.filters.state import StatesGroup, State


class AddUser(StatesGroup):
    tg_id = State()
    submit = State()

