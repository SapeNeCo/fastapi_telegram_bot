import aiosqlite
from telebot import types
from conflib import Configs, Config
import random 
from random import random, randrange, randint
import os
import json
import aiofiles
import aiofiles.os

messbutton = types.InlineKeyboardMarkup()

barsbutton = types.ReplyKeyboardMarkup()

async def init_bd():
    async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id   BIGINT,
            id        BIGINT,
            mess_id   BIGINT,
            tries     INT,
            stage_api TEXT,
            api       TEXT
        )""")
        await db.commit()

all_buy = 'У вас максимальный тарифный план'

buttons = {
    'api_menu':       types.InlineKeyboardButton(text='Создать API', callback_data='api_menu'),
    'profile':        types.InlineKeyboardButton(text='Профиль', callback_data='profile'),
    'help':           types.InlineKeyboardButton(text='Как работает бот', url='https://t.me/fastapibotguide'),
    'api_create':     types.InlineKeyboardButton(text='Создать', callback_data='api_create'),
    'create_get':     types.InlineKeyboardButton(text='GET', callback_data='create_get'),
    'create_post':    types.InlineKeyboardButton(text='POST', callback_data='create_post'),
    'create_put':     types.InlineKeyboardButton(text='PUT', callback_data='create_put'),
    'create_delete':  types.InlineKeyboardButton(text='DELETE', callback_data='create_delete'),
    'create_cancel':  types.InlineKeyboardButton(text='Отмена', callback_data='create_cancel'),
    'delete_method':  types.InlineKeyboardButton(text='Удалить метод', callback_data='delete_method'),
    'add_method':     types.InlineKeyboardButton(text='Сделать ещё один метод', callback_data='add_method'),
    'finish_api':     types.InlineKeyboardButton(text='Закончить создание API', callback_data='finish_api'),
    'clear_api':      types.InlineKeyboardButton(text='Очистить всю API', callback_data='clear_api'),
    'api_in_file':    types.InlineKeyboardButton(text='В файле .py', callback_data='api_in_file'),
    'api_in_message': types.InlineKeyboardButton(text='В сообщении', callback_data='api_in_message'),
    'buy_menu':       types.InlineKeyboardButton(text='Улучшить подписку', callback_data='buy_menu'),
    'buy':            types.InlineKeyboardButton(text='Заплатить 1 XTR', pay=True),
    'menu':           types.InlineKeyboardButton(text='Главное меню', callback_data='start')
}

messages = {
    'hello':           'Здравствуйте!\nПриветствую вас в боте для удобного создания API для вашего проекта!\n\nДанный бот упрощает создание API, используя модуль Python FastAPI.\n\nДля большего знакомства с нашим ботом напишите команду /help, в которой подробней указана работа данного бота.',
    'hello_client':    'Главное меню.\n\nЧто вас интересует?',
    'api_menu':        'Создание API.\n\nЗдесь вы можете начать создавать вашу API.\nДля начала создания нажмите кнопку "Создать".',
    'api_create':      'Выберите метод:',
    'create_get':      'Создание метода GET\n\nДля начала укажите тег, по которому после вашего адреса сайта/сервера будет срабатывать этот запрос, например "/", "/get_value"',
    'create_post':     'Создание метода POST\n\nДля начала укажите тег, по которому после вашего адреса сайта/сервера будет срабатывать этот запрос, например "/", "/post_value"',
    'create_put':      'Создание метода PUT\n\nДля начала укажите тег, по которому после вашего адреса сайта/сервера будет срабатывать этот запрос, например "/", "/put_value"',
    'create_delete':   'Создание метода DELETE\n\nДля начала укажите тег, по которому после вашего адреса сайта/сервера будет срабатывать этот запрос, например "/", "/delete_value"',
    'name_func':       'Укажите имя функции, которая будет использоваться для определения действий, что нужно делать коду при вызове выбранного метода.',
    'return':          'Укажите возвращаемое значение (переменная, класс, json список и т.д.), которое должно вернуться при вызове метода.',
    'arg_count':       'Укажите количество аргументов, которые принимает функция (может быть 0, если функция не принимает аргументы).',
    'argN':            'Укажите аргумент в формате "тип_данных название".',
    'check_need':      'Нужно ли добавлять проверку какого-то аргумента в массиве, списке или классе? (Ответ Да/Нет)',
    'check_item_sum':  'Укажите название аргумента для проверки, название структуры, в которой нужно проверять наличие аргумента, и возвращаемое значение, если аргумент находится в структуре через пробел в формате "название_аргумента название_стуктуры возвращаемое значение"',
    'help':            'Чтобы начать создавать api, напиши мне:\n/create_api\nЧтобы получить информацию по работе бота, перейди по этой ссылке: https://t.me/fastapibotguide',
    'resend':          '❓┃ Я тебя, увы, не понимаю. \nПроверьте написание команды/аргуметов. Или напишите /help.',
    'premium_offer':   'Вы достигли лимита на создание методов. Пожалуйста, приобретите премиум версию для создания большего количества методов.'
}

# Создание папки data, если она не существует
if not os.path.exists('data'):
    os.makedirs('data')

# Асинхронные функции для работы с JSON файлами
async def create_json_file(filename, data):
    async with aiofiles.open(f'data/{filename}', 'w') as f:
        await f.write(json.dumps(data, indent=4))

async def read_json_file(filename):
    async with aiofiles.open(f'data/{filename}', 'r') as f:
        contents = await f.read()
        return json.loads(contents)

async def update_json_file(filename, data):
    async with aiofiles.open(f'data/{filename}', 'w') as f:
        await f.write(json.dumps(data, indent=4))

async def delete_json_file(filename):
    await aiofiles.os.remove(f'data/{filename}')

#Меню оплаты
async def buy(bot, message):
    messbutton = types.InlineKeyboardMarkup()
    messbutton.add(buttons['buy'])
    prices = [types.LabeledPrice(label="XTR", amount=1)]
    await bot.send_invoice(message.chat.id, "Улучший подписку", "Стоимость улучшения подписки: 1 звезда!", "subscribe_payload", "", "XTR", prices, reply_markup=messbutton)

#Меню встречи
async def main_menu(bot, message):
    messbutton = types.InlineKeyboardMarkup()
    message_local = messages['hello']
    messbutton.add(buttons['api_menu'])
    messbutton.add(buttons['profile'])
    messbutton.add(buttons['help'])
    await bot.send_message(message.chat.id, message_local,  reply_markup = messbutton, parse_mode="Markdown")

#Меню встречи через изменение последнего сообщения
async def main_menu_edit(bot, message, last=False): 
    messbutton = types.InlineKeyboardMarkup()
    message_local = messages['hello_client']
    messbutton.add(buttons['api_menu'])
    messbutton.add(buttons['profile'])
    messbutton.add(buttons['help'])
    if last:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=int(await get_value_from_bd("""mess_id""", message.chat.id)), text=message_local, parse_mode="Markdown",  reply_markup = messbutton)
    else:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_local, parse_mode="Markdown",  reply_markup = messbutton)

#Изменение сообщения
async def edit_message(bot, message, text, input_buttons = [], last=False):
    if input_buttons != []:
        messbutton = types.InlineKeyboardMarkup()
        for button in input_buttons:
            messbutton.add(buttons[button])
        if last:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=int(await get_value_from_bd("""mess_id""", message.chat.id)), text=text, reply_markup=messbutton)
        else:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=messbutton)
    else:
        if last:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=int(await get_value_from_bd("""mess_id""", message.chat.id)), text=text)
        else:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text)

async def edit_message_profile(bot, message):
    messbutton = types.InlineKeyboardMarkup()
    text = ''
    tries = int(await get_value_from_bd("""tries""", message.chat.id))
    if tries >= 0:
        text = f'Ваш профиль:\n\nУровень подписки: base\n\nОсталось методов: {tries}'
        messbutton.add(buttons['buy_menu'])
    else:
        text = f'Ваш профиль:\n\nУровень подписки: plus'
    messbutton.add(buttons['menu'])
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=messbutton)

#Отправка сообщения
async def send_message(bot, message, text, input_buttons = []):
    if input_buttons != []:
        messbutton = types.InlineKeyboardMarkup()
        for button in input_buttons:
            messbutton.add(buttons[button])
        await bot.send_message(message.chat.id, text, reply_markup=messbutton)
    else:
        await bot.send_message(message.chat.id, text)

async def api_work(bot, message, stage, value="", name=""):
    user_id = message.from_user.id
    chat_id = message.chat.id
    json_filename = await get_value_from_bd("""api""", chat_id)
    
    async def update_json(data):
        await update_json_file(json_filename, data)
    
    async def read_json():
        return await read_json_file(json_filename)

    data = await read_json()
    current_method_index = data.get("current_method_index", 0)
    current_method = f"method_{current_method_index}"

    match stage:
        case "none":
            await set_value_in_bd("""stage_api""", stage, chat_id)
        case "GET" | "POST" | "PUT" | "DELETE":
            await set_value_in_bd("""stage_api""", stage, chat_id)
            current_method_index += 1
            current_method = f"method_{current_method_index}"
            data["current_method_index"] = current_method_index
            data[current_method] = {"method": stage}
            await update_json(data)
        case "tag":
            await set_value_in_bd("""stage_api""", stage, chat_id)
            data[current_method]["tag"] = name
            await update_json(data)
        case "name_func":
            await set_value_in_bd("""stage_api""", stage, chat_id)
            data[current_method]["name_func"] = value
            await update_json(data)
        case "return":
            await set_value_in_bd("""stage_api""", stage, chat_id)
            data[current_method]["return"] = value
            await update_json(data)
        case "arg_count":
            await set_value_in_bd("""stage_api""", stage, chat_id)
            data[current_method]["arg_count"] = int(value)
            data[current_method]["args"] = []
            await update_json(data)
        case "argN":
            data[current_method]["args"].append(value)
            if len(data[current_method]["args"]) < data[current_method]["arg_count"]:
                await set_value_in_bd("""stage_api""", "argN", chat_id)
            else:
                await set_value_in_bd("""stage_api""", "check_need", chat_id)
            await update_json(data)
        case "check_need":
            if value.lower() == "да":
                data[current_method]["check_need"] = True
                await set_value_in_bd("""stage_api""", "check_item_sum", chat_id)
            else:
                await api_work(bot, message, "none")
            await update_json(data)
        case "check_item_sum":
            if data[current_method].get("check_need"):
                data[current_method]["check_item_sum"] = value
            await api_work(bot, message, "none")
            await update_json(data)
        case _:
            print("Invalid stage provided")

async def delete_method(bot, message):
    chat_id = message.chat.id
    data = await read_json_file(await get_value_from_bd("""api""", chat_id))
    current_method_index = data.get("current_method_index", 0)
    current_method = f"method_{current_method_index}"
    if current_method in data:
        del data[current_method]
        data["current_method_index"] -= 1
        await update_json_file(await get_value_from_bd("""api""", chat_id), data)
    await set_value_in_bd("""stage_api""", "none", chat_id)
    await edit_message(bot, message, 'Метод удалён.\n\nВыберите метод:', input_buttons=['create_get', 'create_post', 'create_put', 'create_delete', 'menu'], last=True)

async def add_method(bot, message):
    chat_id = message.chat.id
    data = await read_json_file(await get_value_from_bd("""api""", chat_id))
    current_method_index = data.get("current_method_index", 0)
    tries = int(await get_value_from_bd("""tries""", chat_id))
    await set_value_in_bd("""stage_api""", "none", chat_id)
    if tries != -1 and current_method_index >= tries:
        await edit_message(bot, message, messages['premium_offer'], input_buttons=['buy_menu', 'menu'], last=True)
    else:
        await edit_message(bot, message, 'Выберите метод:', input_buttons=['create_get', 'create_post', 'create_put', 'create_delete', 'menu'], last=True)

async def finish_api(bot, message):
    chat_id = message.chat.id
    data = await read_json_file(await get_value_from_bd("""api""", chat_id))
    current_method_index = data.get("current_method_index", 0)
    tries = int(await get_value_from_bd("""tries""", chat_id))
    await set_value_in_bd("""stage_api""", "none", chat_id)
    if tries != -1:
        tries -= current_method_index
        await set_value_in_bd("""tries""", tries, chat_id)
    await edit_message(bot, message, 'В каком формате вы хотите получить ваше API?', input_buttons=['api_in_file', 'api_in_message'], last=True)

async def generate_fastapi_code(data):
    code = """
