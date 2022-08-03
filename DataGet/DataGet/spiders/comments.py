import scrapy
from scrapy import Selector
from DataGet.items import Comment
import csv


class CommentsSpider(scrapy.Spider):
    name = 'comments'
    allowed_domains = ['www.xiachufang.com']
    base_url = "https://www.xiachufang.com"

    def start_requests(self):
        # 读取csv文件
        csvfile = open("D:\PROJECT\Xiachufang_DataAnalysis\DataGet/food.csv", "r", encoding='utf-8')
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
            nextPage = response.xpath("//a[@class='next']/@href").get()
            if nextPage:
                print(nextPage)
                yield scrapy.Request(
                    url = self.base_url + nextPage,
                    callback = self.parse_all,
                    errback = self.error_parse,
                )
            # 获取菜品名字
            title = response.xpath('//h1/a/span/text()').get()
            print(title)
            # 爬取评论
            comments = response.xpath('//p[@class="desc"]/text()')
            for item in comments:
                comments_item = item.get().strip()
                if comments_item == "分享图片":
                    pass
                comment = Comment()
                comment['title'] = title
                comment['comment'] = comments_item
                yield comment
                # print("————评论————：",comments_item)


    def error_parse(self, faiture):
        request = faiture.request