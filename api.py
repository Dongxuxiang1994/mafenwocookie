import json
from flask import Flask,g
from saver import *

GENERATOR_MAP = {
    'mafeng':'http://www.mafengwo.cn/friend/index/follow'
}

__all__ = ['app']

app = Flask(__name__)

@app.route('/')
def index():
    return '<h2>Welcome to Cookie Pool System</h2>'

def get_conn():
    for website in GENERATOR_MAP:
        print(website)
        #g是个全局对象
        if not hasattr(g,website):
            setattr(g,website+'_cookies',eval('RedisClient'+'("cookies","'+website+'")'))
            setattr(g, website + '_accounts', eval('RedisClient' + '("accounts","' + website + '")'))
        return g

@app.route('/<website>/random')
def random(website):
    '''
    获取随机的cookie,访问地址如/zhihu/random
    :param website:站点
    :return:随机cookie
    '''
    g = get_conn()
    cookies = getattr(g,website+'_cookies').random()
    return cookies

def add(website,username,password):
    '''
    添加用户，访问地址如/mafeng/add/user/password
    :param website: 站点
    :param username: 用户名
    :param password: 密码
    :return:
    '''
    g = get_conn()
    print(username,password)
    getattr(g,website+'_accounts').set(username,password)
    return json.dumps({'status':'1'})

@app.route('/<website>/count')
def count(website):
    '''
    获取cookies总数
    :param website:
    :return:
    '''
    g = get_conn()
    count = getattr(g,website+'_cookies').count()
    return json.dumps({'status': '1', 'count': count})