from fastapi import FastAPI

app = FastAPI()

"""
    for i in range(1, data["current_method_index"] + 1):
        method_data = data[f"method_{i}"]
        method = method_data["method"].lower()
        tag = method_data["tag"]
        name_func = method_data["name_func"]
        return_value = method_data["return"]
        args = method_data.get("args", [])
        check_item_sum = method_data.get("check_item_sum", "")

        # Generate function definition
        func_def = f"@app.{method}(\"{tag}\")\n"
        func_def += f"async def {name_func}("
        func_def += ", ".join([f"{arg.split()[1]}: {arg.split()[0]}" for arg in args])
        func_def += "):\n"

        # Generate function body
        func_body = ""
        if check_item_sum:
            check_arg, check_structure, check_return = check_item_sum.split()
            func_body += f"    if {check_arg} in {check_structure}:\n"
            func_body += f"        return {check_return}\n"
        func_body += f"    return {return_value}\n"

        # Combine function definition and body
        code += func_def + func_body + "\n"

    return code

async def send_api_in_file(bot, message):
    chat_id = message.chat.id
    data = await read_json_file(await get_value_from_bd("""api""", chat_id))
    code = await generate_fastapi_code(data)
    filename = "your_api.py"
    async with aiofiles.open(f'data/{filename}', 'w') as f:
        await f.write(code)
    await bot.send_document(chat_id, open(f'data/{filename}', 'rb'))
    await aiofiles.os.remove(f'data/{filename}')
    if int(await get_value_from_bd("""tries""", message.chat.id)) == 0:
        await send_message(bot, message, 'Что-то ещё?', input_buttons = ['buy_menu', 'menu'])
    else:
        await send_message(bot, message, 'Что-то ещё?', input_buttons = ['add_method', 'clear_api', 'menu'])

async def send_api_in_message(bot, message):
    chat_id = message.chat.id
    data = await read_json_file(await get_value_from_bd("""api""", chat_id))
    code = await generate_fastapi_code(data)
    await bot.send_message(chat_id, f'Ваше API:\n```python\n{code}\n```', parse_mode="Markdown")
    if int(await get_value_from_bd("""tries""", message.chat.id)) == 0:
        await send_message(bot, message, 'Что-то ещё?', input_buttons = ['buy_menu', 'menu'])
    else:
        await send_message(bot, message, 'Что-то ещё?', input_buttons = ['add_method', 'clear_api', 'menu'])

async def clear_api(bot, message):
    chat_id = message.chat.id
    json_filename = await get_value_from_bd("""api""", chat_id)
    await create_json_file(json_filename, {"user_id": message.from_user.id, "chat_id": chat_id, "current_method_index": 0})
    await set_value_in_bd("""stage_api""", "none", chat_id)
    await edit_message(bot, message, 'API очищенна!', input_buttons=['api_menu', 'menu'], last=True)

#Добавление пользователя в бд и создание JSON файла
async def insert_user(message):
    async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
        async with db.execute("""SELECT * FROM users WHERE id = ?""", (message.chat.id,)) as cursor:
            if await cursor.fetchone() is None:
                json_filename = f"{message.from_user.id}_{message.chat.id}.json"
                await db.execute("""INSERT INTO users (user_id, id, mess_id, tries, stage_api, api) VALUES (?, ?, ?, ?, ?, ?)""",
                                                    (message.from_user.id, message.chat.id, message.message_id, 5, "none", json_filename))
                await db.commit()
                # Создание JSON файла
                await create_json_file(json_filename, {"user_id": message.from_user.id, "chat_id": message.chat.id})

#Получаем значение из бд по колонке и id чата
async def get_value_from_bd(colum, id): #значение colum ВСЕГДА должно идти в тройных двойных ковычках, тоесть """[colum]"""
    async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
        async with db.execute(f"""SELECT {colum} FROM users WHERE id = ?""", (id,)) as cursor:
            colum_ans = await cursor.fetchone()
    return colum_ans[0]

#Ставим значение в бд по колонке и id чата
async def set_value_in_bd(colum, value, id): #значение colum ВСЕГДА должно идти в тройных двойных ковычках, тоесть """[colum]"""
    async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
        await db.execute(f"""UPDATE users SET {colum} = ? WHERE id = ?""", (value, id,))
        await db.commit()
