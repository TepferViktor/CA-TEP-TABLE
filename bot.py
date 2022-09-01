from ast import While
from asyncio.windows_events import NULL
from email import message
from pickle import TRUE
import re
#from tkinter.messagebox import YES
import aiogram
from attr import asdict
from django.conf import settings
import config
import asyncio
import time
import logging
import os, sys
from datetime import datetime
import aioschedule
from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter
import aiogram.utils.markdown as md
from aiogram.utils.deep_linking import get_start_link
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
# Configure logging
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# инициализируем соединение с БД
db = SQLighter('db.db')

class Form(StatesGroup):
	BTCpay = State()
	CheckBTCpay = State()
	USDTpay = State()  
	CheckUSDTpay = State()
	BNBpay = State()
	CheckBNBpay = State()
	addWallet = State()
	Vivod = State()
	Nall_freez = State()
	passive = State()

number = 0
money = 0
usid = 0
stack = 0
wallet = 0
token_prise = 0.0025#za 1
token_priseUSDT = 50#za 20000 tokenov
check = TRUE
ADMIN = 685710474
def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None

@dp.message_handler(commands=['start'],state = None)
async def subscribe_from_start(message: types.Message):

	"""Создание дефолт кнопок"""
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)


	button_1 = types.KeyboardButton(text="💸Купить монету")
	button_2 = types.KeyboardButton(text="👤Профиль")
	button_3 = types.KeyboardButton(text="👥Рефка")
	button_4 = types.KeyboardButton(text="🧊Стейкинг")
	button_5 = types.KeyboardButton(text="📊Статистика")
	button_6 = types.KeyboardButton(text="⚙️Настройки")

	keyboard.add(button_2)
	keyboard.row(button_1,button_3)
	keyboard.row(button_4,button_5)
	keyboard.add(button_6)

	unique_code = extract_unique_code(message.text)
	if unique_code:
       #если есть id рефера
		if(not db.subscriber_exists(message.from_user.id)):
			# если юзера нет в базе, добавляем его
			db.add_subscriber(message.from_user.id,unique_code)
			db.ref_update(message.from_user.id, int(unique_code))
			await bot.send_message(message.chat.id,"Подписка успешно активирована", reply_markup = keyboard)

		else:
			# если он уже есть, то просто обновляем ему статус подписки
			db.update_subscription(message.from_user.id, True)
			await bot.send_message(message.chat.id,"Подписка обновлена", reply_markup = keyboard)
	else:
       #если в ссылке нет id рефера
		db.add_subscriber(message.from_user.id,unique_code)

		await bot.send_message(message.chat.id,"Подписка успешно активирована", reply_markup = keyboard)


