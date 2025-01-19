import telebot
from telebot.async_telebot import AsyncTeleBot
import markup
import asyncio
from conflib import Configs, Config

configs = Configs()
configs.add_config('main', 'main', '')
main_conf = configs.get_config('main')

token = main_conf.cfg_d['token']
bot = AsyncTeleBot(token)

#Встреча Users
@bot.message_handler(content_types=['text'])
async def message_handler(message):
    match message.text:
        case '/start':
            await markup.insert_user(message)
            await markup.main_menu(bot, message)
        case '/menu' | '/home':
            await markup.main_menu_edit(bot, message, last=True)
        case '/help':
            await markup.send_message(bot, message, markup.messages['help'], input_buttons=['menu'])
        case '/create_api':
            await markup.send_message(bot, message, markup.messages['api_create'], input_buttons=['create_get', 'create_post', 'create_put', 'create_delete', 'menu'])
        # case '/property':
        #     await markup.send_my_property(bot, message)
        # case '/modelslist':
        #     await markup.model_menu(bot, message)
        case '/get_id':
            id:int = await markup.get_value_from_bd("""id""", message.chat.id)
            user_id:int = await markup.get_value_from_bd("""user_id""", message.chat.id)
            await markup.send_message(bot, message, f'👾┃ Откладка для персонала \n┃Chat ID:{id} \n┃ User ID:{user_id}')
        case _:
            print(await markup.get_value_from_bd("""stage_api""", message.chat.id))
            match await markup.get_value_from_bd("""stage_api""", message.chat.id):
                case "GET" | "POST" | "PUT" | "DELETE": 
                    if message.text[0] == "/":
                        await markup.api_work(message, "tag", name=message.text)
                        await markup.send_message(bot, message, markup.messages['name_func'])
                    else:
                        await markup.send_message(bot, message, 'Тег может начинаться только со знака "/"!')
                case "tag":
                    if " " in message.text:
                        await markup.send_message(bot, message, 'Название функции не может иметь пробела!')
                    else:
                        await markup.api_work(message, "name_func", value=message.text)
                        await markup.send_message(bot, message, markup.messages['return'])
                case "name_func":
                    await markup.api_work(message, "return", value=message.text)
                    await markup.send_message(bot, message, markup.messages['arg_count'])
                case "return":
                    if message.text.isdigit() and " " not in message.text:
                        await markup.api_work(message, "arg_count", value=message.text)
                        await markup.send_message(bot, message, markup.messages['argN'])
                    else:
                        await markup.send_message(bot, message, 'Количество аргументов должно быть числом без пробелов!')
                case "arg_count":
                    await markup.api_work(message, "argN", value=message.text)
                    await markup.send_message(bot, message, markup.messages['check_need'])
                case "argN":
                    await markup.api_work(message, "check_need", value=message.text)
                    await markup.send_message(bot, message, markup.messages['check_item_sum'])
                case "check_need":
                    if message.text.lower() == "да":
                        await markup.api_work(message, "check_item_sum", value=message.text)
                        await markup.send_message(bot, message, 'API успешно создано!')
                    else:
                        await markup.api_work(message, "none", value=message.text)
                        await markup.send_message(bot, message, 'API успешно создано!')
                case "check_item_sum":
                    await markup.api_work(message, "none", value=message.text)
                    await markup.send_message(bot, message, 'API успешно создано!')
                case _:
                    await markup.send_message(bot, message, markup.messages['resend'])

#Слушаем Юзера
@bot.callback_query_handler(func=lambda call: True)
async def message_callback(call):
    print(call.data)
    await markup.set_value_in_bd("""mess_id""", call.message.message_id, call.message.chat.id)
    match call.data:
        case 'api_menu':
            await markup.edit_message(bot, call.message, markup.messages['api_menu'], input_buttons=['api_create', 'menu'])
        case 'api_create':
            await markup.edit_message(bot, call.message, markup.messages['api_create'], input_buttons=['create_get', 'create_post', 'create_put', 'create_delete', 'menu'])
        case 'create_cancel':
            await markup.edit_message(bot, call.message, markup.messages['api_menu'], input_buttons=['api_create', 'menu'])
        case 'create_get':
            await markup.api_work(call.message, "GET")
            await markup.edit_message(bot, call.message, markup.messages['create_get'], input_buttons=['create_cancel'])
        case 'create_post':
            await markup.api_work(call.message, "POST")
            await markup.edit_message(bot, call.message, markup.messages['create_post'], input_buttons=['create_cancel'])
        case 'create_put':
            await markup.api_work(call.message, "PUT")
            await markup.edit_message(bot, call.message, markup.messages['create_put'], input_buttons=['create_cancel'])
        case 'create_delete':
            await markup.api_work(call.message, "DELETE")
            await markup.edit_message(bot, call.message, markup.messages['create_delete'], input_buttons=['create_cancel'])
        case 'profile':
            await markup.edit_message_profile(bot, call.message)
        # case 'packs':
        #     await markup.edit_message(bot, call.message, markup.messages['sells'],  buy_buttons=True,)
        # case 'buy_packs':
        #     await markup.edit_message(bot, call.message, 'Информация по работе Бота:',  input_buttons=['menu'], )
        # case 'low':
        #     await markup.edit_message(bot, call.message, markup.messages['low'], 'low', ['buy', 'menu'],  )
        # case 'medium':
        #     await markup.edit_message(bot, call.message, markup.messages['medium'],  'medium', ['buy', 'menu'], )
        # case 'premium':
        #     await markup.edit_message(bot, call.message,  markup.messages['premium'], 'premium', ['buy', 'menu'], )
        # case 'buy':
        #     await markup.buy(bot, call.message)
        # case 'check':
        #     await markup.check(bot, call.message)
        case 'help':
            await markup.edit_message(bot, call.message, markup.messages['help'], parse_mode="Markdown", input_buttons=['menu'])
        case 'start':
            await markup.main_menu_edit(bot, call.message)
        # case 'my_property':
        #     await markup.get_my_property(bot, call.message)
        case '':
            for button in markup.buttons:
                if call.data == markup.buttons[f'{button}'].callback_data: 
                    markup.buttons['']
                else:
                    pass
        case _:
            # if '/model ' in call.data:
            #     await markup.model_set(bot, call)
            # else:
                await markup.edit_message(bot, call.message, markup.messages['resend'])

asyncio.run(markup.init_bd())
asyncio.run(bot.polling(none_stop=True))