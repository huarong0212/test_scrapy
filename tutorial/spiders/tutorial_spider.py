import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from tutorial.items import TutorialItem
import re
import sys
import random
import string
from scrapy.selector import Selector

sys.setrecursionlimit(1000000000)

class TutorialSpider(CrawlSpider):        #QuotesSpider类必须要继承scrapy.Spider类，你可以在这个类里面定义一些方法和属性。

    name = "tutorial"                       #name属性，用来区分爬虫，在一个项目中，你不能用同样的名称来命名不同的爬虫。
    num = 0
    allowd_domains=['hdzuoye.com']
    start_urls = []
    for i in range(178900,180000):
        bookid = str(i)
        dict = ['n', 'm', 'p', 'o', 'j', 'i', 'l', 'k', 'f', 'e']
        f = ''.join(random.sample(string.ascii_letters + string.digits, 30))
        f = f.lower()
        f = 'm' + f
        len2 = len(f)
        newstr = {}
        for i in range(0, len2):
            newstr[i] = f[i]
            if i is 1:
                newstr[i] = str(0)
            if i is 2:
                newstr[i] = str(5)
            if i == 4:
                newstr[i] = dict[int(bookid[0])]
            if i == 6:
                newstr[i] = dict[int(bookid[1])]
            if i == 9:
                newstr[i] = dict[int(bookid[2])]
            if i == 17:
                newstr[i] = dict[int(bookid[3])]
            if i == 25:
                newstr[i] = dict[int(bookid[4])]
            if i == 29:
                newstr[i] = dict[int(bookid[5])]

            str1 = ''
            for i in range(0, len(newstr)):
                str1 += newstr[i]
            str1 = 'http://www.hdzuoye.com/detail/' + str1
            start_urls.append(str1)

    link_extractor=LinkExtractor(allow=(r'www.hdzuoye.com\/detail\/([a-z0-9]+)',),)
    rules = [
        Rule(link_extractor=link_extractor,callback='parse',follow=True),
    ]

    def parse(self, response):           #parse方法用来处理request返回的结果。关于这一部分的一些内容，我在后面详细介绍。
        title = response.selector.xpath(".//*[@id='content_bg']/div[2]/div[1]/div[1]/div[2]/p/text()").extract()
        version = response.selector.xpath(".//*[@id='content_bg']/div[2]/div[1]/div[1]/div[2]/ul[1]/li[1]/a/text()").extract()
        grade = response.selector.xpath(".//*[@id='content_bg']/div[2]/div[1]/div[1]/div[2]/ul[1]/li[2]/a/text()").extract()
        subject = response.selector.xpath(".//*[@id='content_bg']/div[2]/div[1]/div[1]/div[2]/ul[1]/li[3]/a/text()").extract()
        publishing = response.selector.xpath(".//*[@id='content_bg']/div[2]/div[1]/div[1]/div[2]/ul[1]/li[4]/text()").extract()

        Tutorial = TutorialItem()
        # 存入items
        Tutorial["title"] = title
        Tutorial["version"] = version
        Tutorial["grade"] = grade
        Tutorial["subject"] = subject
        Tutorial["publishing"] = publishing
        yield Tutorial