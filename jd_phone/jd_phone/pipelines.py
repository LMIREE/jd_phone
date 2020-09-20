from pymongo import MongoClient
from . import settings


class JdPhonePipeline(object):
    def __init__(self):
        # 获取setting中主机名，端口号和集合名
        host = '127.0.0.1'
        port = 27017
        dbname = 'JingDong'
        col = 'JingDongPhone'

        # 创建一个mongo实例
        client = MongoClient(host=host, port=port)

        # 访问数据库
        db = client[dbname]

        # 访问集合
        self.col = db[col]

    def process_item(self, item, spider):
        data = dict(item)
        self.col.insert(data)
        return item
