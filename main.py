from contextlib import nullcontext
from unicodedata import name
from USDT import parse
from BTC import parse_BTC
from ETH import parse_ETH
from BUSD import parse_BUSD
from BNB import parse_BNB
from SHIB import parse_SHIB
from MARKET import market_parse
from urllib import request
from datetime import datetime
import requests
from bs4 import BeautifulSoup as BS
import config 
import asyncio
import time
import logging
from datetime import datetime
import aioschedule
from aiogram import Bot, Dispatcher, executor, types
from MAINPARSE import main_parse
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from sqlighter import SQLighter
from aiogram.utils.deep_linking import get_start_link
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# Configure logging
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)
id = 0 
lg = 0
# инициализируем соединение с БД
db = SQLighter('db.db')

class Form(StatesGroup):
    LOGIN = State()
    PASSW = State()
    NAME = State()
    FIN = State()
    REGISTRATION = State()
    lg = State()
    ps = State()
    YEAR=State()
    adm_set=State()
    life=State()
def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None

@dp.message_handler(commands='start')
async def subscribe_from_start(message: types.Message):


    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_1 = types.KeyboardButton(text="PARSE BINANCE!")
    button_3 = types.KeyboardButton(text="EXIT")
    getId=types.KeyboardButton(text="ПОЛУЧИТЬ ID")
    availeble=types.KeyboardButton(text="ДАТЬ ДОСТУП К ТАБЛИЦЕ НА МЕСЯЦ!")
    year = types.KeyboardButton(text="ДАТЬ ДОСТУП К ТАБЛИЦЕ НА ГОД!")
    life = types.KeyboardButton(text="ДАТЬ ПОЖИЗНЕННЫЙ ДОСТУП К ТАБЛИЦЕ!")
    unique_code = extract_unique_code(message.text)

    if unique_code:
    #если есть id рефера
        if(not db.subscriber_exists(message.from_user.id)):
    	# если юзера нет в базе, добавляем его
            db.add_subscriber(message.from_user.id,unique_code)

            subscriptions = db.get_subscriptions()
            # отправляем всем новость
            for s in subscriptions:
                if s[1] == message.chat.id:
                    if s[6] == 1:
                        keyboard.add(availeble,year,life)
                        await bot.send_message(message.chat.id,f'Добропожаловать в меню администрации!', reply_markup=keyboard)
                    if s[5] == 0:
                        keyboard.add(getId)
                        await bot.send_message(message.chat.id,f'Для продолжения, после оплаты отправьте ваш ID администратору: @MrKeent',reply_markup=keyboard)
                    if s[5] == 1:
                       # keyboard.add(login)
                        await bot.send_message(message.chat.id,f'Ваш ID одобрен!',reply_markup=keyboard)


        else:
        	# если он уже есть, то просто обновляем ему статус подписки
            db.update_subscription(message.from_user.id, True)
            unique_code = extract_unique_code(message.text)

            subscriptions = db.get_subscriptions()
            # отправляем всем новость
            for s in subscriptions:
                if s[1] == message.chat.id:
                    if s[6] == 1:
                        keyboard.add(availeble,year,life)
                        await bot.send_message(message.chat.id,f'Добропожаловать в меню администрации!', reply_markup=keyboard)
                    if s[5] == 0:
                        keyboard.add(getId)
                        await bot.send_message(message.chat.id,f'Для продолжения, после оплаты отправьте ваш ID администратору: @MrKeent',reply_markup=keyboard)
                    
    else:
       #если в ссылке нет id рефера
        db.add_subscriber(message.from_user.id,unique_code)

        unique_code = extract_unique_code(message.text)
        subscriptions = db.get_subscriptions()
        # отправляем всем новость
        for s in subscriptions:
            if s[1] == message.chat.id:
                if s[6] == 1:
                    keyboard.add(availeble,year,life)
                    await bot.send_message(message.chat.id,f'Добропожаловать в меню администрации!', reply_markup=keyboard)
                if s[5] == 0:
                    keyboard.add(getId)
                    await bot.send_message(message.chat.id,f'Для продолжения, после оплаты отправьте ваш ID администратору: @MrKeent',reply_markup=keyboard)
                if s[5] == 1:
                  #  keyboard.add(login)
                    await bot.send_message(message.chat.id,f'Пожалуйста, войдите в аккаунт',reply_markup=keyboard)

