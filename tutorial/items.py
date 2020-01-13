# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FundCompanyItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()


class Net(scrapy.Item):
    code = scrapy.Field()
    datetime = scrapy.Field()
    unit_net = scrapy.Field()
    accumulated_net = scrapy.Field()  # 累计净值
    daily_growth_rate = scrapy.Field()  # 日增长率


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
