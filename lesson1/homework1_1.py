# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import json
import requests

main_link = 'https://api.github.com'
#header = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
username = 'skobsvetlana'

response = requests.get(f'{main_link}/users/{username}/repos')
data = json.loads(response.text)

with open('user_repos.json', 'w') as f:
    json.dump(data, f)