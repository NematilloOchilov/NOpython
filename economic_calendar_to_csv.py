from time import sleep
import pandas as pd
from selenium import webdriver
browser = webdriver.Firefox(firefox_profile=webdriver.FirefoxProfile())
browser.get('https://www.mql5.com/en/economic-calendar')
sleep(3)
soup = browser.find_elements_by_xpath(".//div[@class='ec-table__body']")[0]
rows = []
for i in soup.find_elements_by_class_name('ec-table__item'):
    date = i.find_elements_by_xpath(".//div[@class='ec-table__col ec-table__col_time']")[0].text
    currency = i.find_elements_by_xpath(".//div[@class='ec-table__col ec-table__col_currency']")[0].text
    event = i.find_elements_by_xpath(".//div[@class='ec-table__col ec-table__col_event']")[0].text
    actual = i.find_elements_by_xpath(".//div[@class='ec-table__group-right'][1]")[0].text.split('\n')[0]
    forecast = i.find_elements_by_xpath(".//div[@class='ec-table__col ec-table__col_forecast']")[0].text
    previous = i.find_elements_by_xpath(".//div[@class='ec-table__col ec-table__col_previous']")[0].text
    rows.append([date, currency, event, actual, forecast, previous])

browser.close()
df = pd.DataFrame(rows, columns=['Date', 'Currency', 'Event', 'Actual', 'Forecast', 'Previous'])
df.to_csv('news.csv', sep='\t', encoding='utf-8')
