# *-* coding:utf-8 *-*

from bs4 import BeautifulSoup
import scrapy
from bestjob.items import BestJobItem


class ZlSpider(scrapy.Spider):
    name = 'zl'
    allowed_domins = ['zhaopin.com']
    start_urls = [
        "http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&in=160400&jl=%E6%97%A0%E9%94%A1&sm=0&p=1"
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        for table in soup.find("div", attrs={"id": "newlist_list_content_table"}).find_all("table", attrs={"class": "newlist"}):
            if not table.find("a"):
                continue
            item = BestJobItem()
            item['company_id'] = table.find("td", attrs={"class": "gsmc"}).find("a").attrs['href'].split('/')[-1].split('.')[0]
            item['company_name'] = table.find("td", attrs={"class": "gsmc"}).find("a").text.strip()
            item['url'] = table.find("a").attrs['href'].strip()
            item['position_id'] = item['url'].split('/')[-1].split('.')[0]
            item['position_name'] = table.find("a").text.strip()
            item['city'] = table.find("td", attrs={"class": "gzdd"}).text.strip()
            item['salary'] = table.find("td", attrs={"class": "zwyx"}).text.strip()
            item['create_time'] = table.find("td", attrs={"class": "gxsj"}).find("span").text.strip()
            item['source'] = u"智联招聘"
            yield item
        try:
            np = soup.find("div", attrs={"class": "pagesDown"}).find("a", attrs={"class": "next-page"}).attrs['href']
            yield scrapy.Request(np, callback=self.parse)
        except KeyError:
            return

