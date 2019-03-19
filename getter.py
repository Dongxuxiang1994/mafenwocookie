import json
from selenium import webdriver
from saver import RedisClient
from cookie import MafengCookies


class CookiesGenerator(object):
    def __init__(self,website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies',self.website)
        self.account_db = RedisClient('accounts',self.website)
        self.init_browser()

    def __del__(self):
        self.close()

    def init_browser(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('headless')
        self.browser = webdriver.Chrome()

    def new_cookies(self,username,password):
        '''
        新生成Cookies,子类需要重写
        :param username: 用户名
        :param password: 密码
        :return:
        '''
        raise NotImplementedError

    def process_cookies(self,cookies):
        '''
        处理Cookies
        :param cookies:
        :return:
        '''
        dict = {}
        for cookie in cookies:
            dict[cookie['name']] = cookie['value']
        return dict

    def run(self):
        accounts_usernames = self.account_db.usernames()
        cookies_usenames = self.cookies_db.usernames()

        #找出没有Cookies的账号
        for username in accounts_usernames:
            if not username in cookies_usenames:
                password = self.account_db.get(username)
                print('正在生成Cookies','账号',username,'密码','---')
                result = self.new_cookies(username,password)

                if result.get('status') == 1:
                    cookies = self.process_cookies(result.get('content'))
                    print('成功获取到Cookies',cookies)
                    if self.cookies_db.set(username,json.dumps(cookies)):
                        print('成功保存Cookies')
                #密码错误，移除账号
                elif result.get('status') == 2:
                    print(result.get('content'))
                    if self.account_db.delete(username):
                        print('成功删除帐号')
                else:
                    print(result.get('content'))
        else:
            print('所有账号都已经成功获取Cookies')

    def close(self):
        try:
            print('Closing Browser')
            self.browser.close()
            del self.browser
        except TypeError:
            print('Brower not opened')


class MafengCookiesGenerator(CookiesGenerator):
    def __init__(self, website='mafeng'):
        CookiesGenerator.__init__(self,website)
        self.website = website
    def new_cookies(self, username, password):
        return MafengCookies(username, password,self.browser).main()