@dp.message_handler(state = None)
async def zapisat(message):
	if message.text == "💸Купить монету":
		"""Создание инлайновой клавы"""
		markup = types.InlineKeyboardMarkup(row_width=2)

		BTC = types.InlineKeyboardButton("BTC",callback_data = 'btc')
		USDT = types.InlineKeyboardButton("USDT",callback_data = 'usdt')
		BNB = types.InlineKeyboardButton("BNB",callback_data = 'bnb')

		markup.add(BTC,USDT,BNB)
		await bot.send_message(message.chat.id,text = 'Выберите способ покупки монет', reply_markup= markup)

	if message.text =="👤Профиль":
		"""Создание дефолт кнопок"""
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		bt_0 = types.KeyboardButton(text="🔥AIRDROP")
		button_1 = types.KeyboardButton(text="💸Добавить кошелек")
		button_2 = types.KeyboardButton(text="◀️В главное меню")
		button_3 = types.KeyboardButton(text="🤑Вывод")


		subscriptions = db.get_subscriptions()
		# отправляем всем новость
		for s in subscriptions:
			if s[1] == message.chat.id:
				if s[7] == None:
					keyboard.add(bt_0)
					keyboard.add(button_2,button_1)
				if s[7] != None:
					keyboard.add(bt_0)
					keyboard.add(button_2,button_3)
				await bot.send_message(
					message.chat.id,
					f' Ваш ID в телеграм: {s[1]}\nВаш ID в системе: {s[0]}\nДоступно монет: {s[4]} ({float(s[4]*0.0025)}$)\nЗаморожено монет: {s[5]}({float(s[5]*0.0025)}$)\nКошелек: {s[7]}',
					reply_markup= keyboard
				)       
	
	if message.text == "💸Добавить кошелек":
		await Form.addWallet.set()
		await bot.send_message (message.chat.id,f'Отправьте адрес USDT trc20 кошелька для вывода')

	if message.text == "🤑Вывод":

		subscriptions = db.get_subscriptions()
		# отправляем всем новость
		for s in subscriptions:
			if s[1] == message.chat.id:
				if int(s[4]) < 4000:
					await bot.send_message (message.chat.id,f'У вас недостаточно монет для вывода')
				else:
					await Form.Vivod.set()
					await bot.send_message (message.chat.id,f'Для вывода доступно {s[4]}монет ({float(s[4]*0.0025)}$). Введите количество монет для вывода')

	if message.text =="👥Рефка":
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

		button_1 = types.KeyboardButton(text="❔Информация о структуре")
		button_2 = types.KeyboardButton(text="◀️В главное меню")
			
		keyboard.add(button_2,button_1)
		refLink = await get_start_link(payload=message.from_user.id)
		await bot.send_message(message.chat.id,f'Ваша реферальная ссылка: \n\n{refLink}',reply_markup=keyboard)

	if message.text == "❔Информация о структуре":
		i =0
		m = 0
		subscriptions = db.get_subscriptions()
		for s in subscriptions:
			if s[6] == message.chat.id:
				i = i+1
				m = m+int(s[4])+int(s[5])
				referal = db.get_subscriptions()
				for r in referal:
					if r[6] == s[1]:
						i = i+1
						m = m+int(r[4])+int(r[5])
						last = db.get_subscriptions()
						for l in last:
							if l[6] == r[1]:
								i = i+1
								m = m+int(l[4])+int(l[5])

		await bot.send_message(message.chat.id,f'Количество партнеров: {i}\n\n Количество монет: {m}({float(m)*0.0025}$)')

	if message.text =="📊Статистика":
		subscriptions = db.get_subscriptions()
		# отправляем всем новость
		for s in subscriptions:
			if int(s[1]) == message.chat.id:
				if s[5]!=0:
					await bot.send_message(
						message.chat.id,
						f'Ваш депозит: {s[5]}\n'
                    	f'Процент за 10 дней: {(int(s[5])/100)*int(s[9])}\n'
                    	f'Процент в USD: {((int(s[5])/100)*int(s[9]))*0.0025} $ '
					)  
				else:
					await bot.send_message(
						message.chat.id,
						f'Ваш депозит: {s[5]}\n'
					)					
	if message.text =="⚙️Настройки":
		Setting = types.ReplyKeyboardMarkup(resize_keyboard=True)


		bt_1 = types.KeyboardButton(text="❔FAQ")
		bt_2 = types.KeyboardButton(text="🆘Поддержка")
		bt_3 = types.KeyboardButton(text="🔥Проект")
		bt_4 = types.KeyboardButton(text="🇬🇧Изменить язык")
		bt_5 = types.KeyboardButton(text="◀️В главное меню")
       	

		Setting.row(bt_1,bt_2)
		Setting.row(bt_3,bt_4)
		Setting.add(bt_5)		
		await bot.send_message(message.chat.id,text = 'Вы находитесь в настройках, нажмите на кнопку \"В главное меню\" что бы вернуться назад',reply_markup= Setting)

	if message.text =="❔FAQ":
		await bot.send_message(message.chat.id,text = 'Сообщение с ответами на частозадаваемые вопросы')

	if message.text =="🆘Поддержка":
		await bot.send_message(message.chat.id,text = 'Если у вас возникли какие-нибудь трудности - обращайтесь к @vladiskoobilo')

	if message.text =="🇬🇧Изменить язык":
		await bot.send_message(message.chat.id,f'Недоступно в вашем регионе')
	
	if message.text =="🔥Проект":
		await bot.send_message(message.chat.id,f'Проект:\n\nфинансовый блок экосистемы NFT маркетплейса нового поколения' 
											f'с сообственным токеном, ликвидность которого обеспечена стейкингом и резервным фондом.' 
											f'Мы преследуем цель распостранения нашего токена и приобретения комьюнити'
											f'для дальнейшего продвижения на ТОП-100 Биржи. Для более подробного изучения токеномики экосистемы'
											f' обратитесь к White Paper.'
											f'ТОКЕНЫ:\n\n'
											f'Проект имеет ограниченную эмиссию в 100млрд. токенов, 10%(10млрд.) из которых составят'
											f'резервный фонд создателей. Часть токенов резервного фонда в размере 10%(1млрд.) сформирует'
											f'начальный стейк.'
											f'На AirDrop придется 2.5%(2.5млрд.), так же на маркетинг придется 12.5%(12.5млрд.) токенов. '
											f'Еще 10%(10млрд.) будет направлено в другие блоки экосистемы, а так же 10%(10млрд.) принадлежать '
											f'команде разработчиков. '
											f'СТЭЙК:\n\n'
											f'Оставшиеся 50%(50млрд.) будут распределены между 3-мя этапами стэйкинга в равных долях между каждым этапом:\n\n'
											f'1-ый этап самый высокодоходный и выгодный стейкинг, условия таковы, что пользователь сможет заблокировать '
											f'монеты которыми он владеет на срок от 100 дней с доходностью от 0.87% в сутки\n\n'
											f'2-ой этап менее выгодный стейкинг, но будет возможность заблокировать монеты на срок от 50 дней '
											f'с доходностью от 0.435% в сутки'
											f'3-ий этап принесет пользователям возможность блокировать свои монеты на срок от 30 дней с доходностью от 0.217% в сутки'
											
											)
											
	if message.text =="🔥AIRDROP":
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

		button_1 = types.KeyboardButton(text="✅Подписался")
		button_2 = types.KeyboardButton(text="◀️В главное меню")

		keyboard.add(button_1)
		keyboard.add(button_2)		
		"""Создание инлайновой клавы"""
		markup = types.InlineKeyboardMarkup(row_width=2)

		Y = types.InlineKeyboardButton("Telegram",url="https://t.me/NFTairDro")
		N = types.InlineKeyboardButton("Instagram",url="https://t.me/NFTairDro")

		markup.add(Y,N)
		sub = db.get_subscriptions()
		for s in sub:
			if s[1] == message.chat.id:
				if s[10] == 0:
					await bot.send_message(message.chat.id,f'Вы начали процедуру прохождения AIRDROP, выполните представленые ниже условия что бы получить вознаграждение',reply_markup=keyboard)
					await bot.send_message(message.chat.id,f'Подпишитесь на наш телеграм канал и инстаграм',reply_markup=markup)
				else:
					await bot.send_message(message.chat.id,f'Вы уже прошли AIRDROP')

	if message.text == "◀️В главное меню":
		"""Создание дефолт кнопок"""
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

		button_1 = types.KeyboardButton(text="💸Купить монету")
		button_2 = types.KeyboardButton(text="👤Профиль")
		button_3 = types.KeyboardButton(text="👥Рефка")
		button_4 = types.KeyboardButton(text="🧊Стейкинг")
		button_5 = types.KeyboardButton(text="📊Статистика")
		button_6 = types.KeyboardButton(text="⚙️Настройки")

		keyboard.add(button_2)
		keyboard.row(button_1,button_3)
		keyboard.row(button_4,button_5)
		keyboard.add(button_6)

		await bot.send_message(message.chat.id,text = 'Вы вернулись в главное меню!', reply_markup=keyboard)

	if message.text =="🧊Стейкинг":
		subscriptions = db.get_subscriptions()
		"""Создание инлайновой клавы"""
		markup = types.InlineKeyboardMarkup(row_width=2)

		Y = types.InlineKeyboardButton("✅Да",callback_data = 'allstatic')
		N = types.InlineKeyboardButton("⚠️Заморозить часть",callback_data = 'Nallstatic')

		markup.add(Y,N)
		for s in subscriptions:
			if s[1] == message.chat.id:
				if s[4]<20000:
					await bot.send_message(s[1],f'У вас недостаточно монет для заморозки, минимальное количество для стейкинга - 20000')
				else:
					await bot.send_message(
						message.chat.id,
						f'Количество монет доступное для заморозки: {s[4]}\n\nЗаморозить все ?',
						reply_markup= markup
					)

	if message.text == "Отправить пассив":
		await Form.passive.set()
		await bot.send_message(config.ADMIN, f'Введите процент который начислить всем')

	if message.text =="✅Подписался":
		mon = 0
		user_channel_status = await bot.get_chat_member(chat_id='@NFTairDro', user_id=message.from_user.id)
		user_channel_status = re.findall(r"\w*", str(user_channel_status))
		try:
			sub = db.get_subscriptions()
			for s in sub:
				if s[1] == message.chat.id:
					if s[10]==0:
						if user_channel_status[70] != 'left':
							await bot.send_message(message.chat.id,f'Поздравляем с выполнением условий! На ваш баланс начислено 10$ в эвиваленте 4000 монет')
							sub = db.get_subscriptions()
							for s in sub:
								if s[1] == message.chat.id:
									mon = float(s[4])+4000
									db.token_update(message.chat.id,mon)
									db.up_air(s[1],1)
						else:
							await bot.send_message(message.chat.id,f'Вы подписались не на все каналы')
							#Условие для тех, кто не подписан
					else:
						await bot.send_message(message.chat.id,f'Вы уже забрали вознаграждение')
		except:
			sub = db.get_subscriptions()
			for s in sub:
				if s[1] == message.chat.id:
					if s[10]==0:
						if user_channel_status[60] != 'left':
							await bot.send_message(message.chat.id,f'Поздравляем с выполнением условий! На ваш баланс начислено 10$ в эвиваленте 4000 монет')
							sub = db.get_subscriptions()
							for s in sub:
								if s[1] == message.chat.id:
									mon = float(s[4])+4000
									db.token_update(message.chat.id,mon)
									db.up_air(s[1],1)
						else:
							await bot.send_message(message.from_user.id, f'Вы подписались не на все каналы')
							#Условие для тех, кто не подписан
					else:
						await bot.send_message(message.chat.id,f'Вы уже забрали вознаграждение')
	if message.text =="*#Adm1nn":
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

		button_1 = types.KeyboardButton(text="!№Отправить пассив")

		keyboard.add(button_1)

		await bot.send_message(message.chat.id,f'Поздравляю, вас назначили админом!', reply_markup=keyboard)
	if message.text == "Отправил":
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

		button_1 = types.KeyboardButton(text="💸Купить монету")
		button_2 = types.KeyboardButton(text="👤Профиль")
		button_3 = types.KeyboardButton(text="👥Рефка")
		button_4 = types.KeyboardButton(text="🧊Стейкинг")
		button_5 = types.KeyboardButton(text="📊Статистика")
		button_6 = types.KeyboardButton(text="⚙️Настройки")

		keyboard.add(button_2)
		keyboard.row(button_1,button_3)
		keyboard.row(button_4,button_5)
		keyboard.add(button_6)

		await bot.send_message(message.chat.id,f'Ожидайте поступления средств!',reply_markup=keyboard)
