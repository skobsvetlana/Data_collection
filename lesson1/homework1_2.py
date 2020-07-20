# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию.
# Ответ сервера записать в файл.

import json
import requests

main_link = 'https://api.vk.com/method/users.get'

ID = 'skobsvetlana'
params = {'user_ids': '1',
          'access_token': 'fb7a3734fb7a3734fb7a373437fb1cd0ffffb7afb7a3734a0981e76dc218ad01203535e',
          'fields': 'verified, sex, bdate, city, country, home_town, online, has_mobile, contacts, site, education, '
                    'universities, schools, status, followers_count, occupation',
          'v': '5.110'}

#https://api.vk.com/method/METHOD_NAME?PARAMETERS&access_token=ACCESS_TOKEN&v=V

response = requests.get(main_link,params=params)
data = json.loads(response.text)

with open('vk.json', 'w') as f:
    json.dump(data, f)

