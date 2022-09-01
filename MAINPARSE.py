from email import message
from USDT import parse
from BTC import parse_BTC
from ETH import parse_ETH
from BUSD import parse_BUSD
from BNB import parse_BNB
from SHIB import parse_SHIB
from MARKET import market_parse
from unicodedata import name
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

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from sqlighter import SQLighter
from aiogram.utils.deep_linking import get_start_link
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
#from main import id
bot = Bot(token=config.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)

@dp.message_handler(content_types=['text'])
def main_parse():
    parse()
    bot.send_message(id,f'20%...')
    parse_BTC()    
    parse_ETH()
    bot.send_message(id,f'40%...')
    parse_BUSD()
    parse_BNB()
    bot.send_message(id,f'60%...')
    parse_SHIB()
    bot.send_message(id,f'80%...')
    market_parse()
    bot.send_message(id,f'100%')
def main():
    main_parse()

if __name__ == "__main__":
    main()