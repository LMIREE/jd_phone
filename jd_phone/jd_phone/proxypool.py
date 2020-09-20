import redis
import urllib.request as ur
import time


class ProxyPool():
    def __init__(self):
        # 创建一个Redis连接对象
        self.redis_conn = redis.StrictRedis(
            host='localhost',
            port=6379,
            decode_responses=True,
        )

    def set_proxy(self):
        proxy_old = None
        while True:
            proxy_new = ur.urlopen('http://api.ip.data5u.com/dynamic/get.html?order=58431fe2493da16c9884e2a69cd984fc&random=1&sep=3').read().decode('utf-8').strip().split(' ')
            if proxy_new != proxy_old:
                proxy_old = proxy_new
                self.redis_conn.delete('proxy')
                self.redis_conn.sadd('proxy',*proxy_new)
                print('更换代理ip为:',proxy_new)
                time.sleep(2)
            else:
                time.sleep(1)

    def get_proxy(self):
        proxy_s = self.redis_conn.srandmember('proxy',1)
        if proxy_s:
            return proxy_s[0]
        else:
            time.sleep(0.1)
            return self.get_proxy()

if __name__ == '__main__':
    ProxyPool().set_proxy()
    # ProxyPool().get_proxy()