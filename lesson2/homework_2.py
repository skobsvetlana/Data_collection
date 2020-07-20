#1) Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайта superjob.ru и hh.ru.
# Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы). Получившийся список должен содержать
# в себе минимум:

#    *Наименование вакансии
#    *Предлагаемую зарплату (отдельно мин. и отдельно макс. и отдельно валюта)
#    *Ссылку на саму вакансию
#    *Сайт откуда собрана вакансия
#По своему желанию можно добавить еще работодателя и расположение. Данная структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas.

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd
import re
import json


def comp_distribution(text = ''):
    res = {'min_compensation': None, 'max_compensation': None, 'currency': None}
    if text == '':
        return res
    text = re.sub(r'[\.\s]', "", text)
    text = re.split('(\d+)', text)
    res['currency'] = text.pop()
    if len(text) == 4:
        res['min_compensation'] = int(text[1])
        res['max_compensation'] = int(text[3])
    if len(text) == 2:
        if text[0].lower() == 'от':
            res['min_compensation'] = int(text[1])
        if text[0].lower() == 'до':
            res['max_compensation'] = int(text[1])
    return res


def get_pos_id (link):
    return re.search(r'(\d+)', link).group()


columns = ['_id', 'Position_name', 'Employer_name', 'City', 'Position_link', 'Source', 'Min_compensation',
           'Max_compensation', 'Currency']
df = pd.DataFrame(columns=columns)

main_link = 'https://hh.ru/search/vacancy'

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
          'Accept':'*/*'}

params = {'L_save_area': 'true',
          'clusters': 'true',
          'enable_snippets': 'true',
          'text': 'Python',
          'showClusters': 'true'}

response = requests.get(main_link + '/search/vacancy', headers=header, params=params).text
soup = bs(response, 'lxml')

data_to_db = []

while True:

    vacancy_block = soup.find('div', {'class': 'vacancy-serp'})

    vacancy_list_premium = vacancy_block.find_all('div',
                                                  {'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_premium'})
    for vacancy in vacancy_list_premium:
        vacancy_data = {}

        vacancy_data['Position_name'] = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'}).getText()
        vacancy_data['Employer_name'] = vacancy.find('a', {'class': 'bloko-link bloko-link_secondary'}).getText()
        vacancy_data['City'] = vacancy.find('span', {'class': 'vacancy-serp-item__meta-info'}).getText()
        pos_link = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
        vacancy_data['Position_link'] = pos_link
        vacancy_data['_id'] = main_link + '_' + get_pos_id(pos_link)
        vacancy_data['Source'] = main_link
        compensation_data = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()
        compensation_data = comp_distribution(compensation_data)
        vacancy_data['Min_compensation'] = compensation_data['min_compensation']
        vacancy_data['Max_compensation'] = compensation_data['max_compensation']
        vacancy_data['Currency'] = compensation_data['currency']

        data_to_db.append(vacancy_data)
        df = df.append(pd.Series(vacancy_data, index=df.columns), ignore_index=True)

    vacancy_list = vacancy_block.find_all('div', {'data-qa': 'vacancy-serp__vacancy'})
    for vacancy in vacancy_list:

        vacancy_data['Position_name'] = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'}).getText()
        employer_name = vacancy.find('a', {'class': 'bloko-link bloko-link_secondary'})
        if employer_name:
            vacancy_data['Employer_name'] = employer_name.getText()
        else:
            vacancy_data['Employer_name'] = None
        vacancy_data['City'] = vacancy.find('span', {'class': 'vacancy-serp-item__meta-info'}).getText()
        pos_link = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
        vacancy_data['Position_link'] = pos_link
        vacancy_data['_id'] = main_link + '_' + get_pos_id(pos_link)
        vacancy_data['Source'] = main_link
        compensation_data = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()
        compensation_data = comp_distribution(compensation_data)
        vacancy_data['Min_compensation'] = compensation_data['min_compensation']
        vacancy_data['Max_compensation'] = compensation_data['max_compensation']
        vacancy_data['Currency'] = compensation_data['currency']

        data_to_db.append(vacancy_data)
        df = df.append(pd.Series(vacancy_data, index=df.columns), ignore_index=True)

    next_page_link_block = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})

    if not next_page_link_block:
        break

    next_page_link = next_page_link_block['href']
    response = requests.get(main_link + next_page_link, headers=header).text
    soup = bs(response, 'lxml')

print(df.head(5))

print(df.describe())

path = '/Users/svetlanaskobeltcyna/PycharmProjects/Data_collection_methods/lesson2/'
df.to_csv(path + 'hh_vacancy_data.csv', index=False)

with open(path + 'vacancy_data.json', 'w') as f:
    json.dump(data_to_db, f)

len(data_to_db)