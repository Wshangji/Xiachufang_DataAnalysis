import scrapy
from scrapy import Selector
from DataGet.items import Food
import csv


class FoodSpider(scrapy.Spider):
    name = 'food'
    allowed_domains = ['www.xiachufang.com']
    # start_urls = ['https://www.xiachufang.com/recipe/103920397/']

    def start_requests(self):
        # 读取csv文件
        csvfile = open("D:\PROJECT\Xiachufang_DataAnalysis\DataGet/fooditeams.csv", "r", encoding='utf-8')
        reader = csv.reader(csvfile)
        for item in reader:
            # 忽略第一行
            if reader.line_num == 1:
                continue
            yield scrapy.Request(
                url=item[2],
                callback=self.parse_all,
                errback=self.error_parse,
            )


    def parse_all(self, response):
        materials_list = []
        contents_list = []
        if response.status == 200:
            # 获取菜品名
            title = response.xpath('//h1/text()').get().strip()     #strip去掉两头的换行符
            # 获取用料表
            materials = response.xpath('//table//tr')
            for item in materials:
                materials_used = item.xpath('./td[1]/a/text()').get()
                if materials_used == None:
                    materials_used = item.xpath('./td[1]/text()').get().strip()
                count = item.xpath('./td[2]/text()')
                if not count:
                    count = "适量"
                else:
                    count = count.get().strip()
                materials_list.append(materials_used+":"+count)
                # print("用料：",materials_used)
                # print("用量：",count)
            # 采集制作步骤
            contents = response.xpath('//li[@class="container"]/p/text()')
            for item in contents:
                contents_list.append(item.get())
                # print(item.get())
            comment_url = response.url + "dishes/"
            # print(materials_list)
            # print(contents_list)
            # print(comment_url)
            food = Food()
            food['title'] = title
            food['materials_list'] = materials_list
            food['contents_list'] = contents_list
            food['comment_url'] = comment_url
            yield food


    def error_parse(self, faiture):
        request = faiture.request