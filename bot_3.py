import telebot
from telebot import types
import re
import math
from typing import List

bot = telebot.TeleBot('5594968248:AAEb4rHYoPUZDowrczr3sGvxtixPBWTi1Kk')

def diff (numbers: List):
    print(numbers)
    result = numbers[0]
    for i, number in enumerate(numbers):
        if i == 0:
            continue
        result -= number
    return result

def div (numbers: List):
    print(numbers)
    result = numbers[0]
    for i, number in enumerate(numbers):
        if i == 0:
            continue
        result /= number
    return result

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/calc':
        bot.register_next_step_handler(message, get_numbers)  # следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Не понял запроса :(')


def get_numbers(message):
    question = 'Введите числа'
    bot.send_message(message.from_user.id, question)  # показываем клавиатуру
    bot.register_next_step_handler(message, calc)  # следующий шаг – функция get_name


def calc(message):
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_add = types.InlineKeyboardButton(text='+', callback_data=f'{message.text},add')  # кнопка «Да»
    keyboard.add(key_add)  # добавляем кнопку в клавиатуру
    key_diff = types.InlineKeyboardButton(text='-', callback_data=f'{message.text},diff')  # кнопка «Да»
    keyboard.add(key_diff)  # добавляем кнопку в клавиатуру
    key_mul = types.InlineKeyboardButton(text='*', callback_data=f'{message.text},mul')  # кнопка «Да»
    keyboard.add(key_mul)  # добавляем кнопку в клавиатуру
    key_div = types.InlineKeyboardButton(text='/', callback_data=f'{message.text},div')  # кнопка «Да»
    keyboard.add(key_div)  # добавляем кнопку в клавиатуру
    bot.send_message(message.from_user.id, text='Выбери операцию', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    numbers = re.findall(r'\d+', call.data)
    numbers = [int(i) for i in numbers]
    operation = call.data.split(',')[-1]
    if operation.strip() == "add":
        bot.send_message(call.message.chat.id, str(sum(numbers)))
    if operation.strip() == "diff":
        bot.send_message(call.message.chat.id, str(diff(numbers)))
    if operation.strip() == "mul":
        bot.send_message(call.message.chat.id, str(math.prod(numbers)))
    if operation.strip() == "div":
        bot.send_message(call.message.chat.id, str(div(numbers)))

bot.polling(none_stop=True, interval=0)