async def up_balance(wait):
	while True:
		subscribtions = db.get_subscriptions()
		for s in subscribtions:
			id = s[1]
			sub = db.get_subscriptions()
			for s in sub:
				if s[6] == id:
					if int(s[8])!= 1:
						if int(s[4]) == 0:
							pass
						else:
							await bot.send_message(id,f'За приглашенного партнера из первой линии вам начислено: {(float(s[4])/100)*7} ({((float(s[4])/100)*7)*0.0025}$)')
							db.update_Vozn(s[1], 1)
							money = (float(s[4])/100)*7
							up = db.get_subscriptions()
							for u in up:
								if u[1] == id:
									money = float(u[4])+money
									db.token_update(u[1],money)

			for s in sub:
				if s[6] == id:
					for sec in sub:
						if sec[6] == s[1]:
							if int(sec[8]) != 1:
								if int(sec[4]) == 0:
									pass
								else:
									await bot.send_message(id,f'За приглашенного партнера во второй линии вам начислено: {(float(sec[4])/100)*4} ({((float(sec[4])/100)*4)*0.0025}$)')
									db.update_Vozn(sec[1],1)
									money = (float(sec[4]/100)*4)
									upd = db.get_subscriptions()
									for u in upd:
										if u[1] == id:
											money = float(u[4])+money
											db.token_update(id,money)	

			for s in sub:
				if s[6] == id:
					for sec in sub:
						if sec[6] == s[1]:
							for th in sub:
								if th[6] == sec[1]:
									if int(th[8])!=1:
										if int(th[4]) == 0:
											pass
										else:
											await bot.send_message(id,f'За приглашенного партнера в третьей линии вам начислено: {float(th[4]/100)*1} ({(float(th[4]/100)*1*0.0025)}$)')
											db.update_Vozn(th[1],1)
											money = (float(th[4]/100)*1)
											upd = db.get_subscriptions()
											for u in upd:
												if u[1] == id:
													money = float(u[4])+money
													db.token_update(id,money)
		await asyncio.sleep(wait)

