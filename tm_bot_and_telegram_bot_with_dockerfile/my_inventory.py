import requests
import json
from setting import API, user_agent


def inventory():
    url = f'https://market.csgo.com/api/v2/my-inventory/?key={API}'
    response = requests.get(url=url, headers=user_agent)
    if response.status_code == 200:
        with open('my_inventory_info.json', 'w', encoding='utf-8') as file_json:
            json.dump(response.json()["items"], file_json, ensure_ascii=False, indent=4)
            return response.json()["items"]


def add_my_setting_in_json():
    info = inventory()
    full_info = []
    for my_inventory in info:
        my_inventory['item_id'] = 0
        my_inventory['min_price'] = 0.000
        my_inventory['max_price'] = 0.000
        my_inventory['on_market'] = 0
        full_info.append(my_inventory)
    with open('my_inventory_info.json', 'w', encoding='utf-8') as file_json:
        json.dump(full_info, file_json, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    add_my_setting_in_json()
    print('OK')
