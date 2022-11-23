from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from setting import API, user_agent
from endopoint import items_url
from telegram_token import TOKEN
import requests
import asyncio
from keyboards import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_program(message: types.Message):
    await message.answer(f'Program work', reply_markup=buttons)


""" status = 2 — Вы продали вещь и должны ее передать боту.
    status = 3 — Ожидание передачи боту купленной вами вещи от продавца.
    status = 4 — Вы можете забрать купленную вещь."""


@dp.message_handler(commands=['status_item'])
async def status_my_sell_buy_item(message: types.Message):
    while True:
        try:
            await asyncio.sleep(55)
            payload = {'key': API}
            response = requests.get(url=items_url, headers=user_agent, params=payload, timeout=2)
            if response.status_code == 200:
                for status_item_info in response.json()["items"]:
                    if status_item_info["status"] == "2":
                        await message.answer(f'SOLD!!!\nThis item user:- {status_item_info}')
                    elif status_item_info["status"] == "4":
                        await message.answer(f'GET!!!\nThis item:-{status_item_info}')
                    elif status_item_info["status"] == "3":
                        await message.answer(f'WAIT!!\nMaybe buy this item:- {status_item_info}')
                    else:
                        continue
        except requests.exceptions.Timeout as msg_err:
            print(f'Time out error:-> {msg_err}')
        except requests.exceptions.TooManyRedirects as msg_err:
            print(f'TooManyRedirects:-> {msg_err}')
        except requests.exceptions.ConnectionError as msg_err:
            print(f'Problem with DNS or internet:-> {msg_err}')
        except requests.exceptions.HTTPError as msg_err:
            print(f'Status code not correct or Error:-> {msg_err}')
        finally:
            return status_my_sell_buy_item


"""status = 1 — Вещь выставлена на продажу."""


@dp.message_handler(commands=['on_market'])
async def my_item_on_market(message: types.Message):
    try:
        payload = {'key': API}
        response = requests.get(url=items_url, headers=user_agent, params=payload)
        if response.status_code == 200:
            for item_on_market in response.json()["items"]:
                await message.answer(
                    f'ON_MARKET!!\n{item_on_market["market_hash_name"]}:- {item_on_market["price"]} {item_on_market["currency"]}\nposition:- {item_on_market["position"]}')
    except TypeError as msg_err:
        await message.answer(f'You are not selling anything:- {msg_err}')
    except requests.exceptions.HTTPError as msg_err:
        print(f'Status code not correct or Error:-> {msg_err}')
        await message.answer('Try again, status code not correct')
    finally:
        return status_my_sell_buy_item


if __name__ == '__main__':
    executor.start_polling(dp)