@dp.callback_query_handler()
async def approve(call) :
	global number
	global usid
	global money
	global stack

	if call.data == 'btc' :
		await Form.BTCpay.set()
		await bot.send_message(call.message.chat.id,text = 'Введите количество монет которое хотите приобрести(минимальная сумма покупки 20000 монет или 50$)\n\n После того как админ одобрит вашу заявку на покупку вам придет сообщение с адресом для оплаты')
       
	if call.data == 'yBTC' :

		"""Создание инлайновой клавы"""
		markup = types.InlineKeyboardMarkup(row_width=2)

		Y = types.InlineKeyboardButton("✅Дошли",callback_data = 'ypay')
		N = types.InlineKeyboardButton("⚠️Не дошли",callback_data = 'npay')

		markup.add(Y,N)

		await bot.send_message(config.ADMIN,f'На кошелек BTC было отправлено {money}$, средства зачислены? ', reply_markup=markup)
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

		button_1 = types.KeyboardButton(text="Отправил")

		keyboard.add(button_1)
		await bot.send_message(usid,f'Ваша заявка на покупку монет одобрена!Переведите {money}$ на адресс:\n\nbc1qtgn77auks42zknf8gtm7rr0c4pqvfrtlhkgxwt')
		
		await bot.send_message(usid,f'Нажмите на кнопку \"ОТПРАВИЛ\" после отправки', reply_markup= keyboard)


	if call.data == 'nBTC' :
		await bot.send_message(usid,text = 'К сожалению ваша заявка не одобрена, уточните причину у нашей технической поддержки')

	if call.data == 'usdt' :
		await Form.USDTpay.set()
		await bot.send_message(call.message.chat.id,text = 'Введите количество монет которое хотите приобрести(минимальная сумаа покупки 20000 монет или 50$)\n\n После того как админ одобрит вашу заявку на покупку вам придет сообщение с адресом для оплаты')
       
	if call.data == 'yUSDT' :
		
		"""Создание инлайновой клавы"""
		markup = types.InlineKeyboardMarkup(row_width=2)

		Y = types.InlineKeyboardButton("✅Дошли",callback_data = 'ypay')
		N = types.InlineKeyboardButton("⚠️Не дошли",callback_data = 'npay')

		markup.add(Y,N)

		await bot.send_message(config.ADMIN,f'На кошелек BTC было отправлено {money}$, средства зачислены? ', reply_markup=markup)
		
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

		button_1 = types.KeyboardButton(text="Отправил")

		keyboard.add(button_1)

		await bot.send_message(usid,f'Ваша заявка на покупку монет одобрена! Переведите {money}$ на адресс:\n\nTDFFzjL1AuVR4XnSjPgAvj9frLEPwHAq9r')

		await bot.send_message(usid,f'Нажмите на кнопку \"ОТПРАВИЛ\" после отправки', reply_markup= keyboard)
		
	if call.data == 'nUSDT' :
		await bot.send_message(usid,text = 'К сожалению ваша заявка не одобрена, уточните причину у нашей технической поддержки')

	if call.data == 'bnb' :
		await Form.BNBpay.set()
		await bot.send_message(call.message.chat.id,text = 'Введите количество монет которое хотите приобрести(минимальная сумаа покупки 20000 монет или 50$)\n\n После того как админ одобрит вашу заявку на покупку вам придет сообщение с адресом для оплаты')
       
	if call.data == 'yBNB' :
		
		"""Создание инлайновой клавы"""
		markup = types.InlineKeyboardMarkup(row_width=2)

		Y = types.InlineKeyboardButton("✅Дошли",callback_data = 'ypay')
		N = types.InlineKeyboardButton("⚠️Не дошли",callback_data = 'npay')

		markup.add(Y,N)

		await bot.send_message(config.ADMIN,f'На кошелек BTC было отправлено {money}$, средства зачислены? ', reply_markup=markup)
		
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

		button_1 = types.KeyboardButton(text="Отправил")

		keyboard.add(button_1)
		await bot.send_message(usid,f'Ваша заявка на покупку монет одобрена! переведите {money}$ на адресс:\n\nbnb13cn9ghfgur4s34mcdk25t36jxqjt2aw3tgefxz')
		await bot.send_message(usid,f'Нажмите на кнопку \"ОТПРАВИЛ\" после отправки', reply_markup= keyboard)
		
	if call.data == 'nBNB' :
		await bot.send_message(usid,text = 'К сожалению ваша заявка не одобрена, уточните причину у нашей технической поддержки')


	if call.data == 'ypay' :
		"""Создание дефолт кнопок"""
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

		button_1 = types.KeyboardButton(text="💸Купить монету")
		button_2 = types.KeyboardButton(text="👤Профиль")
		button_3 = types.KeyboardButton(text="👥Рефка")
		button_4 = types.KeyboardButton(text="🧊Стейкинг")
		button_5 = types.KeyboardButton(text="📊Статистика")
		button_6 = types.KeyboardButton(text="⚙️Настройки")

		keyboard.add(button_2)
		keyboard.row(button_1,button_3)
		keyboard.row(button_4,button_5)
		keyboard.add(button_6)
		subscriptions = db.get_subscriptions()
		for s in subscriptions:
			if s[1] == usid:
				number = s[4]
		await bot.send_message(usid,text = 'Перевод подтвержден! Наша команда поздравляет вас с покупкой токена! Можете проверить их количество в профиле!',reply_markup=keyboard)
        #тут добавить функцию для занесения количества монет в бд 
		money = float(money)/0.0025
		money = int(money) + number
		db.token_update(usid,money)

	if call.data == 'npay' :
		"""Создание дефолт кнопок"""
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

		button_1 = types.KeyboardButton(text="💸Купить монету")
		button_2 = types.KeyboardButton(text="👤Профиль")
		button_3 = types.KeyboardButton(text="👥Рефка")
		button_4 = types.KeyboardButton(text="🧊Стейкинг")
		button_5 = types.KeyboardButton(text="📊Статистика")
		button_6 = types.KeyboardButton(text="⚙️Настройки")
		keyboard.add(button_2)
		keyboard.row(button_1,button_3)
		keyboard.row(button_4,button_5)
		keyboard.add(button_6)
		await bot.send_message(usid,text = 'К сожалению ваши средства не дошли! обратитесь в службу поддержки для уточнения ситуации',reply_markup=keyboard)


	if call.data == 'allstatic' :
		subscriptions = db.get_subscriptions()
		for s in subscriptions:
			if s[1] == call.message.chat.id:
				number = s[4]
				stack = s[5]
		stack = number+stack
		number = 0
		db.token_update(call.message.chat.id, number)
		db.stack_update(call.message.chat.id, stack)
		await bot.send_message(call.message.chat.id,f'Все доступные вам монеты переведены в стейкинг! Поздравляем!')

	if call.data == 'Nallstatic' :
		usid = call.message.chat.id
		await Form.Nall_freez.set()
		await bot.send_message(call.message.chat.id,f'Отпарвьте количество монет которое которые хотите заморозить(минимум 20000 токенов) ')

	if call.data == 'yViv' :
		subscriptions = db.get_subscriptions()

		for s in subscriptions:
			if s[1] == usid:
				number = s[4]
		money = number - int(money)
		db.token_update(usid,money)
		await bot.send_message(usid,text = 'Средства были отправлены на ваш кошелек! Ожидайте поступления!')

	if call.data == 'nViv' :
		subscriptions = db.get_subscriptions()

		for s in subscriptions:
			if s[1] == usid:
				await bot.send_message(usid,text = 'В заявке на вывод было отказано, уточните причину у поддержки')


		     
