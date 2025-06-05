from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from loader import dp
from aiogram.types import ReplyKeyboardRemove
from data.config import ADMINS
from data.config import DOCTORS
from filters import IsAdmin
import handlers


patient_message = 'Мониторинг пациента'
addmin_message = 'Добавить администратора'
adddoc_message = 'Добавить пользователя'
help_message = 'Помощь'
points=0
sepsis=False
num_question=0
q_tags=['Алиментарный, алкогольный', 'Билиарный', 'Посттравматический (послеоперационный, постпапиллотомический)',
        'Не установлена', 'Хирургическое отделение', 'Реаниматологическое отделение', 'Амилаза повышена в 3 и более раз на момент заполнения карты?',
        'Липаза повышена в 3 и более раз на момент заполнения карты?', 'Головка ПЖ увеличена в размерах?',
        'Тело ПЖ увеличено в размерах?', 'Хвост ПЖ увеличен в размерах?', 'Свободная жидкость в сальлниковой сумке',
        'Свободная жидкость в брюшной полости', 'Расширение общего желчного протока более 9 мм', 'Наличие тёмно-вишнёвого выпота в брюшной полости',
        'Наличие бляшек стеатонекроза', 'Установлен дренаж в брюшную полость', 'Установлен дренаж в сальниковую сумку',
        'Холецистостома', 'Гипокальциемия меньше 1.2 ммоль/л', 'Гемоконцентрация:\nгемоглобин крови > 160 г/л или\nгематокрит > 40',
        'Гипергликемия > 10 ммоль/л', 'C-реактивный белок > 120 мг/л', 'Шок (систолическое АД меньше 90 мм рт. ст.)',
        'Дыхательная недостаточность (pO2 меньше 60 мм рт. ст.)', 'Почечная недостаточность (олиго-анурия, креатинин > 177 мкмоль/л)',
        'Концентрация билирубина > 35 мкмоль/л', 'Церебральная недостаточность (делирий, сопор, кома)',
        'Желудочно-кишечное кровотечение (более 500 мл/сутки)', 'Коагулопатия (тромбоциты меньше 100x10^9/л, фибриноген меньше 1 г/л)',
        'Острое жидкостное скопление', 'Псевдокиста поджелудочной железы', 'Перипанкретический инфильтрат',
        'Абсцесс сальниковой сумки и забрюшинного пространства', 'Распространённый гнойно-некротический парапанкреатит',
        'Тромбоз селезеночной или воротной вен', 'Некроз ободочной кишки, нарушение эвакуации из желудка',
        'Полиорганная недостаточность', 'Дигестивные свищи', 'Механическая желтуха', 'Панкреатический свищ',
        'Гнойный перитонит', 'Сепсис', 'Аррозивное кровотечение']
questions={'Алиментарный, алкогольный' : ['Этиология панкреатита:', 1],
           'Билиарный' : ['Этиология панкреатита:', 3],
           'Посттравматический (послеоперационный, постпапиллотомический)' : ['Этиология панкреатита:', 1],
           'Не установлена' : ['Этиология панкреатита:', 1],
           'Хирургическое отделение' : ['Где находится больной на лечении?', 1],
           'Реаниматологическое отделение' : ['Где находится больной на лечении?', 3],
           'Амилаза повышена в 3 и более раз на момент заполнения карты?' : ['Уровень ферментации:', 1],
           'Липаза повышена в 3 и более раз на момент заполнения карты?' : ['Уровень ферментации:', 1],
           'Головка ПЖ увеличена в размерах?' : ['Данные УЗИ:', 1],
           'Тело ПЖ увеличено в размерах?' : ['Данные УЗИ:', 1],
           'Хвост ПЖ увеличен в размерах?' : ['Данные УЗИ:', 1],
           'Свободная жидкость в сальлниковой сумке' : ['Данные УЗИ:', 2],
           'Свободная жидкость в брюшной полости' : ['Данные УЗИ:', 2],
           'Расширение общего желчного протока более 9 мм' : ['Данные УЗИ:', 2],
           'Наличие тёмно-вишнёвого выпота в брюшной полости' : ['Данные диагностической (лечебной) лапароскопии (при наличии):', 2],
           'Наличие бляшек стеатонекроза' : ['Данные диагностической (лечебной) лапароскопии (при наличии):', 2],
           'Установлен дренаж в брюшную полость' : ['Данные диагностической (лечебной) лапароскопии (при наличии):', 1],
           'Установлен дренаж в сальниковую сумку' : ['Данные диагностической (лечебной) лапароскопии (при наличии):', 1],
           'Холецистостома' : ['Данные диагностической (лечебной) лапароскопии (при наличии):', 1],
           'Гипокальциемия меньше 1.2 ммоль/л' : ['Органная дисфункция:', 1],
           'Гемоконцентрация:\nгемоглобин крови > 160 г/л или\nгематокрит > 40' : ['Органная дисфункция:', 1],
           'Гипергликемия > 10 ммоль/л' : ['Органная дисфункция:', 1],
           'C-реактивный белок > 120 мг/л' : ['Органная дисфункция:', 2],
           'Шок (систолическое АД меньше 90 мм рт. ст.)' : ['Органная дисфункция:', 3],
           'Дыхательная недостаточность (pO2 меньше 60 мм рт. ст.)' : ['Органная дисфункция:', 3],
           'Почечная недостаточность (олиго-анурия, креатинин > 177 мкмоль/л)' : ['Органная дисфункция:', 3],
           'Концентрация билирубина > 35 мкмоль/л' : ['Органная дисфункция:', 1],
           'Церебральная недостаточность (делирий, сопор, кома)' : ['Органная дисфункция:', 3],
           'Желудочно-кишечное кровотечение (более 500 мл/сутки)' : ['Органная дисфункция:', 3],
           'Коагулопатия (тромбоциты меньше 100x10^9/л, фибриноген меньше 1 г/л)' : ['Органная дисфункция:', 1],
           'Острое жидкостное скопление' : ['Наличие осложнений:', 2],
           'Псевдокиста поджелудочной железы' : ['Наличие осложнений:', 2],
           'Перипанкретический инфильтрат' : ['Наличие осложнений:', 2],
           'Абсцесс сальниковой сумки и забрюшинного пространства' : ['Наличие осложнений:', 3],
           'Распространённый гнойно-некротический парапанкреатит' : ['Наличие осложнений:', 3],
           'Тромбоз селезеночной или воротной вен' : ['Наличие осложнений:', 2],
           'Некроз ободочной кишки, нарушение эвакуации из желудка' : ['Наличие осложнений:', 3],
           'Полиорганная недостаточность' : ['Наличие осложнений:', 3],
           'Дигестивные свищи' : ['Наличие осложнений:', 2],
           'Механическая желтуха' : ['Наличие осложнений:', 3],
           'Панкреатический свищ' : ['Наличие осложнений:', 3],
           'Гнойный перитонит' : ['Наличие осложнений:', 3],
           'Сепсис' : ['Наличие осложнений:', 3],
           'Аррозивное кровотечение' : ['Наличие осложнений:', 3]}

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    cid = message.chat.id
    if cid not in ADMINS and cid not in DOCTORS:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(help_message)
        await message.answer('''Здравствуйте! Это бот по ведению пациентов с острым аппендицитом. Вы не зарегистрированы в системе, Ваш id: '''+str(
            message.chat.id)+'\n\nПопросить зарегистрировать Вас или же задать вопрос можно по команде /sos', reply_markup=markup)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(patient_message)
        await message.answer(
            '''Здравствуйте! Это бот по ведению пациентов с острым аппендицитом.
            \n\nПри возникновении вопросов обратитесь к команде /sos''', reply_markup=markup)

