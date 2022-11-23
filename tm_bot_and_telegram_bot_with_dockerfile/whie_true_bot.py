import json
import time
import requests
from setting import API, user_agent, default_price, coin, currency
import pprint
from endopoint import search_item_by_hash_name_specific, set_price
import sys
import random


with open('skin_full_info.json', 'r', encoding='utf-8') as file_json:
    my_inventory = json.load(file_json)


def bot_work():
    while True:
        inventory = my_inventory
        for item in inventory:
            time.sleep(1)
            url_search_item_by_hash_name_specific = search_item_by_hash_name_specific
            payload = {'key': API, 'hash_name': item["market_hash_name"]}
            response = requests.get(url=url_search_item_by_hash_name_specific, params=payload, headers=user_agent)
            if response.status_code == 200:
                # print(response.json())
                enemy_item = response.json()["data"][0]
                if int(enemy_item["id"]) != int(item["item_id"]):
                    if int(enemy_item["price"]) > int(item["min_price"] * default_price) and int(enemy_item["price"]) < int(item["max_price"] * default_price):
                        my_price = int(enemy_item["price"]) - coin
                        url_set_price = set_price
                        payload = {'key': API, 'item_id': item["item_id"], 'price': my_price, 'cur': currency}
                        response = requests.post(url=url_set_price, params=payload, headers=user_agent)
                        if response.status_code == 200:
                            if response.json()["success"] is True:
                                print(f'{response.json()}:-{item["market_hash_name"]}, {time.ctime()}')
                else:
                    int(enemy_item["price"]) > int(item["max_price"])
                    print(f'THIS item:- {response.json()["data"][0]["market_hash_name"]},need change price or delete with list,{time.ctime()}')
                    continue


try:
    bot_work()
except requests.exceptions.Timeout as msg_err:
    print(f'Time out error:-> {msg_err}')
except requests.exceptions.TooManyRedirects as msg_err:
    print(f'TooManyRedirects:-> {msg_err}')
except requests.exceptions.ConnectionError as msg_err:
    print(f'Problem with DNS or internet:-> {msg_err}')
except requests.exceptions.HTTPError as msg_err:
    print(f'Status code not correct or Error:-> {msg_err}')
except KeyboardInterrupt as msg_err:
    print(f'Stop script:-> {msg_err}')
except IndexError as msg_err:
    print(f'IndexError:-> {msg_err}')

finally:
    time_out = random.choice([45, 65, 135, 185])
    print(f'Sleep script on:- {time_out}:\nTime now:-{time.ctime()}')
    time.sleep(time_out)
    bot_work()


if __name__ == "__main__":
    bot_work()