@dp.message_handler(content_types=['text'])
async def subscribe(message):
    if message.text=="ДАТЬ ДОСТУП К ТАБЛИЦЕ НА МЕСЯЦ!":
       
        subscriptions = db.get_subscriptions()
        for s in subscriptions:
            if s[1] == message.chat.id:
                if s[6] == 1:
                    await Form.LOGIN.set()
                    await bot.send_message(message.chat.id,f"Введите ID человека которому нужно предоставить доступ:")
    
    if message.text=="ДАТЬ ДОСТУП К ТАБЛИЦЕ НА ГОД!":
       
        subscriptions = db.get_subscriptions()
        for s in subscriptions:
            if s[1] == message.chat.id:
                if s[6] == 1:
                    await Form.YEAR.set()
                    await bot.send_message(message.chat.id,f"Введите ID человека которому нужно предоставить доступ:")
    
    if message.text=="ДАТЬ ПОЖИЗНЕННЫЙ ДОСТУП К ТАБЛИЦЕ!":
        subscriptions = db.get_subscriptions()
        for s in subscriptions:
            if s[1] == message.chat.id:
                if s[6] == 1:
                    await Form.life.set()
                    await bot.send_message(message.chat.id,f"Введите ID человека которому нужно предоставить доступ:")

    if message.text =="DB data":
        subscriptions = db.get_subscriptions()
        # отправляем всем новость
        for s in subscriptions:
            await bot.send_message(message.chat.id,f'id: {s[1]}\n\nname: {s[3]}\n\nemail: {s[6]}\n\n password: {s[7]}')

    if message.text =="PARSE BINANCE!": 
        global id
        id = message.chat.id
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

        getId=types.KeyboardButton(text="ПОЛУЧИТЬ ID")
        keyboard.add(getId)
        subscriptions = db.get_subscriptions()
        # отправляем всем новость
        for s in subscriptions:
            if s[8] == 0:
                if s[7] == datetime.now().month:
                    await bot.send_message(s[1],f"Ваша подписка подошла к концу, для обновления обратитесь к администратору:@MrKeent ",reply_markup=keyboard)  
                    db.up_Login(0,s[1])
                else:
                    await bot.send_message(message.chat.id,f'Данные парсяться, подождите минутку...')
                    parse()
                    await bot.send_message(id,f'20%...')
                    parse_BTC()    
                    parse_ETH()
                    await bot.send_message(id,f'40%...')
                    parse_BUSD()
                    parse_BNB()
                    await bot.send_message(id,f'60%...')
                    parse_SHIB()
                    await bot.send_message(id,f'80%...')
                    market_parse()
                    await bot.send_message(id,f'100%')
                    await bot.send_message(message.chat.id,f'Данные спарсились, ожидайте отправку файла...')
                    await message.reply_document(open('binance.xlsx', 'rb'))

            if s[8] ==datetime.now().year:
                if s[7]==datetime.now().month:
                    await bot.send_message(s[1],f"Ваша подписка подошла к концу, для обновления обратитесь к администратору:@MrKeent ",reply_markup=keyboard)  
                    db.up_Login(0,s[1])
                else:
                    await bot.send_message(message.chat.id,f'Данные парсяться, подождите минутку...')
                    parse()
                    await bot.send_message(id,f'20%...')
                    parse_BTC()    
                    parse_ETH()
                    await bot.send_message(id,f'40%...')
                    parse_BUSD()
                    parse_BNB()
                    await bot.send_message(id,f'60%...')
                    parse_SHIB()
                    await bot.send_message(id,f'80%...')
                    market_parse()
                    await bot.send_message(id,f'100%')
                    await bot.send_message(message.chat.id,f'Данные спарсились, ожидайте отправку файла...')
                    await message.reply_document(open('binance.xlsx', 'rb'))


    if message.text =="ELSE CRYPTOBIRGE!": 
        await bot.send_message(message.chat.id,f'Данный функционал ещё не реализован')

    if message.text =="ПОЛУЧИТЬ ID":
        await bot.send_message(message.chat.id,f'Ваш ID: {message.chat.id}')
    if message.text == "АДМИНКА":
        if message.chat.id == 685710474:
            await Form.adm_set.set()
            await bot.send_message(685710474,f'Введите id человека которому выдать права администратора:')
       
