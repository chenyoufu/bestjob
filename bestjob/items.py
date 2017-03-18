# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BestJobItem(scrapy.Item):

    company_id = scrapy.Field()
    company_name = scrapy.Field()

    position_id = scrapy.Field()
    position_name = scrapy.Field()

    create_time = scrapy.Field()

    salary = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    salary_avg = scrapy.Field()

    city = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()

