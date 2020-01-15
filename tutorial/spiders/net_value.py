import json
import time

import pymongo
import scrapy

from tutorial import settings
from tutorial.items import Net


class NetValueSpider(scrapy.Spider):
    name = 'net_value_spider'

    def get_codes(self):
        # 获取数据库里面存放数据的表名
        collections = self.mdb['fund_company']
        res_list = []
        for v in collections.find({}):
            res_list.append(v.get('code'))
        return res_list

    def __init__(self, **kwargs):
        # 获取setting主机名、端口号和数据库名称
        super().__init__(**kwargs)
        self.host = settings.MONGODB_HOST
        self.port = settings.MONGODB_PORT
        self.dbname = settings.MONGODB_DBNAME
        # 创建数据库连接
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        # 指向指定数据库
        self.mdb = self.client[self.dbname]

    # 重写start_requests方法
    def start_requests(self):
        code_list = get_codes()
        headers = {
            'Referer': 'http://fundf10.eastmoney.com/'
        }
        start_urls = [
            rf'http://api.fund.eastmoney.com/f10/lsjz?fundCode={v}&pageIndex=1&pageSize=10000&startDate=&endDate=&_={time.time()}'
            for v in code_list]
        for url in start_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        items = []
        datas = response.body_as_unicode()
        datas = json.loads(datas)

        data_list = datas.get('Data', {}).get('LSJZList', [])
        for v in data_list:
            item = Net()
            item['code'] = str(response.request.url).split('http://api.fund.eastmoney.com/f10/lsjz?fundCode=')[1].split(
                '&pageIndex=1&pa')[0]
            item['datetime'] = v['FSRQ']
            item['unit_net'] = v['DWJZ']
            item['accumulated_net'] = v['LJJZ']  # 累计净值
            item['daily_growth_rate'] = v['JZZZL']  # 日增长率
            items.append(item)
        item_list = [dict(v) for v in items]
        for v in item_list:
            self.mdb['net_value'].replace_one(filter=v, replacement=v, upsert=True)
        print('len====', item_list.__len__())
        # print(self.mdb['net_value'].insert_many(item_list))
        return items[0]
