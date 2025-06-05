from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from data.config import DOCTORS


class IsDoc(BoundFilter):

    async def check(self, message: Message):
        return message.from_user.id in DOCTORS