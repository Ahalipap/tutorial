import json
import time
import scrapy

from tutorial.items import FundCompanyItem


class FundCompaniesSpider(scrapy.Spider):
    name = 'fund_company_spider'
    start_urls = [
        rf'http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=zdf,desc&page={i},200&dt={int(time.time())}&atfc=&onlySale=0'
        for i in range(1, 40)]

    def parse(self, response):
        items = []
        datas = response.body_as_unicode()
        datas = datas.split('var ')[1].split('db=')[1].split('datas:')[1]
        data_list = datas.split('],')
        for v in data_list:
            if v.split(',').__len__() != 21:
                continue
            else:
                fond_code = v.split(',')[0].replace('[', '').replace('"', '')
                fond_company_name = v.split(',')[1].replace('"', '')
                item = FundCompanyItem()
                item['code'] = fond_code
                item['name'] = fond_company_name
                items.append(item)
        return items
# def main():
#     print('task FundCompaniesSpider start')
#
#     for i in range(1, 41):
#         async with aiohttp.ClientSession() as session:
#             html = await fetch(session,
#                                rf'http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=zdf,desc&page={i},200&dt={int(time.time())}&atfc=&onlySale=0')
#             datas = html.split('var ')[1].split('db=')[1].split('datas:')[1]
#             data_list = datas.split('],')
#             for v in data_list:
#                 if v.split(',').__len__() != 21:
#                     continue
#                 else:
#                     fond_code = v.split(',')[0].replace('[', '').replace('"', '')
#                     fond_company_name = v.split(',')[1].replace('"', '')
#                     UUID = uuid.uuid5(namespace=uuid.NAMESPACE_OID,
#                                       name=fond_code.__str__() + fond_company_name).__str__()
#                     await FundCompaniesModel(
#                         uuid=UUID, fond_code=fond_code,
#                         fond_company_name=fond_company_name).replace()
#     print('task FundCompaniesSpider finished')
