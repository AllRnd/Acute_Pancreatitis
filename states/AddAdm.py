from aiogram.dispatcher.filters.state import StatesGroup, State


class AddAdm(StatesGroup):
    tg_id = State()
    submit = State()