@dp.message_handler(text=help_message)
async def cmd_start(message: types.Message):
    await message.answer(
        '''Чтобы Вас зарегистрировали, необходимо выслать через /sos свой id''')

@dp.message_handler(IsAdmin(), commands='admin')
async def cmd_start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(addmin_message, adddoc_message)
    await message.answer(
        '''Добро пожаловать в режим администратора''', reply_markup=markup)

from aiogram.types import Message
from states import AddUser, AddAdm
from aiogram.dispatcher import FSMContext
from keyboards.default.markups import all_right_message, cancel_message, submit_markup
@dp.message_handler(IsAdmin(), text=adddoc_message)
async def cmd_sos(message: Message):
    await AddUser.tg_id.set()
    await message.answer(
        'Впешите ID пользователя, которого хотите сделать пользователем.',
        reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=AddUser.tg_id)
async def process_question(message: Message, state: FSMContext):
    async with state.proxy()as data:
        data['tg_id'] = message.text

    await message.answer('Убедитесь, что все верно.',
                         reply_markup=submit_markup())
    await AddUser.next()

@dp.message_handler(
    lambda message: message.text not in [cancel_message, all_right_message],
    state=AddUser.submit)
async def process_price_invalid(message: Message):
    await message.answer('Такого варианта не было.')

@dp.message_handler(text=cancel_message, state=AddUser.submit)
async def process_cancel(message: Message, state: FSMContext):
    await message.answer('Отменено!', reply_markup=ReplyKeyboardRemove())
    await state.finish()

@dp.message_handler(text=all_right_message, state=AddUser.submit)
async def process_cancel(message: Message, state: FSMContext):
    async with state.proxy() as data:
        add_id=int(data['tg_id'])
    if add_id not in DOCTORS:
        DOCTORS.append(add_id)
    await message.answer('Выполнено!', reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(IsAdmin(), text=addmin_message)
async def cmd_sos(message: Message):
    await AddAdm.tg_id.set()
    await message.answer(
        'Впешите ID пользователя, которого хотите сделать админом.',
        reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=AddAdm.tg_id)
async def process_question(message: Message, state: FSMContext):
    async with state.proxy()as data:
        data['tg_id'] = message.text

    await message.answer('Убедитесь, что все верно.',
                         reply_markup=submit_markup())
    await AddAdm.next()

@dp.message_handler(
    lambda message: message.text not in [cancel_message, all_right_message],
    state=AddAdm.submit)
async def process_price_invalid(message: Message):
    await message.answer('Такого варианта не было.')

@dp.message_handler(text=cancel_message, state=AddAdm.submit)
async def process_cancel(message: Message, state: FSMContext):
    await message.answer('Отменено!', reply_markup=ReplyKeyboardRemove())
    await state.finish()

@dp.message_handler(text=all_right_message, state=AddAdm.submit)
async def process_cancel(message: Message, state: FSMContext):
    async with state.proxy() as data:
        add_id=int(data['tg_id'])
    if add_id not in ADMINS:
        ADMINS.append(add_id)
    await message.answer('Выполнено!', reply_markup=ReplyKeyboardRemove())
    await state.finish()


from aiogram import executor
from logging import basicConfig, INFO

from loader import db, bot

async def on_startup(dp):
    basicConfig(level=INFO)
    db.create_tables()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
from aiogram import executor
from logging import basicConfig, INFO

from loader import db, bot

async def on_startup(dp):
    basicConfig(level=INFO)
    db.create_tables()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
