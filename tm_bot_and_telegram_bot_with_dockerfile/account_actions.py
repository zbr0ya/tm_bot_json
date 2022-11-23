import requests
import sys
from setting import API, user_agent
from endopoint import *


def what_you_need():
    print("""Виберіть параметр:-\n1 - get_money\n2 - go_offline\n3 - update_inventory\n4 - remove_all_from_sale\n5 - test\n6 - get_my_steam_id""")
    info = {1: get_money, 2: go_offline, 3: update_inventory, 4: remove_all_from_sale, 5: test, 6: get_my_steam_id}
    waiting_for_the_user = int(input('Виберіть функцію використовуючи цифри:-'))
    if info.get(waiting_for_the_user) is None:
        raise KeyError(f'Ключ:- відсутній!!!')
    elif type(info.get(waiting_for_the_user)) is str():
        raise ValueError('Використовуйте лише цифри')
    else:
        return info.get(waiting_for_the_user)


def send_user_info():
    user_endpoint = str(what_you_need())
    payload = {'key': API}
    response = requests.get(url=user_endpoint, headers=user_agent, params=payload)
    if response.status_code == 200:
        print(response.json())
        sys.exit('Прогрму зупинено!!!')


send_user_info()
