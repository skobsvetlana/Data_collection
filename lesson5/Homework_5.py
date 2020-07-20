# 1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить
# данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172

from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def get_mail_from_mail_ru():
    chrome_options = Options()
    chrome_options.add_argument('start-maximized')

    driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    driver.get('https://mail.ru/')

    elem = driver.find_element_by_id('mailbox:login')
    elem.send_keys('study.ai_172@mail.ru')

    time.sleep(3)
    elem = driver.find_element_by_id('mailbox:submit')
    elem.click()

    time.sleep(3)
    #elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mailbox:password')))
    elem = driver.find_element_by_id('mailbox:password')
    elem.send_keys('NextPassword172')

    elem.send_keys(Keys.ENTER)

    time.sleep(20)
    letters = driver.find_elements_by_xpath("//a[@class='llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal']")

    for letter in letters:
        try:
            letter_link = letter.get_attribute('href')
            pprint(letter_link)
            #driver.get(letter_link)
            #letter_link.click()

        except:
            print('Парсинг окончен')

# 2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

def get_from_mvideo_bestsellers():
    chrome_options = Options()
    chrome_options.add_argument('start-maximized')

    driver = webdriver.Chrome('/./chromedriver',
                              options=chrome_options)
    driver.get('https://www.mvideo.ru/')

    block_xpath = "//div[@class='section']"
    #block_xpath = "//div[@class='gallery-content accessories-new ']"

    pages = 0
    bestsellers_block = ''
    i = 1
    while bestsellers_block != 'Хиты продаж':
        time.sleep(5)
        blocks = driver.find_elements_by_xpath(block_xpath)
        actions = ActionChains(driver)
        actions.move_to_element(blocks[i + 1])
        actions.perform()
        i += 1
        try:
            bestsellers_block = blocks[i].find_element_by_class_name('h2').text
            pprint(bestsellers_block)
            time.sleep(5)
        except:
            continue
    else:
        while True:
            try:
                print('111111112')
                # button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'next-btn sel-hits-button-next')))
                button = blocks[i - 1].find_element_by_xpath("//a[@class='next-btn sel-hits-button-next']/@href")
                pprint(button)
                action = ActionChains(button)
                action.move_to_element(button).perform()
                # button = driver.find_element_by_xpath("//a[@class='next-btn sel-hits-button-next']/@href")

                button.click()
                pages += 1
            except:
                print(f'Всего {pages} страниц')
                break

    #bestsellers_text = driver.find_element_by_xpath("//div[contains(text(), 'Хиты продаж')]")

    #time.sleep(10)
    #bestsellers_block = driver.find_element_by_xpath("//div[./div[./div[./div[contains(text(), 'Хиты продаж')]]]]//li[@class='gallery-list-item height-ready']")

    # xpath = "//div[./div[./div[./div[contains(text(), 'Хиты продаж')]]]]//li[@class='gc-product-tile sel-product-tile-main ']"
    # xpath = "//div[./div[./div[./div[contains(text(), 'Хиты продаж')]]]]"#//li[@class='gc-product-tile sel-product-tile-main ']"
    # bestsellers_block = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    #
    # action = ActionChains(bestsellers_block)
    # action.move_to_element(bestsellers_block).perform()





    # while True:
    #     try:
    #         #button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'next-btn sel-hits-button-next')))
    #
    #         bestsellers_block = WebDriverWait(bestsellers_block, 30).until(
    #             EC.presence_of_element_located((By.XPATH, "//div[@class='gallery-layout sel-hits-block ']")))
    #         action = ActionChains(bestsellers_block)
    #         action.move_to_element(bestsellers_block).perform()
    #         #button = driver.find_element_by_xpath("//a[@class='next-btn sel-hits-button-next']/@href")
    #
    #         #button.click()
    #         pages += 1
    #     except:
    #         print(f'Всего {pages} страниц')
    #         break
    #goods = driver.find_elements_by_class_name('sale-card')
    #for good in goods:
        # try:
        #     print(good.find_element_by_xpath("//a[@class='sel-product-tile-title']/@href"))
        #     print(good.find_element_by_xpath("//a[@class='sel-product-tile-title']/@data-product-info"))
        # except:
        #     print('Парсинг окончен')

    #driver.quit()





#get_from_mvideo_bestsellers()

get_mail_from_mail_ru()



