import requests
from bs4 import BeautifulSoup

mandatview = []
band = {"b": 0}


def get_table(url):
    rows = {}
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent": USER_AGENT}
    page = requests.get(url, headers=headers)
    soup1 = BeautifulSoup(page.text, 'html.parser').find_all('table', class_='table')[0].find_all('tr')[
        1].find_all('td')
    ball = str(soup1[4].text).replace(',', '.')
    if ball == 'Qiymatlanmagan!':
        return False
    link = 'https://mandat.dtm.uz' + str(soup1[7].find('a')['href'])
    fio = soup1[1].text
    rows["fio"] = fio
    rows["ball"] = ball
    rows["home_url"] = url
    page = requests.get(link, headers=headers)
    soup2 = BeautifulSoup(page.text, 'html.parser')
    soup3 = soup2.find_all('table', class_='table table-responsive table-bordered')[0].find_all('tr')
    for y, child in enumerate(soup3[2:]):
        row = {}
        gk = 0
        child = child.find_all('td')
        key = ["yun_num", "otm", "yunalish", "faculity", "grant", "kontrakt"]
        for x, td in enumerate(child[:-3]):
            try:
                tx = td.text.replace('\n', '')
                row[key[x]] = tx
            except:
                continue
        try:
            gk = int(row["grant"]) + int(row["kontrakt"])
        except ValueError:
            if row["grant"] == '-':
                gk = int(row["kontrakt"])
            elif row["kontrakt"] == '-':
                gk = int(row["grant"])
        row["gk"] = gk
        page = 1
        if gk > 10:
            page = str((gk // 10) + 1)
        qator = int(str(gk)[-1])
        if qator == 0:
            qator = 10
        link1 = 'https://mandat.dtm.uz' + str(child[8].find('a')['href']).replace('®', '&reg')
        link1 = link1.replace('AfterFilter?name=', f'AfterFilter?page={page}&name=')
        soup4 = BeautifulSoup(requests.get(link1, headers=headers).text, 'html.parser')
        abt_soni = soup4.find_all('div', class_='alert')[0].find_all('b')[2].text
        soup5 = soup4.find_all('div', class_='table-responsive')[0].find_all('tr')
        minball = float(soup5[qator].find_all('td')[4].text.replace(',', '.'))
        row["minball"] = minball
        row["abt_soni"] = abt_soni
        row["url"] = link1
        rows[y] = row
    return rows

text = <ID_RAQAM>

if band["b"] == 0:
  Url = r'https://mandat.dtm.uz/Home/AfterFilter?name=%s' % str(text)
  await message.reply_text(f"Iltimos 20 soniya kuting...\n<a href='{Url}'>Manba</a> ")
  try:
      band["b"] = 1
      await bot.send_chat_action(chat_id, "typing")
      gt = get_table(Url)
      if gt is False:
          await message.reply_text("Ushbu abituriyant test sinovlarida qatnashmagan")
      else:
          c = list(gt.items())
          send = f"F.I.O: {c[0][1]}\nUmumiy ball: {str(c[1][1])}\nHavola: {c[2][1]}\n\n"
          for i in c[3:]:
              v = i[1]
              send += f"\n-----------\nYo'nalish raqami: {v['yun_num']}\nOTM: {v['otm']}\nYo'nalish: <a href='{v['url']}'>{v['yunalish']}</a>\nShifri: {v['faculity']}\n\nQabul rejasi\nDavlat granti: {v['grant']}\nTo'lov shartnoma: {v['kontrakt']}\nJami: {v['gk']}\n\n{v['gk']}-o'rinda turgan abituriyent to'plagan ball: {v['minball']}\nAbituriyentlar soni: {v['abt_soni']}"
          await message.reply_text(send, parse_mode="HTML")
          mandatview.append(user_id)
          band["b"] = 0
          return
  except IndexError:
      await message.reply_text("Noto'g'ri ID raqam kiritdingiz")
      mandatview.append(user_id)
      band["b"] = 0
  except Exception as ex:
      band["b"] = 0
      await bot.send_message(-1001216448130, "mandat\n{}".format(str(ex)))
else:
  await message.reply_text("Hozir serverlar band, 60 soniyadan keyin qaytadan urinib ko'ring")