"""Создание заявки на покупку в битке"""
@dp.message_handler(state = Form.BTCpay)
async def Bitcoin_payments(message: types.Message, state: FSMContext):
	global money
	global usid
	money = message.text
	usid = message.chat.id
	if float(money)<20000:
		await bot.send_message(message.chat.id, f'Сумма токенов для покупки меньше минимальной. Составьте новую заявку с количеством токенов от 20000')
		await state.finish()
	if float(money)>=20000:
		"""Создание инлайновой клавы"""
		markup = types.InlineKeyboardMarkup(row_width=2)

		Y = types.InlineKeyboardButton("✅Одобрить",callback_data = 'yBTC')
		N = types.InlineKeyboardButton("⚠️Запретить",callback_data = 'nBTC')

		markup.add(Y,N)
		money = float(money)*0.0025
		await state.finish()
		await bot.send_message(config.ADMIN,f'ЗАЯВКА НА ПОКУПКУ\n\nФИО покупателя: ФИО из БД\n\nВалюта оплаты: BTC\n\nСумма к оплате: {money}$', reply_markup=markup)
		
@dp.message_handler(state = Form.USDTpay)
async def USDT_payments(message: types.Message, state: FSMContext):
	global money
	global usid
	money = message.text
	usid = message.chat.id
	if float(money)<20000:
		await bot.send_message(message.chat.id, f'Сумма токенов для покупки меньше	 минимальной. Составьте новую заявку с количеством токенов от 20000')
		await state.finish
	if float(money)>=20000:
		"""Создание инлайновой клавы"""
		markup = types.InlineKeyboardMarkup(row_width=2)

		Y = types.InlineKeyboardButton("✅Одобрить",callback_data = 'yUSDT')
		N = types.InlineKeyboardButton("⚠️Запретить",callback_data = 'nUSDT')

		markup.add(Y,N)
		money = float(money)*0.0025
		await bot.send_message(config.ADMIN,f'ЗАЯВКА НА ПОКУПКУ\n\nФИО покупателя: ФИО из БД\n\nВалюта оплаты: USDT\n\nСумма к оплате: {money}$', reply_markup=markup)
		await state.finish()

