from setting import API, user_agent
from endopoint import url_ping_pong
import requests
import time
import sys
import random


def ping_pong():
    while True:
        payload = {'key': API}
        response = requests.get(url=url_ping_pong, headers=user_agent, params=payload, timeout=25)
        time.sleep(180)
        if response.status_code == 200:
            print(f'Done:- {response.json()}, {time.ctime()}')


try:
    ping_pong()
except requests.exceptions.Timeout as msg_err:
    print(f'Time out error:-> {msg_err}')
except requests.exceptions.TooManyRedirects as msg_err:
    print(f'TooManyRedirects:-> {msg_err}')
except requests.exceptions.ConnectionError as msg_err:
    sys.exit(f'Problem with DNS or internet:-> {msg_err}')
except requests.exceptions.HTTPError as msg_err:
    print(f'Status code not correct or Error:-> {msg_err}')
except KeyboardInterrupt as msg_err:
    print(f'Stop script:-> {msg_err}')
finally:
    time_out = random.choice([45, 65, 135, 185])
    print(f'Sleep script on:- {time_out}:\nTime now:-{time.ctime()}')
    time.sleep(time_out)
    ping_pong()


if __name__ == "__main__":
    ping_pong()
