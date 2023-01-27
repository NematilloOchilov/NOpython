
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import datetime
import csv

driver = webdriver.Firefox()
driver.get("https://tradingeconomics.com/calendar")
sleep(3)
xpath = "/html/body/form/div[4]/div/div/"
driver.find_element_by_xpath(xpath + "table/tbody/tr/td[1]/div/div[2]/button").click()  # impact
driver.find_element_by_xpath(xpath + "table/tbody/tr/td[1]/div/div[2]/ul/li[2]/a").click()  # impact 2
sleep(1)
driver.find_element_by_xpath(xpath + "table/tbody/tr/td[1]/div/button").click()  # event
driver.find_element_by_xpath(xpath + "span/div/div[2]/div[1]").click()  # clear
driver.find_element_by_xpath(xpath + "span/div/span/ul[4]/li[27]").click()  # us
sleep(2)
element = driver.find_element_by_xpath(xpath + "span/div/div[2]/div[3]/a")  # us save
driver.execute_script("arguments[0].click();", element)
sleep(2)

driver.find_element_by_xpath(xpath + "table/tbody/tr/td[1]/div/div[1]/button").click()
sleep(2)
driver.find_element_by_xpath(xpath + "table/tbody/tr/td[1]/div/div[1]/ul/li[12]/a").click()
start_elem = driver.find_element_by_xpath('//*[@id="startDate"]')
end_elem = driver.find_element_by_xpath('//*[@id="endDate"]')
sleep(3)
start_elem.clear()
start_elem.send_keys(datetime.datetime(2022, 1, 1).strftime("%Y-%m-%d"))
start_elem.send_keys(Keys.TAB)
end_elem.clear()
end_elem.send_keys(datetime.datetime(2023, 1, 10).strftime("%Y-%m-%d"))
end_elem.send_keys(Keys.TAB)
btn = driver.find_element_by_xpath("/html/body/form/div[4]/div/div/div[1]/div/span[3]/button")
btn.send_keys(Keys.RETURN)
sleep(5)
calender_html = driver.find_element_by_xpath("/html/body/form/div[4]/div/div/div[3]").get_attribute('innerHTML')
soup = BeautifulSoup(calender_html, "html.parser")
dates = ''
rows = []
for tag in soup.find_all():
    if tag.name == 'thead':
        if str(tag).startswith('<thead class="table-header"'):
            tm = tag.text.strip().split('\n')[0].split(' ')
            dates = datetime.datetime.strptime(f'{tm[3]} {tm[2]} {tm[1]}', '%Y %d %B').strftime("%Y.%m.%d ")
    elif tag.name == 'tbody':
        if str(tag).startswith('<tbody><tr '):
            for tr in tag.find_all('tr'):
                row = tr.find_all('td')
                if str(row[0]).startswith('<td style="white-space: nowrap;">\n<span class="calendar-date-'):
                    times = row[0].text.strip().split(' ')
                    if times[1] == 'PM':
                        times = str(int(times[0][:2]) + 12) + times[0][2:5]
                    else:
                        times = times[0]
                    previous = row[6].text if not ('\n' in row[6].text) else row[6].text.split('\n')[0]
                    rows.append(
                        [
                            dates + times,  # date
                            row[3].text.strip(),  # currency
                            row[4].text.strip(),  # event
                            previous.strip(),  # previous
                            row[8].text.strip(),  # forecast
                            row[5].text.strip(),  # actual
                            row[7].text.strip(),  # consensus
                        ]
                    )

driver.close()
df = pd.DataFrame(rows, columns=['Time', 'Currency', 'Event', 'Previous', 'Forecast', 'Actual', 'Consensus'])
df.to_csv('calendar_tradingeconomics.csv', sep='\t', encoding='utf-8')
