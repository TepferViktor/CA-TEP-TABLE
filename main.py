from unicodedata import name
from USDT import parse
from BTC import parse_BTC
from ETH import parse_ETH
from BUSD import parse_BUSD
from BNB import parse_BNB
from SHIB import parse_SHIB
from MARKET import market_parse
from urllib import request
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

def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None

@dp.message_handler(commands='start')
async def subscribe_from_start(message: types.Message):

    REGIS = types.ReplyKeyboardMarkup(resize_keyboard=True)

    login = types.KeyboardButton(text="LOGIN")
    registration = types.KeyboardButton(text="REGISTRATION")
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
                    if s[5] == 0:
                        REGIS.add(registration)
                        await bot.send_message(message.chat.id,f'Пожалуйста, зарегестрируйтесь в аккаунте',reply_markup=REGIS)
                    if s[5] == 1:
                        REGIS.add(login)
                        await bot.send_message(message.chat.id,f'Пожалуйста, войдите в аккаунт',reply_markup=REGIS)

        else:
        	# если он уже есть, то просто обновляем ему статус подписки
            db.update_subscription(message.from_user.id, True)
            unique_code = extract_unique_code(message.text)

            subscriptions = db.get_subscriptions()
            # отправляем всем новость
            for s in subscriptions:
                if s[1] == message.chat.id:
                    if s[5] == 0:
                        REGIS.add(registration)
                        await bot.send_message(message.chat.id,f'Пожалуйста, зарегестрируйтесь в аккаунте',reply_markup=REGIS)
                    if s[5] == 1:
                        REGIS.add(login)
                        await bot.send_message(message.chat.id,f'Пожалуйста, войдите в аккаунт',reply_markup=REGIS)
    else:
       #если в ссылке нет id рефера
        db.add_subscriber(message.from_user.id,unique_code)

        unique_code = extract_unique_code(message.text)
        subscriptions = db.get_subscriptions()
        # отправляем всем новость
        for s in subscriptions:
            if s[1] == message.chat.id:
                if s[5] == 0:
                    REGIS.add(registration)
                    await bot.send_message(message.chat.id,f'Пожалуйста, зарегестрируйтесь в аккаунте',reply_markup=REGIS)
                if s[5] == 1:
                    REGIS.add(login)
                    await bot.send_message(message.chat.id,f'Пожалуйста, войдите в аккаунт',reply_markup=REGIS)

@dp.message_handler(content_types=['text'])
async def subscribe(message):
    if message.text =="REGISTRATION":
        await Form.LOGIN.set()
        await bot.send_message(message.chat.id,f'Введите LOGIN:')

    if message.text =="PARSE BINANCE!": 
        global id
        id = message.chat.id
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

    if message.text == "LOGIN":
        await bot.send_message(message.chat.id,f'Введите ваш логин:')
        await Form.lg.set()
    if message.text =="EXIT":
        db.up_Login(0,message.chat.id)
        REGIS = types.ReplyKeyboardMarkup(resize_keyboard=True)
        login = types.KeyboardButton(text="LOGIN")
        registration = types.KeyboardButton(text="REGISTRATION")
        REGIS.add(login,registration)
        await bot.send_message(message.chat.id,f'Возвращайтесь скорее, деньги ждать не будут 😉',reply_markup = REGIS)
  

@dp.message_handler(state = Form.LOGIN)
async def register_login(message: types.Message, state: FSMContext):
    log = message.text
    db.add_email(message.chat.id,log)  
    await bot.send_message(message.chat.id,f'Введите пароль:')  
    await Form.PASSW.set()

@dp.message_handler(state = Form.lg)
async def login(message: types.Message, state: FSMContext):
    global lg
    lg = message.text
    subscription = db.get_subscriptions()
    for s in subscription:
        if s[1] == message.chat.id:       
            if s[6] == lg:
                await bot.send_message(message.chat.id,f'Введите ваш пароль: ')
                await Form.ps.set()
            else:
                await bot.send_message(message.chat.id,f'Неверный логин')
@dp.message_handler(state = Form.ps)
async def password(message: types.Message, state: FSMContext):
    global lg
    ps = message.text
    subscription = db.get_subscriptions()
    for s in subscription:
        if s[1] == message.chat.id:
            if s[6] == lg:
                if s[7] == ps:
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

                        button_1 = types.KeyboardButton(text="PARSE BINANCE!")
                        button_2 = types.KeyboardButton(text="ELSE CRYPTOBIRGE")
                        button_3 = types.KeyboardButton(text="EXIT")
                        keyboard.add(button_1,button_2)
                        keyboard.row(button_3)
                        await bot.send_message(message.chat.id,f'Вход выполнен успешно!',reply_markup = keyboard)
                        db.up_Login(1,message.chat.id)
                        await state.finish()
                else:
                    await bot.send_message(message.chat.id,f'Неверный пароль! Выполните процедуру входа заново!')
                    await state.finish()

@dp.message_handler(state = Form.PASSW)
async def Bitcoin_payments(message: types.Message, state: FSMContext):
    passw = message.text
    db.add_passw(message.chat.id,passw) 
    await bot.send_message(message.chat.id,f'Введите ваше ФИО:')
    await Form.NAME.set()

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