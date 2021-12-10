from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

import os
import json
from state_machine import machine, lump

with open('questions/questions.json') as q:
    questions = json.load(q)

TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

size_pizza_keyboard = InlineKeyboardMarkup(row_width=2)
big_pizza = InlineKeyboardButton(text='Большую', callback_data="big_pizza")
small_pizza = InlineKeyboardButton(text='Маленькую', callback_data="small_pizza")
size_pizza_keyboard.add(big_pizza, small_pizza)

payment_method_keyboard = InlineKeyboardMarkup(row_width=2)
payment_method_card = InlineKeyboardButton(text='Картой', callback_data="payment_method_card")
payment_method_cash = InlineKeyboardButton(text='Наличкой', callback_data="payment_method_cash")
payment_method_keyboard.add(payment_method_card, payment_method_cash)

confirm_keyboard = InlineKeyboardMarkup(row_width=2)
positive = InlineKeyboardButton(text='Да', callback_data='positive')
negative = InlineKeyboardButton(text='Нет', callback_data='negative')
confirm_keyboard.add(positive, negative)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, questions.get('question_1'), reply_markup=size_pizza_keyboard)
    machine.set_state('start')


@dp.callback_query_handler()
async def messages(call: types.CallbackQuery):
    if call.data == 'big_pizza':
        lump.trigger('pizza_size')
        lump.pizza_size = 'большую'
        await bot.send_message(call.from_user.id, questions.get('question_2'), reply_markup=payment_method_keyboard)
    elif call.data == 'small_pizza':
        lump.trigger('pizza_size')
        lump.pizza_size = 'маленькую'
        await bot.send_message(call.from_user.id, questions.get('question_2'), reply_markup=payment_method_keyboard)
    elif call.data == 'payment_method_card':
        lump.trigger('payment_method')
        lump.payment_method = 'картой'
        msg = questions.get('question_3').replace('SIZE', lump.get_answers()[0]).\
            replace('PAYMETHOD', lump.get_answers()[1])
        await bot.send_message(call.from_user.id, msg, reply_markup=confirm_keyboard)
    elif call.data == 'payment_method_cash':
        lump.trigger('payment_method')
        lump.payment_method = 'наличкой'
        msg = questions.get('question_3').replace('SIZE', lump.get_answers()[0]).\
            replace('PAYMETHOD', lump.get_answers()[1])
        await bot.send_message(call.from_user.id, msg, reply_markup=confirm_keyboard)
    elif call.data == 'positive':
        lump.trigger('final')
        await bot.send_message(call.from_user.id, 'Спасибо за заказ')
    elif call.data == 'negative':
        machine.set_state('start')
        await bot.send_message(call.from_user.id, questions.get('question_1'), reply_markup=size_pizza_keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
