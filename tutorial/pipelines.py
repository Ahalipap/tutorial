# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from tutorial import settings


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class FundCompanyPipeline(object):

    def __init__(self):
        # 获取setting主机名、端口号和数据库名称
        host = settings.MONGODB_HOST
        port = settings.MONGODB_PORT
        dbname = settings.MONGODB_DBNAME

        # 创建数据库连接
        client = pymongo.MongoClient(host=host, port=port)

        # 指向指定数据库
        mdb = client[dbname]

        # 获取数据库里面存放数据的表名
        self.post = mdb['fund_company']

    def process_item(self, item, spider):
        data = dict(item)
        # 向指定的表里添加数据
        self.post.replace_one(replacement=data, filter=data, upsert=True)
        return item


class NetValuePipeline(object):

    def __init__(self):
        # 获取setting主机名、端口号和数据库名称
        host = settings.MONGODB_HOST
        port = settings.MONGODB_PORT
        dbname = settings.MONGODB_DBNAME

        # 创建数据库连接
        client = pymongo.MongoClient(host=host, port=port)

        # 指向指定数据库
        mdb = client[dbname]

        # 获取数据库里面存放数据的表名
        self.post = mdb['net_value']

    def process_item(self, item, spider):
        data = dict(item)
        # 向指定的表里添加数据
        self.post.replace_one(replacement=data, filter=data, upsert=True)
        return item
