import aiosqlite
from telebot import types
from conflib import Configs, Config
import random 
from random import random, randrange, randint
import os
import json
import aiofiles

messbutton = types.InlineKeyboardMarkup()

barsbutton = types.ReplyKeyboardMarkup()

async def init_bd():
    async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id   BIGINT,
            id        BIGINT,
            mess_id   BIGINT,
            bill_id   TEXT,
            premium   INT,
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
    'buy_menu':       types.InlineKeyboardButton(text='Улучшить подписку', callback_data='buy_menu'),
    'menu':           types.InlineKeyboardButton(text='Главное меню', callback_data='start'),
    'delete_method':  types.InlineKeyboardButton(text='Удалить метод', callback_data='delete_method'),
    'add_method':     types.InlineKeyboardButton(text='Сделать ещё один метод', callback_data='add_method'),
    'finish_api':     types.InlineKeyboardButton(text='Закончить создание API', callback_data='finish_api'),
    'clear_api':      types.InlineKeyboardButton(text='Очистить всю API', callback_data='clear_api')
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
    'resend':          '❓┃ Я тебя, увы, не понимаю. \nПроверьте написание команды/аргуметов. Или напишите /help.'
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

# #Меню оплаты
# async def buy(bot, message):
#     channel = await get_value_from_bd("""buy_channel""", message.chat.id)
#     comment = str(message.chat.id) + '_' + channel
#     bill = p2p.bill(amount = prices[channel], lifetime = 15, comment = comment)
#     await set_value_in_bd("""bill_id""", bill.bill_id, message.chat.id)
#     buy_btn = types.InlineKeyboardButton(text = "Купить", url = bill.pay_url)
#     messbutton = types.InlineKeyboardMarkup()
#     messbutton.add(buy_btn)
#     messbutton.add(buttons['check'])
#     messbutton.add(buttons['menu'])
#     await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Вы приобретаете тариф **Stable Diffusion** Тариф.План\nОзнакомится с получаемыми возможностями, вы можете здесь Placeholder for Price List',  reply_markup=messbutton)

# #Проверить платёж
# async def check(bot, message):
#     bill = await get_value_from_bd("""bill_id""", message.chat.id)
#     status = p2p.check(bill_id=bill).status
#     match status:
#         case 'WAITING':
#             await send_message(bot, message, '❓┃ Вы ещё не оплатили')
#         case 'REJECTED':
#             await set_value_in_bd("""bill_id""", '', message.chat.id)
#             await set_value_in_bd("""buy_channel""", '', message.chat.id)
#             await edit_message(bot, message, '❌┃ Счёт откланён, начните оплату сначала',  input_buttons=['packs'])
#         case 'EXPIRED':
#             await set_value_in_bd("""bill_id""", '', message.chat.id)
#             await set_value_in_bd("""buy_channel""", '', message.chat.id)
#             await edit_message(bot, message, '❌┃Время счёта истекло, начните оплату сначала',  input_buttons=['packs'])
#         case 'PAID':
#             match get_value_from_bd("""buy_channel""", message.chat.id):
#                 case 'low':
#                     await set_value_in_bd("""level""", 1, message.chat.id)
#                 case 'medium':
#                     await set_value_in_bd("""level""", 2, message.chat.id)
#                 case 'premium':
#                     await set_value_in_bd("""level""", 3, message.chat.id)
#             await set_value_in_bd("""bill_id""", '', message.chat.id)
#             await set_value_in_bd("""buy_channel""", '', message.chat.id)
#             await set_value_in_bd("""days""", 31, message.chat.id)
#             await edit_message(bot, message, '✅┃ Спасибо за покупку. С возможностями вашего тарфного плана, вы можете ознакомится здесь',  input_buttons=['buy_packs', 'packs', 'menu'])

