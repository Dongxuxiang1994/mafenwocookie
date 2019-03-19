from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions as ex
import time


class MafengCookies():
    def __init__(self,username,password,browser):
        self.url = 'https://passport.mafengwo.cn/'
        self.browser = browser
        self.wait = WebDriverWait(self.browser,10)
        self.username = username
        self.password = password

    def open(self):
        '''
        打开网页并输入用户名与密码
        :return:
        '''
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.XPATH, '//form[@id="_j_login_form"]//input[@name="passport"]')))
        password = self.wait.until(EC.presence_of_element_located((By.XPATH, '//form[@id="_j_login_form"]//input[@name="password"]')))
        submit = self.wait.until(EC.presence_of_element_located((By.XPATH, '//form[@id="_j_login_form"]//div[@class="submit-btn"]/button')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        time.sleep(2)
        submit.click()

    def password_error(self):
        '''
        判断密码是否错误
        :return:
        '''
        try:
            return bool(
                WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.XPATH,'//div[@class="alert alert-danger"]')))
            )
        except ex.TimeoutException:
            return False

    def get_cookies(self):
        '''
        获取cookies
        :return:
        '''
        return self.browser.get_cookies()

    def login_successfully(self):
        '''
        判断是否登录成功
        :return:
        '''
        try:
            return bool(
                WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.XPATH,'//div[@class="user-image"]')))
            )
        except ex.TimeoutException:
            return False

    def main(self):
        self.open()
        time.sleep(5)
        if self.password_error():
            return{
                'status':2,
                'content':'用户名或密码错误'
            }
        elif self.login_successfully():
            cookies = self.get_cookies()
            return {
                'status':1,
                'content':cookies
            }
        else:
            return{
                'status':3,
                'content':'登录失败'
            }

