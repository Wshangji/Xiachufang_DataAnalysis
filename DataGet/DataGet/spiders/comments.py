import scrapy
from scrapy import Selector
import csv


class CommentsSpider(scrapy.Spider):
    name = 'comments'
    allowed_domains = ['www.xiachufang.com']


    def start_requests(self):
        # 读取csv文件
        csvfile = open("food.csv", "r", encoding='utf-8')
        reader = csv.reader(csvfile)
        for item in reader:
            # 忽略第一行
            if reader.line_num == 1:
                continue
            yield scrapy.Request(
                url=item[0],
                callback=self.parse_all,
                errback=self.error_parse,
            )


    def parse_all(self, response):
        if response.status == 200:
            # 执行js脚本,将下拉条拉到最下面
            self.browser.execute_script(
                'window.scrollTo(0,document.body.scrollHeight)'
            )
            # 获取菜品名字
            title = response.xpath('//h1/a/span/text()').get()
            # print(title)
            # 爬取评论
            commentss = response.xpath('//p[@class="desc"]/text()')
            print(commentss)


    def error_parse(self, faiture):
        request = faiture.request