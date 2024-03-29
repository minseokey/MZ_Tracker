import sys
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from konlp.kma.klt2023 import klt2023
import demoji


def remove_emoji(content):
    content = demoji.replace(content, '')
    return content


def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def insta_searching(word):
    url = "https://www.instagram.com/explore/tags/" + str(word)
    return url


def select_first(driver):
    first = driver.find_element(By.CLASS_NAME, "_aagu")
    first.click()
    time.sleep(2)


def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    try:
        content = remove_emoji(soup.select('div._a9zs')[0].text)

    except:
        content = ''

    tags = re.findall(r'#[^\s#,\\]+', content)
    data = [content, tags if tags else []]
    return data


def move_next(driver):
    right = driver.find_element(By.CLASS_NAME, "_aaqg._aaqh")
    right.click()
    time.sleep(1)


# driver = webdriver.Chrome('chromedriver.exe')
driver = set_chrome_driver()
driver.get('https://www.instagram.com')
time.sleep(2)

email = "" # 인스타그램 아이디 입력
password = "" # 인스타그램 비밀번호 입력
input = driver.find_elements(By.TAG_NAME, 'input')

input[0].send_keys(email)
input[1].send_keys(password)

input[1].send_keys(Keys.RETURN)
time.sleep(5)

btn_later1 = driver.find_element(By.CLASS_NAME, '_ac8f')
btn_later1.click()
time.sleep(1)

btn_later2 = driver.find_element(By.CLASS_NAME, '_a9--._a9_1')
btn_later2.click()
time.sleep(1)

word = ""# 검색할 헤쉬테그 입력.
url = insta_searching(word)

driver.get(url)
time.sleep(10)

select_first(driver)

result = []
target = 3
k = klt2023()

try:
    for i in range(target):
        try:
            data = get_content(driver)
            result.append(data)
            move_next(driver)
        except:
            time.sleep(1)
            move_next(driver)
        time.sleep(1)

    sys.stdout = open("data/return.txt", 'w', encoding='UTF-8')
    for i in result:
        print(*k.nouns(i[0]), *i[1])
    sys.stdout.close()
except:
    print("emergency...")
    sys.stdout = open("data/return.txt", 'w', encoding='UTF-8')
    for i in result:
        print(*k.nouns(i[0]), *i[1])
    sys.stdout.close()
