# *-* coding:utf-8 *-*


from bs4 import BeautifulSoup
import scrapy
from bestjob.items import BestJobItem

class LgSpider(scrapy.Spider):
    name = 'lg'
    allowed_domins = ['lagou.com']
    start_urls = [
        "https://www.lagou.com/gongsi/84-0-0.json"
    ]

