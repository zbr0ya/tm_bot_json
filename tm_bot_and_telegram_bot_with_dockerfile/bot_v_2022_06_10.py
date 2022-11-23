from setting import API, user_agent, default_price, coin, currency
from endopoint import search_item_by_hash_name_specific, set_price

import json
import time
import requests
import os
import sys


"""Пропуск помилок від сервера"""

#потрібно додать помилки з бібліотеки requests adn index error!!!
def error_decorator(function):
    def wrapper(item):
        try:
            function(item)
            return function(item)
        # except Exception as msg_err:
        #     print(f'Error, {msg_err}')
        except IndexError as msg_err:
            print(f'IndexError:-> {msg_err}')
        except requests.exceptions.Timeout as msg_err:
            print(f'Time out error:-> {msg_err}')
        except requests.exceptions.TooManyRedirects as msg_err:
            print(f'TooManyRedirects:-> {msg_err}')
        except requests.exceptions.ConnectionError as msg_err:
            print(f'Problem with DNS or internet:-> {msg_err}')
        except requests.exceptions.HTTPError as msg_err:
            print(f'Status code not correct or Error:-> {msg_err}')
    return wrapper


"""Валідація ціни предмета"""


def validator_price(price: int, item: dict) -> int:
    if int(price) >= int(item["min_price"] * default_price) and int(item["min_price"] * default_price - 100) < int(price) and int(item["max_price"] * default_price) >= int(price):
        return int(price)
    # elif int(price) >= int(item["min_price"] * default_price) and int(item["min_price"] * default_price - 100) < int(price) and int(item["max_price"] * default_price) < int(price):
    #     return int(item["max_price"] * default_price)
    elif int(price) < int(item["min_price"] * default_price):
        return int(item["min_price"] * default_price)
    elif int(price) > int(item["max_price"] * default_price):
        return int(item["max_price"] * default_price)
    else:
        sys.exit(f'This item has a problem:- {item}, {time.ctime()}, {price}')


"""Видалення предмета з списку предметів на продажу"""


def delete_item_with_skin_full_info_json_and_update(delete_item: dict) -> str:
    with open('skin_full_info.json', 'r') as file_json:
        read_my_inventory = json.load(file_json)
        for item_index in read_my_inventory:
            if item_index["item_id"] == str(delete_item["item_id"]):
                read_my_inventory.pop(read_my_inventory.index(item_index))
                with open('skin_full_info.json', 'w', encoding='utf-8') as update_file_json:
                    json.dump(read_my_inventory, update_file_json, ensure_ascii=False, indent=4)
                    time.sleep(2)
                    return f'delete this item:-{item_index["market_hash_name"]}, {time.ctime()}'


"""валідація response.json - def one_marker_item"""


def validator_item_status_on_market_2(item: dict, item_info: list) -> list[dict]:
    enemy_validator_box = [skin for skin in item_info if str(skin.setdefault("class")) == item["classid"]]
    sorted_full_enemy_item = sorted(enemy_validator_box, key=lambda price: price["price"])
    return sorted_full_enemy_item


"""url - search_item_by_hash_name пошук по конкретній (одній) ячейці інформації 2"""


@error_decorator
def one_market_item(item: dict) -> dict:
    try:
        payload = {'key': API, 'hash_name': item["market_hash_name"]}
        response = requests.get(url=search_item_by_hash_name_specific, params=payload, headers=user_agent)
        if response.status_code == 200:
            sorted_enemy_validator_box = validator_item_status_on_market_2(item, response.json()["data"])
            if int(sorted_enemy_validator_box[0]["id"]) == int(item["item_id"]):
                my_price = int(sorted_enemy_validator_box[1]["price"]) - coin
                payload = {'key': API, 'item_id': item["item_id"], 'price': validator_price(my_price, item), 'cur': currency}
                response = requests.post(url=set_price, params=payload, headers=user_agent)
                if response.status_code == 200:
                    return {
                        'status_item': f'2 :- {item["market_hash_name"]} price:- {sorted_enemy_validator_box[0]["price"]}',
                        'response': response.json(),
                        'item': item
                    }
            else:
                for enemy_item in sorted_enemy_validator_box:
                    if int(enemy_item["price"]) < int(item["min_price"] * default_price):
                        continue
                    else:
                        if int(enemy_item["price"]) > int(item["min_price"] * default_price):
                            my_price = int(enemy_item["price"]) - coin
                            payload = {'key': API, 'item_id': item["item_id"], 'price': validator_price(my_price, item), 'cur': currency}
                            response = requests.post(url=set_price, params=payload, headers=user_agent)
                            if response.status_code == 200:
                                return {
                                    'status_item': f'2 :- {item["market_hash_name"]} price:- {sorted_enemy_validator_box[0]["price"]}',
                                    'response': response.json(),
                                    'item': item
                                }
    except Exception as msg_err:
        print(msg_err)



