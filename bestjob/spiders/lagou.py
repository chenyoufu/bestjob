# *-* coding:utf-8 *-*

import json
import scrapy
import time
import random
import requests
from bestjob.items import BestJobItem


class LgSpider(scrapy.Spider):
    name = 'lg'
    allowed_domins = ['lagou.com']
    start_urls = [
        "https://www.lagou.com"
    ]
    seeds = {
        'wuxi': 'https://www.lagou.com/gongsi/84-0-0.json',
        'suzhou': 'https://www.lagou.com/gongsi/80-0-0.json',
        'shanghai': 'https://www.lagou.com/gongsi/3-0-0.json',
        'hangzhou': 'https://www.lagou.com/gongsi/6-0-0.json',
        'nanjing': 'https://www.lagou.com/gongsi/79-0-0.json',
    }

    def __init__(self, city=None, *args, **kwargs):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'user_trace_token=20161216232858-d55af3950207433d8f7aa363ac9a76ff; LGUID=20161216232858-5d12c08d-c3a4-11e6-b15f-525400f775ce; TG-TRACK-CODE=index_navigation; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2Fchanpinzongjian%2F%3FlabelWords%3Dlabel; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=30; SEARCH_ID=51f62985cda44c409d5b40b8f612b77a; index_location_city=%E4%B8%8A%E6%B5%B7; login=false; unick=""; _putrc=""; JSESSIONID=85628EFE21CD9ECA73F06627C0BCFF63; _ga=GA1.2.1703120497.1481902153; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1488706452,1488958803,1488958889,1488958912; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1489845976; LGSID=20170318214512-1c3894de-0be1-11e7-94fd-5254005c3644; LGRID=20170318220616-0d46f8da-0be4-11e7-9500-5254005c3644'
        }
        self.city = city
        self.seed = self.seeds[city]

    def parse_companies(self, url, pn):
        payload = 'first=false&pn={0}&sortField=0&havemark=0'.format(pn)
        r = requests.post(url, headers=self.headers, data=payload)
        if r.encoding == 'ISO-8859-1':
            encodings = requests.utils.get_encodings_from_content(r.content)
            if encodings:
                r.encoding = encodings[0]
            else:
                r.encoding = r.apparent_encoding
        companies = json.loads(r.text)['result']
        return companies

    def parse(self, response):
        page_no = 1
        payload = 'first=false&pn={0}&sortField=0&havemark=0'.format(page_no)
        seed = self.seed
        r = requests.post(seed, headers=self.headers, data=payload)
        page_size = json.loads(r.text)['pageSize']
        total_count = int(json.loads(r.text)['totalCount'])
        print u'正在爬取{0}地区{1}个公司...'.format(self.city, total_count)

        for pn in range(1, total_count / page_size + 2):
            print u'总共{0}页，正在爬取第{1}页...'.format(total_count / page_size+1, pn)

            time.sleep(random.randint(20, 40))
            for c in self.parse_companies(seed, pn):
                url = 'https://www.lagou.com/gongsi/searchPosition.json'
                payload = 'companyId={0}&positionFirstType=%E6%8A%80%E6%9C%AF&pageNo=1&pageSize=20'.format(c['companyId'])
                # time.sleep(random.randint(10, 30))
                r = requests.post(url, headers=self.headers, data=payload)
                try:
                    jobs = json.loads(r.text)['content']['data']['page']['result']
                    for job in jobs:
                        item = BestJobItem()
                        item['company_id'] = job['companyId']
                        item['company_name'] = job['companyName']
                        item['url'] = 'https://www.lagou.com/jobs/{0}.html'.format(job['positionId'])
                        item['position_id'] = job['positionId']
                        item['position_name'] = job['positionName']
                        item['city'] = job['city']
                        item['salary'] = job['salary']
                        item['create_time'] = job['createTime']
                        item['source'] = u"拉钩网"
                        yield item
                except ValueError:
                    print r.text
        print u'爬取{0}地区{1}个公司完毕.'.format(self.city, total_count)