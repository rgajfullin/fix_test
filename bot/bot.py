import requests
import re
import json
import logging
import time
import signal
with open('config.json') as config_file:
    config = json.load(config_file)

token = config['telegram']['token']
chat_id = config['telegram']['chat_id']
read_timeout = config['timeout']['read']
connection_timeout = config['timeout']['connection']
url = config['service']['url']
search_string = config['service']['search_string']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


def send_message(text):
    telegram_url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
    response = requests.post(telegram_url, data={'text': text,
                             'chat_id': chat_id, 'parse_mode': 'html'})


def check_url():
    try:
        request = requests.get(url, timeout=(connection_timeout, read_timeout))
        if request.status_code == 200 and request.text.find(search_string) >= 0:
            return 0
        else:
            send_message(text="{} is broken. {} not found".format(url, search_string))
            return 1
    except requests.exceptions.ReadTimeout as error:
        send_message(text="Read timed out")
        print error
        return 1
    except requests.exceptions.ConnectTimeout as error:
        send_message(text="Connection timed out")
        print error
        return 1
    except requests.exceptions.ConnectionError as error:
        send_message(text="Connection error")
        print error
        return 1


def main():
    killer = GracefulKiller()
    print "Bot ready"
    send_message(text="Monitoring up")
    starttime = time.time()
    while True:
        if check_url():
            time.sleep(60)
        if killer.kill_now:
            break
    send_message(text="Monitoring down")
    print "Gracefully shutting down."
    time.sleep(1.0 - ((time.time() - starttime) % 1.0))

if __name__ == '__main__':
    main()
