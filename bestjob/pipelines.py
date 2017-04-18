# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
import pymysql
import maya
import re


from scrapy.exceptions import DropItem


def parse_create_time(create_time):
    try:
        t = maya.parse(create_time).iso8601()
    except TypeError:
        # print create_time
        t = datetime.strptime(create_time, '%m-%d').isoformat()
        # print t
    return t


def parse_zl_salary(salary):
    s = salary.split('-')
    if len(s) != 2:
        return 0, 0, 0, 0
    s_min = int(s[0]) / 1000
    s_max = int(s[1]) / 1000
    s_avg = (s_min + s_max) / 2
    ss = "{0}k-{1}k".format(s_min, s_max)
    return ss, s_min, s_max, s_avg


def parse_lg_salary(salary):
    s = re.findall('\d+', salary)
    if len(s) != 2:
        return 0, 0, 0, 0
    s_min = int(s[0])
    s_max = int(s[1])
    s_avg = (s_min + s_max) / 2
    return salary, s_min, s_max, s_avg


def parse_51_salary(salary):
    if '/' not in salary:
        return 0, 0, 0, 0
    unit = salary.split('/')[0][-1] == u'千' and 1.0 or 10.0
    if salary.split('/')[1][0] == u'年':
        unit /= 12
    elif salary.split('/')[1][0] == u'月':
        unit /= 1
    else:
        return 0, 0, 0, 0
    salaries = re.findall('\d+\.?\d*', salary)
    if len(salaries) == 1:
        s_min = int(float(salaries[0]) * unit)
        s_max = s_min
        s_avg = s_min
    elif len(salaries) == 2:
        s_min = int(float(salaries[0]) * unit)
        s_max = int(float(salaries[1]) * unit)
        s_avg = (s_min + s_max) / 2
    else:
        s_min, s_max, s_avg = 0, 0, 0
    s = "{0}k-{1}k".format(s_min, s_max)
    return s, s_min, s_max, s_avg


class BestJobPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1', user='root', password='666offer', db='bestjob', charset='utf8')
        self.table = 'jobs'
        self.seen = self.ids_seen()

    def ids_seen(self):
        with self.db.cursor() as cursor:
            sql = 'select position_id from %s' % self.table
            cursor.execute(sql)
            cols = cursor.fetchall()
        return [x[0] for x in cols]

    def process_item(self, item, spider):
        try:
            if int(item['position_id']) in self.ids_seen():
                raise DropItem("Duplicate item found: %s" % item)
            if spider.name == 'lg':
                item['salary'], item['salary_min'], item['salary_max'], item['salary_avg'] = parse_lg_salary(item['salary'])
            elif spider.name == 'zl':
                item['salary'], item['salary_min'], item['salary_max'], item['salary_avg'] = parse_zl_salary(item['salary'])
            elif spider.name == '51job':
                item['salary'], item['salary_min'], item['salary_max'], item['salary_avg'] = parse_51_salary(item['salary'])
            else:
                raise DropItem("Error item salary found: %s" % item)
            if item['salary_min'] == 0 or item['salary_min'] >= 50:
                raise DropItem("Error item found: %s" % item)

            item['create_time'] = parse_create_time(item['create_time'])
        except ValueError:
            raise DropItem("Duplicate item found: %s" % item)

        try:
            with self.db.cursor() as cursor:
                # Create a new record
                columns = ", ".join(item.fields)
                values_template = ", ".join(["%s"] * len(item.fields))
                values = tuple(item[k] for k in item.fields)

                sql = "INSERT INTO %s (%s) VALUES (%s)" % (self.table, columns, values_template)
                cursor.execute(sql, values)
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.db.commit()
        except:
            self.db.rollback()
        return item

