# *-* coding:utf-8 *-*

from bs4 import BeautifulSoup
import scrapy
from bestjob.items import BestJobItem


class Job51Spider(scrapy.Spider):
    name = '51job'
    allowed_domins = ['51job.com']
    start_urls = [
        "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=070400%2C00&district=000000&funtype=0100&industrytype=01&issuedate=9&providesalary=99&keywordtype=2&curr_page=2&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=0&confirmdate=9"
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        for div in soup.find("div", attrs={"class": "dw_table"}).find_all("div", attrs={"class": "el"}):
            if not div.find("a"):
                continue
            item = BestJobItem()
            item['company_id'] = \
            div.find("span", attrs={"class": "t2"}).find("a").attrs['href'].strip().split('/')[-1].split('.')[0][2:]
            item['company_name'] = div.find("span", attrs={"class": "t2"}).find("a").attrs['title'].strip()
            item['url'] = div.find("a").attrs['href'].strip()
            item['position_id'] = item['url'].split('/')[-1].split('.')[0]
            item['position_name'] = div.find("a").attrs['title'].strip()
            item['company_size'] = 0
            item['city'] = div.find("span", attrs={"class": "t3"}).text.strip()
            item['salary'] = div.find("span", attrs={"class": "t4"}).text.strip()
            item['work_year'] = 0
            item['education'] = 0
            item['create_time'] = div.find("span", attrs={"class": "t5"}).text.strip()
            item['source'] = self.name
            yield item

        next_page = soup.find("div", attrs={"class": "dw_page"}).find_all("li", attrs={"class": "bk"})[-1].find("a")
        if next_page is not None:
            np = next_page.attrs['href']
            yield scrapy.Request(np, callback=self.parse)
