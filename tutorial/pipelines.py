# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from tutorial import settings
from twisted.internet import reactor, defer

# 获取setting主机名、端口号和数据库名称
from tutorial.settings import MONGODB_DBNAME

host = settings.MONGODB_HOST
port = settings.MONGODB_PORT
dbname = settings.MONGODB_DBNAME
# 创建数据库连接
client = pymongo.MongoClient(host=host, port=port)
# 指向指定数据库
mdb = client[dbname]

NetValueList = list()


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class FundCompanyPipeline(object):

    def __init__(self):
        # 获取数据库里面存放数据的表名
        self.post = mdb['fund_company']

    def process_item(self, item, spider):
        data = dict(item)
        # 向指定的表里添加数据
        self.post.replace_one(replacement=data, filter=data, upsert=True)
        return item


class NetValuePipeline(object):

    def __init__(self, mongo_uri, mongo_db, mongo_col):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_col = mongo_col

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri='mongodb://127.0.0.1:27017/',
            mongo_db=MONGODB_DBNAME,
            mongo_col='net_value',
        )

    def open_spider(self, spider):
        """
        爬虫启动时，启动
        :param spider:
        :return:
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.mongodb = self.client[self.mongo_db]

    def close_spider(self, spider):
        """
        爬虫关闭时执行
        :param spider:
        :return:
        """
        self.client.close()

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        out = defer.Deferred()
        reactor.callInThread(self._insert, item, out, spider)
        yield out
        defer.returnValue(item)

    def _insert(self, item, out, spider):
        """
        插入函数
        :param item:
        :param out:
        :return:
        """
        self.mongodb[self.mongo_col].replace_one(replacement=dict(item), filter=dict(item), upsert=True)
        reactor.callFromThread(out.callback, item)
