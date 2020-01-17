from apscheduler.schedulers.blocking import BlockingScheduler
from scrapy import cmdline

from tutorial.pipelines import NetValueList, NetValuePipeline


def job_fund_company_spider():
    cmdline.execute("scrapy crawl fund_company_spider".split())


def job_net_value_spider():
    cmdline.execute("scrapy crawl net_value_spider".split())


if __name__ == '__main__':
    # BlockingScheduler：在进程中运行单个任务，调度器是唯一运行的东西
    # scheduler = BlockingScheduler()
    # 采用阻塞的方式

    # 采用date的方式，在特定时间只执行一次
    # scheduler.add_job(job_net_value_spider, 'interval', seconds=3600)
    # scheduler.add_job(job_fund_company_spider, 'interval', seconds=3600)
    # scheduler.start()
    # job_fund_company_spider()
    # cmdline.execute("scrapy crawl fund_company_spider".split())
    cmdline.execute("scrapy crawl net_value_spider --nolog".split())
    # if NetValueList.__len__() != 0:
    #     NetValuePipeline.post.insert_many(documents=NetValueList)
    #     print('success')
