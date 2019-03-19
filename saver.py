import random
import redis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None

class RedisClient(object):
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=2,decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        return "{type}:{website}".format(type=self.type,website=self.website)

    def set(self,username,value):
        '''
        设置键值对
        :param username: 用户名
        :param value: 密码或cookies
        :return:
        '''
        return self.db.hset(self.name(),username,value)

    def get(self,username):
        '''
        根据键名获取键值
        :param username: 用户名
        :return:
        '''
        return self.db.hget(self.name(),username)

    def delete(self,username):
        '''
        根据键名删除键值对
        :param username: 用户名
        :return: 删除结果
        '''
        return self.db.hdel(self.name(), username)

    def count(self):
        '''
        获取数目
        :return:数目
        '''
        return self.db.hlen(self.name())

    def random(self):
        '''
        随机获得键值，用户随机cookies获取
        :return: 随机Cookies
        '''
        return random.choice(self.db.hvals(self.name()))

    def usernames(self):
        '''
        获取所有账户信息
        :return: 所有用户名
        '''
        return self.db.hkeys(self.name())

    def all(self):
        '''
        获取所有键值对
        :return: 用户名和密码或cookies的映射表
        '''
        return self.db.hgetall(self.name())