"""Подтверждение перевода в USDT"""
@dp.message_handler(state = Form.CheckUSDTpay)
async def USDT_payments(message: types.Message, state: FSMContext):
	global money
	global usid

	"""Создание инлайновой клавы"""
	markup = types.InlineKeyboardMarkup(row_width=2)

	Y = types.InlineKeyboardButton("✅Дошли",callback_data = 'ypay')
	N = types.InlineKeyboardButton("⚠️Не дошли",callback_data = 'npay')

	markup.add(Y,N)

	await bot.send_message(config.ADMIN,f'На кошелек USDT было отправлено {money}$, средства зачислены? ', reply_markup=markup)
	await state.finish()

@dp.message_handler(state = Form.BNBpay)
async def BNB_payments(message: types.Message, state: FSMContext):
	global money
	global usid
	money = message.text
	usid = message.chat.id
	if float(money)<20000:
		await bot.send_message(message.chat.id, f'Сумма токенов для покупки меньше минимальной. Составьте новую заявку с количеством токенов от 20000')
		await state.finish
	if float(money)>=20000:
		"""Создание инлайновой клавы"""
		markup = types.InlineKeyboardMarkup(row_width=2)

		Y = types.InlineKeyboardButton("✅Одобрить",callback_data = 'yBNB')
		N = types.InlineKeyboardButton("⚠️Запретить",callback_data = 'nBNB')

		markup.add(Y,N)
		money = float(money)*0.0025
		await bot.send_message(config.ADMIN,f'ЗАЯВКА НА ПОКУПКУ\n\nФИО покупателя: ФИО из БД\n\nВалюта оплаты: BNB\n\nСумма к оплате: {money}$', reply_markup=markup)
		await state.finish()

