import re
import datetime
from time import sleep
import pandas as pd
from selenium import webdriver

weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
browser = webdriver.Firefox(firefox_profile=webdriver.FirefoxProfile())
browser.get('https://www.mql5.com/en/economic-calendar')  # file://D:/...mql5.html
sleep(3)

soup = browser.find_elements_by_xpath(".//div[@class='ec-table__body']")[0]
year = int(re.findall(r'[\d]{4}', soup.find_elements_by_xpath(
    ".//div[@class='ec-table__nav__item ec-table__nav__item_current']")[0].text)[-1])
date = ''
rows = []
for i in soup.find_elements_by_xpath('.//div')[6:]:
    sana = re.findall(r'[\d]+ [\w]{3,}, [a-zA-Z]{6,}', i.text)
    if len(sana) == 1:
        tm = sana[0].split(', ')
        years = 0
        for y in range(year + 1, year - 1, -1):
            if weekDays[datetime.datetime.strptime(f'{tm[0]} {str(y)}', "%d %B %Y").weekday()] == tm[1]:
                years = y
                break
        date = datetime.datetime.strptime(f'{str(years)} {tm[0]}', '%Y %d %B').strftime("%Y.%m.%d")
    else:
        event = i.find_elements_by_xpath(".//div[@class='ec-table__col ec-table__col_event']")
        if event:
            actual = ''
            for z in [
                'ec-table__col ec-table__col_actual ',
                'ec-table__col ec-table__col_actual  green',
                'ec-table__col ec-table__col_actual  red'
            ]:
                try:
                    actual = i.find_elements_by_xpath(f".//div[@class='{z}']")[0].text
                    if actual:
                        break
                except:
                    pass
            try:
                times = i.find_elements_by_xpath(".//div[@class='ec-table__col ec-table__col_time']")[0].text
                currency = i.find_elements_by_xpath(".//div[@class='ec-table__col ec-table__col_currency']")[0].text
                forecast = i.find_elements_by_xpath(".//div[@class='ec-table__col ec-table__col_forecast']")[0].text
                previous = i.find_elements_by_xpath(".//div[@class='ec-table__col ec-table__col_previous']")[0].text
                row = [date + ' ' + times.replace(' (tent.)', ''), currency, event[0].text, actual, forecast, previous]
                print(row)
                rows.append(row)
            except:
                pass

browser.close()
df = pd.DataFrame(rows, columns=['Time', 'Currency', 'Event', 'Actual', 'Forecast', 'Previous'])
df.to_csv('calendar_mql5.csv', sep='\t', encoding='utf-8')