# #Конфигурация бота
# async def configure(bot, message):
#     print(message.text)
#     match int(await get_value_from_bd("""level""", message.chat.id)):
#         case 0:
#             await send_message(bot, message, '❌┃ Вам пока не доступна настройка бота, купите тариф для того, чтобы пользоваться нашим ботом',  input_buttons=['packs', 'menu'])
#         case 1:
#             match message.text.split(' ')[0]:
#                 case '/model':
#                     if message.text.split(' ')[1] in models_low:
#                         await set_value_in_bd("""model""", models[message.text.split(' ')[1]], message.chat.id)
#                         await send_message(bot, message, '✅┃ Конфигураци `model` поставлена на ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
#                     else:
#                         await send_message(bot, message, '❌┃ Нет такой модели или вам она недоступна, почитайте возможности конфигурации',  input_buttons=['buy_packs', 'menu'])
#                 case '/cfg':
#                     if message.text.split(' ')[1] >= 0:
#                         await set_value_in_bd("""cfg""", float(message.text.split(' ')[1]), message.chat.id)
#                         await send_message(bot, message, '✅┃ Конфигураци cfg поставлена на ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
#                     else:
#                         await send_message(bot, message, '❌┃ Введите, пожалуйста положительное число, или 0. Рекомендую от 6 - 7.5 - 8. Работает эффективно',  input_buttons=['buy_packs', 'menu'])
#                 case '/size':
#                     if len(message.text.split(' ')) == 3:
#                         height = int(message.text.split(' ')[1])
#                         width = int(message.text.split(' ')[2])
#                         if height >= min_height['low'] and height <= max_height['low'] and width >= min_width['low'] and width <= max_width['low']:
#                             await set_value_in_bd("""size_height""", height, message.chat.id)
#                             await set_value_in_bd("""size_width""", width, message.chat.id)
#                             await send_message(bot, message, '✅┃ Конфигураци size поставлена на значения ' + message.text.split(' ')[1] + ' ' + message.text.split(' ')[2],  input_buttons=['buy_packs', 'menu'])
#                         else:
#                             await send_message(bot, message, '❌┃ Вам не доступны такие размеры изображения. \nПочитайте возможности конфигурации для вашего тарифа',   input_buttons=['buy_packs', 'menu'])
#                     else:
#                         await send_message(bot, message, '❗┃ Введите пожалуйста размеры желательного изображения в формате `/size [height] [width]`',  parse_mode="Markdown")
#                 case '/countpic':
#                     if int(message.text.split(' ')[1]) >= min_countpic['low'] and int(message.text.split(' ')[1]) <= max_countpic['low']:
#                         await set_value_in_bd("""countpic""", int(message.text.split(' ')[1]), message.chat.id)
#                         await send_message(bot, message, f'✅┃ Конфигурация `/countpic` поставлена на значение {message.text.split(" ")[1]}',  input_buttons=['buy_packs', 'menu'])
#                     else:
#                         await send_message(bot, message, '❌┃ Вам не доступно такое количество картинок на обработку, почитайте возможности конфигурации',  input_buttons=['buy_packs', 'menu'])
#                 case '/sampler':
#                     await set_value_in_bd("""sampler""", message.text.split(' ')[1], message.chat.id)
#                     await send_message(bot, message, '✅┃ Конфигураци `sampler` поставлена на значение ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
#                 case '/generate' | '/prompts':
#                     await generate(bot, message)
#                 case _:
#                     await send_message(bot, message, messages['resend'])
#         #Stable Diffusion Medium
#         case 2:
#             match message.text.split(' ')[0]:
#                 case '/model':
#                     if message.text.split(' ')[1] in models_medium:
#                         await set_value_in_bd("""model""",  models[message.text.split(' ')[1]], message.chat.id)
#                         await send_message(bot, message, '✅┃ Конфигураци `model` поставлена на ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
#                     else:
#                         await send_message(bot, message, '❌┃ Нет такой модели или вам она недоступна, почитайте возможности конфигурации',  input_buttons=['buy_packs', 'menu'])
#                 case '/cfg':
#                     if message.text.split(' ')[1] >= 0:
#                         await set_value_in_bd("""cfg""", float(message.text.split(' ')[1]), message.chat.id)
#                         await send_message(bot, message, '✅┃ Конфигураци cfg поставлена на ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
#                     else:
#                         await send_message(bot, message, '❌┃ Введите, пожалуйста положительное число, или 0. Рекомендую от 6 - 7.5 - 8. Работает эффективно',  input_buttons=['buy_packs', 'menu'])
#                 case '/size':
#                     if len(message.text.split(' ')) == 3:
#                         height = int(message.text.split(' ')[1])
#                         width = int(message.text.split(' ')[2])
#                         if height >= min_height['medium'] and height <= max_height['medium'] and width >= min_width['medium'] and width <= max_width['medium']:
#                             await set_value_in_bd("""size_height""", height, message.chat.id)
#                             await set_value_in_bd("""size_width""", width, message.chat.id)
#                             await send_message(bot, message, '✅┃ Конфигураци size поставлена на значения ' + message.text.split(' ')[1] + ' ' + message.text.split(' ')[2],  input_buttons=['buy_packs', 'menu'])
#                         else:
#                             await send_message(bot, message, '❌┃ Вам не доступны такие размеры изображения. \nПочитайте возможности конфигурации для вашего тарифа',   input_buttons=['buy_packs', 'menu'])
#                     else:
#                         await send_message(bot, message, '❗┃ Введите пожалуйста размеры желательного изображения в формате `/size [height] [width]`',  parse_mode="Markdown")
#                 case '/countpic':
#                     if int(message.text.split(' ')[1]) >= min_countpic['medium'] and int(message.text.split(' ')[1]) <= max_countpic['medium']:
#                         await set_value_in_bd("""countpic""", int(message.text.split(' ')[1]), message.chat.id)
#                         await send_message(bot, message, f'✅┃ Конфигурация `/countpic` поставлена на значение {message.text.split(" ")[1]}',  input_buttons=['buy_packs', 'menu'])
#                     else:
#                         await send_message(bot, message, '❌┃ Вам не доступно такое количество картинок на обработку, почитайте возможности конфигурации',  input_buttons=['buy_packs', 'menu'])
#                 case '/sampler':
#                     await set_value_in_bd("""sampler""", message.text.split(' ')[1], message.chat.id)
#                     await send_message(bot, message, '✅┃ Конфигураци `sampler` поставлена на значение ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
#                 case '/generate' | '/prompts':
#                     await generate(bot, message)
#                 case _:
#                     await send_message(bot, message, messages['resend'])
#         case 3 | 777:
#             match message.text.split(' ')[0]:
#                 case '/model':
#                     if message.text.split(' ')[1] in models_premium:
#                         await set_value_in_bd("""model""",  models[message.text.split(' ')[1]], message.chat.id)
#                         await send_message(bot, message, 'Конфигураци model поставлена на ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
#                     else:
#                         await send_message(bot, message, 'Нет такой модели, почитайте возможности конфигурации',  input_buttons=['buy_packs', 'menu'])
#                 case '/cfg':
#                     if message.text.split(' ')[1] >= 0:
#                         await set_value_in_bd("""cfg""", float(message.text.split(' ')[1]), message.chat.id)
#                         await send_message(bot, message, 'Конфигураци cfg поставлена на ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
#                     else:
#                         await send_message(bot, message, 'Введите, пожалуйста положительное число, или 0',  input_buttons=['buy_packs', 'menu'])
#                 case '/size':
#                     if len(message.text.split(' ')) == 3:
#                         height = int(message.text.split(' ')[1])
#                         width = int(message.text.split(' ')[2])
#                         if height >= min_height['premium'] and height <= max_height['premium'] and width >= min_width['premium'] and width <= max_width['premium']:
#                             await set_value_in_bd("""size_height""", height, message.chat.id)
#                             await set_value_in_bd("""size_width""", width, message.chat.id)
#                             await send_message(bot, message, 'Конфигураци size поставлена на значения ' + message.text.split(' ')[1] + ' ' + message.text.split(' ')[2],  input_buttons=['buy_packs', 'menu'])
#                         else:
#                             await send_message(bot, message, 'Вам не доступны такие размеры изображения, почитайте возможности конфигурации',  input_buttons=['buy_packs', 'menu'])
#                     else:
#                         await send_message(bot, message, 'Введите пожалуйста размеры желательного изображения в формате /size [height] [width]')
#                 case '/countpic':
#                     if int(message.text.split(' ')[1]) >= min_countpic['premium'] and int(message.text.split(' ')[1]) <= max_countpic['premium']:
#                         await set_value_in_bd("""countpic""", int(message.text.split(' ')[1]), message.chat.id)
#                         await send_message(bot, message, 'Конфигураци countpic поставлена на значение ' + int(message.text.split(' ')[1]),  input_buttons=['buy_packs', 'menu'])
#                     else:
#                         await send_message(bot, message, 'Вам не доступно такое количество картинок на обработку, почитайте возможности конфигурации',  input_buttons=['buy_packs', 'menu'])
#                 case '/sampler':
#                     await set_value_in_bd("""sampler""", message.text.split(' ')[1], message.chat.id)
#                     await send_message(bot, message, 'Конфигураци sampler поставлена на значение ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
#                 case '/generate' | '/prompts':
#                     await generate(bot, message)
#                 case _:
#                     await send_message(bot, message, messages['resend'])

