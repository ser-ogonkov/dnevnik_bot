import datetime
import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup

day = datetime.date.today()
schedule = f"Расписание на {datetime.date.day}:"

data = {}

driver = Chrome('chromedriver')
url = 'https://region.obramur.ru/?AL=Y'

driver.get(url)
sleep(1)

element = driver.find_element(by=By.ID, value='provinces')
provinces = element.text.split('\n')
data['provinces'] = provinces
element.send_keys("Городской округ Благовещенск")
element.send_keys(Keys.RETURN)
sleep(1)

element = driver.find_element(by=By.ID, value='cities')
cities = element.text.split('\n')
data['cities'] = cities
element.send_keys("Благовещенск, г.")
element.send_keys(Keys.RETURN)
sleep(1)

element = driver.find_element(by=By.ID, value='funcs')
element.send_keys("Общеобразовательная")
element.send_keys(Keys.RETURN)
sleep(1)

element = driver.find_element(by=By.ID, value='schools')
schools = element.text.split('\n')
element.send_keys('МАОУ "Алексеевская гимназия г.Благовещенска"')
element.send_keys(Keys.RETURN)
sleep(1)

element = driver.find_element(by=By.NAME, value='UN')
element.send_keys('ВасилецА4')
element.send_keys(Keys.RETURN)
sleep(1)

element = driver.find_element(by=By.NAME, value='PW')
element.send_keys('irjkfirjkf4')
element.send_keys(Keys.RETURN)
sleep(1)

print(provinces)
print(cities)
print(schools)

# driver.find_element(by=By.LINK_TEXT, value='Продолжить')
element = []
while not element:
    try:
        element = driver.find_element(by=By.LINK_TEXT, value='Продолжить')
    
element.send_keys(Keys.END)

element = []
while not element:
    element = driver.find_elements(by=By.CLASS_NAME, value='hidden-scr-sm')
[print(i.text) for i in element]
sleep(1)
