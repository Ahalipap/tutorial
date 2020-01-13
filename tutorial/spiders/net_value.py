import json
import time

import pymongo
import scrapy

from tutorial import settings
from tutorial.items import FundCompanyItem, Net


def get_codes():
    host = settings.MONGODB_HOST
    port = settings.MONGODB_PORT
    dbname = settings.MONGODB_DBNAME

    # 创建数据库连接
    client = pymongo.MongoClient(host=host, port=port)

    # 指向指定数据库
    mdb = client[dbname]

    # 获取数据库里面存放数据的表名
    collections = mdb['fund_company']
    res_list = []
    for v in collections.find({}):
        res_list.append(v.get('code'))
    return res_list


if __name__ == '__main__':
    get_codes()


class NetValueSpider(scrapy.Spider):
    name = 'net_value_spider'


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
        print(len(items))
        return items


"""
class ScrapySpider(scrapy.Spider):
    name = "scrapy_spider"
    allowed_domains = ["httpbin.org"]

    start_urls = (
        "https://httpbin.org/get?show_env=1",
    )
    # 新加的代码
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={"User-Agent": USER_AGENT})
    # ------------

    def parse(self, response):
        print response.text
"""