@dp.message_handler(state = Form.LOGIN)
async def Bitcoin_payments(message: types.Message, state: FSMContext):
    id = message.text
    date = datetime.now()
    #await bot.send_message(message.chat.id,f'MONTH: {month.month}')
    db.update_month_sub(id,date.month+1)

    db.up_Login(1,id) 
    await bot.send_message(message.chat.id,f'Доступ к таблице для аккаунта {id} предоставлен!')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_1 = types.KeyboardButton(text="PARSE BINANCE!")

    
    keyboard.add(button_1)
    await bot.send_message(id,f'Оплата прошла успешно, вам предоставлен доступ к таблице!',reply_markup=keyboard)
    await state.finish()


@dp.message_handler(state = Form.YEAR)
async def Bitcoin_payments(message: types.Message, state: FSMContext):
    id = message.text
    date = datetime.now()
    #await bot.send_message(message.chat.id,f'MONTH: {month.month}')
    db.update_month_sub(id,date.month)
    db.update_year_sub(id,date.year+1)
    db.up_Login(1,id) 
    await bot.send_message(message.chat.id,f'Доступ к таблице для аккаунта {id} предоставлен!')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_1 = types.KeyboardButton(text="PARSE BINANCE!")

    
    keyboard.add(button_1)
    await bot.send_message(id,f'Оплата прошла успешно, вам предоставлен доступ к таблице!',reply_markup=keyboard)
    await state.finish()

@dp.message_handler(state = Form.life)
async def Bitcoin_payments(message: types.Message, state: FSMContext):
    id = message.text
    db.update_month_sub(id,0)
    
    db.up_Login(1,id) 
    await bot.send_message(message.chat.id,f'Доступ к таблице для аккаунта {id} предоставлен!')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_1 = types.KeyboardButton(text="PARSE BINANCE!")
    
    keyboard.add(button_1)

    await bot.send_message(id,f'Оплата прошла успешно, вам предоставлен ПОЖИЗНЕННЫЙ ДОСТУП к таблице!',reply_markup=keyboard)
    await state.finish()


@dp.message_handler(state = Form.adm_set)
async def Bitcoin_payments(message: types.Message, state: FSMContext):
    id = message.text
    db.update_admin(id,1)
    db.up_Login(1,id) 
    await bot.send_message(message.chat.id,f'Доступ к меню администрации для аккаунта {id} предоставлен!')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_1 = types.KeyboardButton(text="PARSE BINANCE!")
    getId=types.KeyboardButton(text="ПОЛУЧИТЬ ID")
    availeble=types.KeyboardButton(text="ДАТЬ ДОСТУП К ТАБЛИЦЕ НА МЕСЯЦ!")
    year = types.KeyboardButton(text="ДАТЬ ДОСТУП К ТАБЛИЦЕ НА ГОД!")
    life = types.KeyboardButton(text="ДАТЬ ПОЖИЗНЕННЫЙ ДОСТУП К ТАБЛИЦЕ!")
    
    keyboard.add(button_1,getId)
    keyboard.row(availeble,year,life)

    await bot.send_message(id,f'Оплата прошла успешно, вам предоставлен доступ к таблице!',reply_markup=keyboard)
    await state.finish()


@dp.message_handler(state = Form.NAME)
async def Bitcoin_payments(message: types.Message, state: FSMContext):
    FIO = message.text
    db.add_name(message.chat.id,FIO)  

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_1 = types.KeyboardButton(text="PARSE BINANCE!")
    button_2 = types.KeyboardButton(text="ELSE CRYPTOBIRGE")
    button_3 = types.KeyboardButton(text="EXIT")
    keyboard.add(button_1,button_2)
    keyboard.row(button_3)

    await bot.send_message(message.chat.id,f'Ваш аккаунт успешно создан, можете приступать к использованию софта!',reply_markup=keyboard)

    db.up_Login(1,message.chat.id)
    await state.finish()


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