"""url - search_item_by_hash_name_specific пошук по всім ячейкам інформації 1"""


@error_decorator
def all_market_item(item: dict) -> dict:
    try:
        payload = {'key': API, 'hash_name': item["market_hash_name"]}
        response = requests.get(url=search_item_by_hash_name_specific, params=payload, headers=user_agent)
        if response.status_code == 200:
            enemy_item = response.json()["data"][0:2]
            """цей блок коду виконуєтся якщо предмет не на першому місці в черзі (також знижує ціну)"""
            if int(enemy_item[0]["id"]) != int(item["item_id"]):
                if int(enemy_item[0]["price"]) > int(item["min_price"] * default_price) and int(enemy_item[0]["price"]) < int(item["max_price"] * default_price):
                    my_price = int(enemy_item[0]["price"]) - coin
                    payload = {'key': API, 'item_id': item["item_id"], 'price': validator_price(my_price, item), 'cur': currency}
                    response = requests.post(url=set_price, params=payload, headers=user_agent)
                    if response.status_code == 200:
                        return {
                            'status_item': f'1 update price - {response.json()}:-{item["market_hash_name"]}, {time.ctime()}',
                            'response': response.json(),
                            'item': item
                        }
            else:
                """цей блок коду виконуєтся якщо предмет на першому місці і виконує функцію піднятя ціни предмета до другого - 10"""
                if int(enemy_item[0]["id"]) == int(item["item_id"]):
                    my_price = int(enemy_item[1]["price"]) - coin
                    if int(my_price) == int(enemy_item[1]["price"]) - coin:
                        return {
                            'status_item': f'1 not change price  {item["market_hash_name"]}, {time.ctime()}',
                            'response': response.json(),
                            'item': item
                        }
                    else:
                        if int(my_price) >= int(item["min_price"]):
                            payload = {'key': API, 'item_id': item["item_id"], 'price': validator_price(my_price, item), 'cur': currency}
                            response = requests.post(url=set_price, params=payload, headers=user_agent)
                            if response.status_code == 200:
                                return {
                                    'status_item': f'1 return and up price - {response.json()}:-{item["market_hash_name"]}, {time.ctime()}',
                                    'response': response.json(),
                                    'item': item
                                }
    except Exception as msg_err:
        print(msg_err)


"""функція генератор для зменшення оброблюваної інформації"""


def read_line_skin_full_info_json() -> dict:
    with open('skin_full_info.json', 'r', encoding='utf-8') as file_json:
        my_inventory = json.load(file_json)
    for get_item in my_inventory:
        yield get_item


"""main функція або виконуюча"""


def main():
    while True:
        for item in read_line_skin_full_info_json():  # виконую ітерацію по генератору
            time.sleep(1)  # час затримки роботи програми
            if item["on_market"] == 1:  # якщо статус предмета == 1 то виконується функція all_market_item
                status_name_specific = all_market_item(item)  # змінна status_item == функції all_market_item
                if status_name_specific is None:  # якщо функція all_market_item is None продовжуємо роботу без інформації в консолі
                    continue
                else:
                    if status_name_specific['response']['success'] is False and status_name_specific['response']['error'] == 'bad_item':  # перевіряемо предмет на коректність параметрів
                        delete_item_1 = delete_item_with_skin_full_info_json_and_update(status_name_specific['item'])  # якщо параметри не коректні видаляємо
                        print(delete_item_1)
                    else:
                        print(status_name_specific['status_item'])
            elif item["on_market"] == 2:  # зеркально item["on_market"] == 1
                status_hash_name = one_market_item(item)
                if status_hash_name is None:
                    continue
                else:
                    if status_hash_name['response']['success'] is False and status_hash_name['response']['error'] == 'bad_item':
                        delete_item_2 = delete_item_with_skin_full_info_json_and_update(status_hash_name['item'])
                        time.sleep(2)
                        print(delete_item_2)
                    else:
                        print(status_hash_name['status_item'])
            else:
                continue


if __name__ == "__main__":
    try:
        if not os.path.isfile("skin_full_info.json"):
            raise OSError('not found file:- skin_full_info.json')
        main()
    except OSError as msg_err:
        print(f'Error:- {msg_err}')
    except Exception as msg_err:
        print(f'Error:- {msg_err}')
        main()
    except KeyboardInterrupt as msg_err:
        print('Stop bot')
