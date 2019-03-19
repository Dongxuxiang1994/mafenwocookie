from saver import RedisClient
import json
import requests

TEST_URL_MAP = {
    'mafeng' : 'http://www.mafengwo.cn/friend/index/follow'
}

class ValidTester(object):
    def __init__(self,website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies',self.website)
        self.accounts_db = RedisClient('accounts',self.website)
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

    def test(self,username,cookies):
        raise NotImplementedError

    def run(self):
        cookies_groups = self.cookies_db.all()
        for username,cookies in cookies_groups.items():
            self.test(username,cookies)

class MafengValidTester(ValidTester):
    def __init__(self, website='mafeng'):
        ValidTester.__init__(self,website)

    def test(self,username,cookies):
        print('正在测试Cookies','用户名',username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies不合法',username)
            self.cookies_db.delete(username)
            print('删除Cookies',username)
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url,headers=self.header,cookies=cookies,timeout=5, allow_redirects=False)
            if response.status_code == 200:
                print('Cookies有效',username)
            else:
                print(response.status_code,response.headers)
                print('Cookies失效',username)
                self.cookies_db.delete(username)
                print('删除Cookies',username)
        except ConnectionError as e:
            print('发生异常',e.args)
