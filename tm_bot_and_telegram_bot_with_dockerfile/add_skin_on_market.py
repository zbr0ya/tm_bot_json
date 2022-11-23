import time
import requests
import json
from setting import API, user_agent, currency
import sys


def read_info_about_my_inventory():
    try:
        with open('my_inventory_info.json', 'r', encoding='utf-8') as file_json:
            read_my_inventory = json.load(file_json)
            return read_my_inventory
    except FileNotFoundError as error:
        print(f'Потрібно створити цей файл:-{str(error).split(":")[1]}\nВикориставши метод my_inventory.py\n{"#" * 53}')


def add_my_inventory_on_market():
    id_my_inventory = []
    my_inventory = read_info_about_my_inventory()
    if my_inventory is None:
        sys.exit('Ви не використали скрипт:- my_inventory.py')
    else:
        for skin in my_inventory:
            if skin["on_market"] == 1 or skin["on_market"] == 2:
                my_price = round(skin["max_price"] * 1000, 3)
                url_add_to_sale = f'https://market.csgo.com/api/v2/add-to-sale?key={API}&id={skin["id"]}&price={my_price}&cur={currency}'
                print(url_add_to_sale)
                time.sleep(1)
                response = requests.post(url=url_add_to_sale, headers=user_agent)
                if response.status_code == 200:
                    print(response.json())
                    if response.json()['success'] is True:
                        skin["item_id"] = response.json()["item_id"]
                        print(skin)
                        id_my_inventory.append(skin)
                    else:
                        response.json()['success'] is False
                        continue

        return id_my_inventory


def write_my_skin_inventory_id():
    write_id = add_my_inventory_on_market()
    with open('skin_full_info.json', 'w', encoding='utf-8') as file_json:
        json.dump(write_id, file_json, ensure_ascii=False, indent=4)


write_my_skin_inventory_id()