"""Подтверждение перевода в BNB"""
@dp.message_handler(state = Form.CheckBNBpay)
async def BNB_payments(message: types.Message, state: FSMContext):
	global money
	global usid

	"""Создание инлайновой клавы"""
	markup = types.InlineKeyboardMarkup(row_width=2)

	Y = types.InlineKeyboardButton("✅Дошли",callback_data = 'ypay')
	N = types.InlineKeyboardButton("⚠️Не дошли",callback_data = 'npay')

	markup.add(Y,N)

	await bot.send_message(config.ADMIN,f'На кошелек BNB было отправлено {money}$, средства зачислены? ', reply_markup=markup)
	await state.finish()

"""Добавление USDT trc20 кошелька"""
@dp.message_handler(state = Form.addWallet)
async def BNB_payments(message: types.Message, state: FSMContext):
	global wallet
	wallet = message.text
	db.add_wallet(message.from_user.id, wallet)
	await bot.send_message(message.chat.id,f'Кошелек для вывода средств добавлен!')

	await state.finish()

"""Вывод монет"""
@dp.message_handler(state = Form.Vivod)
async def BNB_payments(message: types.Message, state: FSMContext):
	global money
	global usid
	money = message.text
	usid = message.chat.id
	if int(money)<4000:
		await bot.send_message(usid,f'Вывод доступен от 4000 монет (10$), введите корректную сумму')
		await Form.Vivod.set()
	else:
		await bot.send_message(usid,f'Заявка на вывод создана, как только админ одобрит заявку вам придет уведомление!')

		"""Создание инлайновой клавы"""
		markup = types.InlineKeyboardMarkup(row_width=2)

		Y = types.InlineKeyboardButton("✅Одобрена",callback_data = 'yViv')
		N = types.InlineKeyboardButton("⚠️Отказано",callback_data = 'nViv')

		markup.add(Y,N)
		subscriptions = db.get_subscriptions()
		for s in subscriptions:
			if s[1] == usid:
				wallet = s[7]
	#Ввести id админа
		await bot.send_message(config.ADMIN,f'ЗАЯВКА НА ВЫВОД:\nКоличество монет для вывода:{money}\nКошелек для отправки:\n\n {wallet}',reply_markup=markup)

		await state.finish()


