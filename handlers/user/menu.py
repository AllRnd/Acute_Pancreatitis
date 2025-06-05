from aiogram.types import Message, ReplyKeyboardMarkup
from loader import dp
from filters import IsAdmin, IsDoc

questions = '❓ Вопросы'


@dp.message_handler(IsAdmin(), commands='menu')
async def admin_menu(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(questions)

    await message.answer('Меню', reply_markup=markup)

import app
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery

@dp.message_handler(IsDoc(), text=app.patient_message)
async def process_settings(message: Message):
    app.points = 0
    app.sepsis = False
    app.num_question=0
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        'Да', callback_data='cet_yes'))
    markup.add(InlineKeyboardButton(
        'Нет', callback_data='cet_no'))
    text_ans = app.questions[app.q_tags[app.num_question]][0] + '\n\n' + app.q_tags[app.num_question]
    await message.answer(text_ans, reply_markup=markup)

@dp.callback_query_handler(IsDoc(), text='cet_yes')
async def add_category_callback_handler(query: CallbackQuery):
    await query.message.delete()
    app.points += app.questions[app.q_tags[app.num_question]][1]
    if app.questions[app.q_tags[app.num_question]][1]==3:
        app.sepsis=True
    app.num_question+=1
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        'Да', callback_data='cet_yes'))
    markup.add(InlineKeyboardButton(
        'Нет', callback_data='cet_no'))
    if app.num_question<len(app.q_tags):
        text_ans=app.questions[app.q_tags[app.num_question]][0]+'\n\n'+app.q_tags[app.num_question]
        await query.message.answer(text_ans, reply_markup=markup)
    else:
        if app.sepsis or app.points>20:
            text_ans = 'Необходима консультация с краевым (областным) гнойно-септическим центром'
        elif app.points>11:
            text_ans = 'Необходима консультация с межрайонной больницей'
        else:
            text_ans = 'Показано лечение в районной больнице'
        await query.message.answer(text_ans)
        app.num_question = 0
        app.points = 0
        app.sepsis = False

@dp.callback_query_handler(IsDoc(), text='cet_no')
async def add_category_callback_handler(query: CallbackQuery):
    await query.message.delete()
    app.num_question+=1
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        'Да', callback_data='cet_yes'))
    markup.add(InlineKeyboardButton(
        'Нет', callback_data='cet_no'))
    if app.num_question<len(app.q_tags):
        text_ans=app.questions[app.q_tags[app.num_question]][0]+'\n\n'+app.q_tags[app.num_question]
        await query.message.answer(text_ans, reply_markup=markup)
    else:
        if app.sepsis or app.points>20:
            text_ans = 'Необходима консультация с краевым (областным) гнойно-септическим центром'
        elif app.points>11:
            text_ans = 'Необходима консультация с межрайонной больницей'
        else:
            text_ans = 'Показано лечение в районной больнице'
        await query.message.answer(text_ans)
        app.num_question = 0
        app.points = 0
        app.sepsis = False
