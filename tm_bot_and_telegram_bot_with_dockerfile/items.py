import requests
import time
from setting import API, user_agent
from endopoint import items_url
import random
import sys


def refresh_item_status():
    while True:
        payload = {'key': API}
        response = requests.get(url=items_url, headers=user_agent, params=payload, timeout=2)
        time.sleep(35)
        if response.status_code == 200:
            for status_item_info in response.json()["items"]:
                if status_item_info["status"] == "2":
                    print(f'SOLD!!!\nThis item user:- {status_item_info}')
                elif status_item_info["status"] == "4":
                    print(f'GET!!!\nThis item:-{status_item_info}')
                elif status_item_info["status"] == "3":
                    print(f'WAIT!!\nMaybe buy this item:- {status_item_info}')
                else:
                    continue


try:
    refresh_item_status()
except requests.exceptions.ConnectionError as msg_err:
    print(f'Problem with DNS or internet:- {msg_err}')
except requests.exceptions.HTTPError as msg_err:
    print(f'Not correct status code:- {msg_err}')
except requests.exceptions.TooManyRedirects as msg_err:
    print(f'Time out error:- {msg_err}')
except KeyboardInterrupt as msg_err:
    sys.exit(f'Stop program:- {msg_err}')
finally:
    time_out_program = random.choice([45, 65, 95])
    time.sleep(int(time_out_program))
    refresh_item_status()
