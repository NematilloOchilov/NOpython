from bs4 import BeautifulSoup
import requests
from time import sleep
import otm_dtm_data as general 

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
headers = {"user-agent": USER_AGENT}


for i in general:
    url = f"https://mandat.dtm.uz/Home/AfterFilter?name=&region={i['region']}&university={i['university']}&faculty={i['faculty']}&edLang={i['language']}&edType=1"
    try:
        soup4 = BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser').find_all('table', class_='table')[0].find_all('tr')[
            1].find_all('td')[0].text
        url1 = f"https://mandat.dtm.uz/Home/Details/{str(soup4)}"
        page = requests.get(url1, headers=headers)
        soup2 = BeautifulSoup(page.text, 'html.parser')
        soup3 = soup2.find_all('table', class_='table table-responsive table-bordered')[0].find_all('tr')
        natija = soup2.find_all('div', class_='alert alert-dismissible')[-1].find('h5').text.strip()
        dic = dict()
        for y, child in enumerate(soup3[2:]):
            row = {}
            gk = 0
            child = child.find_all('td')
            key = ["yun_num", "otm", "yunalish", "faculty", "grant", "kontrakt", "grant_", "kontrakt_"]
            for x, td in enumerate(child[:-1]):
                try:
                    tx = td.text.replace('\n', '')
                    row[key[x]] = tx
                except:
                    continue
            print(row['otm'], university[i['university']])
            # print(row['faculty'], i['faculty'])
            print(row)
            if row['otm'] == university[i['university']] and row['faculty'] == i['faculty']:
                dic = {
                    "name": i['name'],
                    "faculty": i['faculty'],
                    "university_code": i['university'],
                    "university": university[i['university']],
                    "emode": i['emode'],
                    "language": i['language'],
                    "region": i['region'],
                    "qabul_grant": row["grant"],
                    "qabul_kontrakt": row["kontrakt"],
                    "ball_grant": row["grant_"],
                    "ball_kontrakt": row["kontrakt_"]
                }
                break
        file = open('file.txt', 'a')
        file.write(str(dic) + ',')
        file.close()
    except Exception as ex:
        file = open('exceptexcept.txt', 'a')
        file.write(str(ex) + '\n' + url + '\n\n')
        file.close()
    sleep(1)
