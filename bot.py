import requests
from datetime import datetime


def handle_response(func):
    def wrapper(self, *args, **kwargs):
        response = func(self, *args, **kwargs)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Ошибка: {response.status_code}')
            return None
    return wrapper


class TelegramApiCommands:
    def __init__(self, token):
        self.token = token

    @handle_response
    def get_me(self):
        return requests.get(f'https://api.telegram.org/bot{self.token}/getMe')

    @handle_response
    def get_updates(self):
        return requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')

    def send_message(self, message):
        return requests.post(f'https://api.telegram.org/bot{self.token}/sendMessage', data=message)


get_updates = requests.get('https://api.telegram.org/bot6033278709:AAFazBge1Hc_z-FqyY4So05btPUwK7U7q7Y/getUpdates')
if get_updates.status_code == 200:
    data = get_updates.json()
    # Проверяем, что в "result" есть хотя бы один элемент
    if 'result' in data and len(data['result']) > 1:
        for item in data['result']:
            if 'message' in item and 'text' in item['message']:
                text = item['message']['text']
            if 'message' in item and 'date' in item['message']:
                date = item['message']['date']
                if date is not None:
                    print(str(datetime.fromtimestamp(date)) + '-' + text)
    else:
        print("В ответе нет сообщений.")
else:
    print(f'Ошибка: {get_updates.status_code}')