@dp.message_handler(state = Form.Nall_freez)
async def some_freez(message: types.Message, state: FSMContext):
	global money_freez
	global usid
	money_freez = message.text
	st_d = 0
	subscriptions = db.get_subscriptions()
	if int(money_freez) < 20000:
		await bot.send_message(message.chat.id,f'Вы ввели некоректную сумму, создайте новую зайвку на перевод монет в стейкинг(минимальное количество монет для заморозки 20000)')
	else:
		for s in subscriptions:
			if s[1] == usid:
				m = s[4]
				st = s[5]
				st_d = int(st)+ int(money_freez)
				money_fre = int(m) - int(money_freez)
				db.token_update(s[1],money_fre)
				db.stack_update(s[1],st_d)
		await bot.send_message(usid,f'Поздравляем! Монеты заморожены!')

	await state.finish()

@dp.message_handler(state = Form.passive)
async def some_freez(message: types.Message, state: FSMContext):
	pr = message.text
	sub = db.get_subscriptions()
	for s in sub:
		if float(s[5]) == 0:
			pass
		else:
			await bot.send_message(s[1],f'Вам начислен пассивный доход в размере {float(s[5])/100 * float(pr)}')
			money = s[4]+float(s[5])/100*float(pr)
			db.token_update(s[1], money)
			db.set_pass(s[1],int(pr))
	await state.finish()


# запускаем лонг поллинг
if __name__ == '__main__':
	try:
		loop = asyncio.get_event_loop()
		loop.create_task(up_balance(10))
		executor.start_polling(dp, skip_updates=True)
	except:
		aiogram.utils.exceptions.BotBlocked	