# async def send_modelslist(bot, message):
#     match int(await get_value_from_bd("""level""", message.chat.id)):
#         case 0:
#                     await send_message(bot, message, "❗┃ Вы ещё не приобрели тариф, вам не доступна эта команда")
#         case 1:
#                     await send_message(bot, message, f'┬'+'\n├'.join(models_low))
#         case 2:
#                     await send_message(bot, message, f'┬'+'\n├'.join(models_medium))
#         case 3 | 777:
#                     await send_message(bot, message, f'┬'+'\n├'.join(models_premium))

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

# #Отправка фото
# async def send_photo(bot, message, img:Image=None):
#         await bot.send_photo(message.chat.id, photo=img)

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
    await set_value_in_bd("""stage_api""", "none", message.chat.id)
    await edit_message(bot, message, 'Выберите метод:', input_buttons=['create_get', 'create_post', 'create_put', 'create_delete', 'menu'], last=True)

async def finish_api(bot, message):
    await edit_message(bot, message, 'В каком формате вы хотите получить ваше API?', last=True)

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
                await db.execute("""INSERT INTO users (user_id, id, mess_id, bill_id, premium, tries, stage_api, api) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                                    (message.from_user.id, message.chat.id, message.message_id, '', 0, 5, "none", json_filename))
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

# #получение конфигурации пользователя
# async def get_my_property(bot, message):
#     height = await get_value_from_bd("""size_height""", message.chat.id)
#     width = await get_value_from_bd("""size_width""", message.chat.id)
#     model = await get_value_from_bd("""model""", message.chat.id)
#     cfg_scale = await get_value_from_bd("""cfg""", message.chat.id)
#     n_iter = await get_value_from_bd("""countpic""", message.chat.id)
#     sampler = await get_value_from_bd("""sampler""", message.chat.id)
#     await edit_message(bot, message, text= f"ℹ️ ┃ Ваши настройки:\n\nРазмеры картинки:\n ┃ {height} x {width}\n\nМодель:\n ┃ {model}\n\nКоэфициент точности:\n ┃ {cfg_scale}\n\nКоличество картинок:\n ┃ {n_iter}\n\nСэмплер:\n ┃ {sampler}")


# #Отправка конфигурации пользователя /property
# async def send_my_property(bot, message):
#     height = await get_value_from_bd("""size_height""", message.chat.id)
#     width = await get_value_from_bd("""size_width""", message.chat.id)
#     model = await get_value_from_bd("""model""", message.chat.id)
#     cfg_scale = await get_value_from_bd("""cfg""", message.chat.id)
#     n_iter = await get_value_from_bd("""countpic""", message.chat.id)
#     sampler = await get_value_from_bd("""sampler""", message.chat.id)
#     await send_message(bot, message, text= f"ℹ️ ┃ Ваши настройки:\n\nРазмеры картинки:\n /size\n ┃ {height} x {width}\n\nМодель:\n /model\n ┃ {model}\n\nКоэфициент точности:\n /cfg\n ┃ {cfg_scale}\n\nКоличество картинок:\n /countpic\n ┃ {n_iter}\n\nСэмплер:\n/sampler \n ┃ {sampler}")




# async def model_menu(bot, message):
#     level = int(await get_value_from_bd("""level""", message.chat.id))
#     match level:
#         case 0:
#             await send_message(bot, message, '❌┃ Вам пока не доступна настройка бота, купите тариф для того, чтобы пользоваться нашим ботом',  input_buttons=['packs', 'menu'])
#         case 1 | 2 | 3 | 777:
#             await send_message(bot, message, text= f"Ваш список моделей", input_buttons=(models_low if level == 1 else models_medium if level == 2 else models_premium if level == 3 else models_premium if level == 777 else 'fuck'))

# async def model_set(bot, call):
#     level = int(await get_value_from_bd("""level""", call.message.chat.id))
#     match level:
#         case 0:
#             await send_message(bot, call.message, '❌┃ Вам пока не доступна настройка бота, купите тариф для того, чтобы пользоваться нашим ботом',  input_buttons=['packs', 'menu'])
#         case 1 | 2 | 3 | 777:
#             if call.data.split(' ')[1] in (models_low if level == 1 else models_medium if level == 1 else models_premium if level == 3 else models_premium if level == 777 else 'fuck'):
#                 await set_value_in_bd("""model""",  models[call.data.split(' ')[1]], call.message.chat.id)
#                 await send_message(bot, call.message, '✅┃ Конфигураци `model` поставлена на ' + call.data.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
#             else:
#                 await send_message(bot, call.message, '❌┃ Нет такой модели или вам она недоступна, почитайте возможности конфигурации',  input_buttons=['buy_packs', 'menu'])

# #генерация запроса в нейросеть
# async def generate(bot, message):
#     height:int = await get_value_from_bd("""size_height""", message.chat.id)
#     width:int = await get_value_from_bd("""size_width""", message.chat.id)
#     model:str = await get_value_from_bd("""model""", message.chat.id)
#     cfg_scale:float = await get_value_from_bd("""cfg""", message.chat.id)
#     n_iter:int = await get_value_from_bd("""countpic""", message.chat.id)
#     sampler:str = await get_value_from_bd("""sampler""", message.chat.id)
#     pr:str = ' '.join([i for n,i in enumerate(message.text.split(' ')) if n > 0])
#     prompt:str = pr
#     negative_prompt:str = ''
#     if '!' in pr:
#         prompts = pr.split('!')
#         prompt = prompts[0]
#         negative_prompt = prompts[1]
    
#     message_num = randint(1, 3)
#     if message_num == 1:
#         message_local = "🔃┃ Дай подумать, что-то покажу"
#     elif message_num == 2:
#         message_local = "🔃┃ Подожди, я думаю. Как будет готово, покажу(^3^)"
#     elif message_num == 3:
#         message_local = "🔃┃ В оброботке, подожди чуток"
#     await send_message(bot, message, message_local)
#     await Req2neuro(url_=main_conf.cfg_d['url_sd_server'], prompt=prompt, negative_prompt=negative_prompt, width=width, height=height, cfg_scale=cfg_scale, model=model, sampler=sampler, n_iter=n_iter, steps=25, func=send_photo, bot=bot, message=message)

#     if message_num == 1:
#         message_local = "✅┃ Всё готово, смотри"
#     elif message_num == 2:
#         message_local = "✅┃ Ого, что приготовилось!:з"
#     elif message_num == 3:
#         message_local = "✅┃ Вот ваш заказ"
#     await send_message(bot, message, message_local, parse_mode="Markdown")