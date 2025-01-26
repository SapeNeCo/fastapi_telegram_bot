import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import types
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
            tries = int(await markup.get_value_from_bd("""tries""", message.chat.id))
            if tries == 0:
                await markup.set_value_in_bd("""stage_api""", "none", message.chat.id)
                await markup.send_message(bot, message, markup.messages['premium_offer'], input_buttons=['buy_menu', 'menu'])
            else:
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
            current_stage = await markup.get_value_from_bd("""stage_api""", message.chat.id)
            data = await markup.read_json_file(await markup.get_value_from_bd("""api""", message.chat.id))
            current_method_index = data.get("current_method_index", 0)
            current_method = f"method_{current_method_index}"
            match current_stage:
                case "GET" | "POST" | "PUT" | "DELETE": 
                    if message.text[0] == "/":
                        await markup.api_work(bot, message, "tag", name=message.text)
                        await markup.send_message(bot, message, markup.messages['name_func'], input_buttons=['delete_method'])
                    else:
                        await markup.send_message(bot, message, 'Тег может начинаться только со знака "/"!', input_buttons=['delete_method'])
                case "tag":
                    if " " in message.text:
                        await markup.send_message(bot, message, 'Название функции не может иметь пробела!', input_buttons=['delete_method'])
                    else:
                        await markup.api_work(bot, message, "name_func", value=message.text)
                        await markup.send_message(bot, message, markup.messages['return'], input_buttons=['delete_method'])
                case "name_func":
                    await markup.api_work(bot, message, "return", value=message.text)
                    await markup.send_message(bot, message, markup.messages['arg_count'], input_buttons=['delete_method'])
                case "return":
                    if message.text.isdigit() and " " not in message.text:
                        if int(message.text) == 0:
                            if data[current_method]["method"] == "GET":
                                await markup.api_work(bot, message, "none")
                                if current_method_index - int(await markup.get_value_from_bd("""tries""", message.chat.id)) == 0:
                                    await markup.send_message(bot, message, 'Метод создан!\n\nКоличество доступных методов закончилось на эту неделю, если хотите безлимитное использование нашего бота, то вы можете улучший подписку.\n\nТак же вы можете удалить последний метод и переписать его.',
                                                               input_buttons=['buy_menu', 'delete_method', 'finish_api', 'clear_api', 'menu'])
                                else:
                                    await markup.send_message(bot, message, 'Метод создан!', input_buttons=['add_method', 'delete_method', 'finish_api', 'clear_api', 'menu'])
                            else:
                                await markup.set_value_in_bd("""stage_api""", "check_need", message.chat.id)
                                await markup.send_message(bot, message, markup.messages['check_need'], input_buttons=['delete_method'])
                        else:
                            await markup.api_work(bot, message, "arg_count", value=message.text)
                            await markup.send_message(bot, message, markup.messages['argN'], input_buttons=['delete_method'])
                    else:
                        await markup.send_message(bot, message, 'Количество аргументов должно быть числом без пробелов!', input_buttons=['delete_method'])
                case "arg_count":
                    await markup.api_work(bot, message, "argN", value=message.text)
                    if data[current_method]["arg_count"] == 1:
                        if data[current_method]["method"] == "GET":
                            await markup.api_work(bot, message, "none")
                            if current_method_index - int(await markup.get_value_from_bd("""tries""", message.chat.id)) == 0:
                                await markup.send_message(bot, message, 'Метод создан!\n\nКоличество доступных методов закончилось на эту неделю, если хотите безлимитное использование нашего бота, то вы можете улучший подписку.\n\nТак же вы можете удалить последний метод и переписать его.', 
                                                          input_buttons=['buy_menu', 'delete_method', 'finish_api', 'clear_api', 'menu'])
                            else:
                                await markup.send_message(bot, message, 'Метод создан!', input_buttons=['add_method', 'delete_method', 'finish_api', 'clear_api', 'menu'])
                        else:
                            await markup.send_message(bot, message, markup.messages['check_need'], input_buttons=['delete_method'])
                    else:
                        await markup.send_message(bot, message, markup.messages['argN'], input_buttons=['delete_method'])
                case "argN":
                    await markup.api_work(bot, message, "argN", value=message.text)
                    if len(data[current_method]["args"]) < data[current_method]["arg_count"]:
                        if data[current_method]["arg_count"] - len(data[current_method]["args"]) <= 1:
                            # Проверка метода GET
                            if data[current_method]["method"] == "GET":
                                await markup.api_work(bot, message, "none")
                                if current_method_index - int(await markup.get_value_from_bd("""tries""", message.chat.id)) == 0:
                                    await markup.send_message(bot, message, 'Метод создан!\n\nКоличество доступных методов закончилось на эту неделю, если хотите безлимитное использование нашего бота, то вы можете улучший подписку.\n\nТак же вы можете удалить последний метод и переписать его.',
                                                               input_buttons=['buy_menu', 'delete_method', 'finish_api', 'clear_api', 'menu'])
                                else:
                                    await markup.send_message(bot, message, 'Метод создан!', input_buttons=['add_method', 'delete_method', 'finish_api', 'clear_api', 'menu'])
                            else:
                                await markup.send_message(bot, message, markup.messages['check_need'], input_buttons=['delete_method'])
                        else:
                            await markup.send_message(bot, message, markup.messages['argN'], input_buttons=['delete_method'])
                    else:
                        await markup.send_message(bot, message, markup.messages['check_need'], input_buttons=['delete_method'])
                case "check_need":
                    if message.text.lower() == "да":
                        await markup.api_work(bot, message, "check_need", value=message.text)
                        await markup.send_message(bot, message, markup.messages['check_item_sum'], input_buttons=['delete_method'])
                    elif message.text.lower() == "нет":
                        await markup.api_work(bot, message, "none", value=message.text)
                        if current_method_index - int(await markup.get_value_from_bd("""tries""", message.chat.id)) == 0:
                            await markup.send_message(bot, message, 'Метод создан!\n\nКоличество доступных методов закончилось на эту неделю, если хотите безлимитное использование нашего бота, то вы можете улучший подписку.\n\nТак же вы можете удалить последний метод и переписать его.',
                                                       input_buttons=['buy_menu', 'delete_method', 'finish_api', 'clear_api', 'menu'])
                        else:
                            await markup.send_message(bot, message, 'Метод создан!', input_buttons=['add_method', 'delete_method', 'finish_api', 'clear_api', 'menu'])
                    else:
                        await markup.send_message(bot, message, 'Введите либо "Да" либо "Нет"', input_buttons=['delete_method'])
                case "check_item_sum":
                    await markup.api_work(bot, message, "check_item_sum", value=message.text)
                    if current_method_index - int(await markup.get_value_from_bd("""tries""", message.chat.id)) == 0:
                        await markup.send_message(bot, message, 'Метод создан!\n\nКоличество доступных методов закончилось на эту неделю, если хотите безлимитное использование нашего бота, то вы можете улучший подписку.\n\nТак же вы можете удалить последний метод и переписать его.',
                                                    input_buttons=['buy_menu', 'delete_method', 'finish_api', 'clear_api', 'menu'])
                    else:
                        await markup.send_message(bot, message, 'Метод создан!', input_buttons=['add_method', 'delete_method', 'finish_api', 'clear_api', 'menu'])
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
            tries = int(await markup.get_value_from_bd("""tries""", call.message.chat.id))
            if tries == 0:
                await markup.set_value_in_bd("""stage_api""", "none", call.message.chat.id)
                await markup.edit_message(bot, call.message, markup.messages['premium_offer'], input_buttons=['buy_menu', 'menu'])
            else:
                await markup.edit_message(bot, call.message, markup.messages['api_create'], input_buttons=['create_get', 'create_post', 'create_put', 'create_delete', 'menu'])
        case 'create_cancel':
            await markup.delete_method(bot, call.message)
            await markup.edit_message(bot, call.message, markup.messages['api_menu'], input_buttons=['api_create', 'menu'])
        case 'create_get':
            await markup.api_work(bot, call.message, "GET")
            await markup.edit_message(bot, call.message, markup.messages['create_get'], input_buttons=['create_cancel'])
        case 'create_post':
            await markup.api_work(bot, call.message, "POST")
            await markup.edit_message(bot, call.message, markup.messages['create_post'], input_buttons=['create_cancel'])
        case 'create_put':
            await markup.api_work(bot, call.message, "PUT")
            await markup.edit_message(bot, call.message, markup.messages['create_put'], input_buttons=['create_cancel'])
        case 'create_delete':
            await markup.api_work(bot, call.message, "DELETE")
            await markup.edit_message(bot, call.message, markup.messages['create_delete'], input_buttons=['create_cancel'])
        case 'delete_method':
            await markup.delete_method(bot, call.message)
        case 'add_method':
            await markup.add_method(bot, call.message)
        case 'finish_api':
            await markup.finish_api(bot, call.message)
        case 'api_in_file':
            await markup.send_api_in_file(bot, call.message)
        case 'api_in_message':
            await markup.send_api_in_message(bot, call.message)
        case 'clear_api':
            await markup.clear_api(bot, call.message)
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