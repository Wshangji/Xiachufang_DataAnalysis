import scrapy
from scrapy import Selector
from DataGet.items import FoodItem
import csv


class FooditeamsSpider(scrapy.Spider):
    name = 'fooditeams'
    allowed_domains = ['www.xiachufang.com']
    base_url = "https://www.xiachufang.com"

    def start_requests(self):
        # 读取csv文件
        csvfile = open("category.csv", "r", encoding='utf-8')
        reader = csv.reader(csvfile)
        for item in reader:
            # 忽略第一行
            if reader.line_num == 1:
                continue
            # print(item[2])
            yield scrapy.Request(
                url=item[2],
                callback=self.parse_all,
                errback=self.error_parse,
            )

    def parse_all(self, response):
        if response.status == 200:
            recipes = response.xpath("//div[@class='normal-recipe-list']/ul/li").extract()
            nextPage = response.xpath("//div[@class='pager']/a[@class='next']/@href").extract_first()
            # print(recipes)
            if nextPage:
                print(nextPage)
                yield scrapy.Request(
                    url = self.base_url + nextPage,
                    callback = self.parse_all,
                    errback = self.error_parse,
                )
            for recipe in recipes:
                sel = Selector(text=recipe)
                food_item = FoodItem()
                name = sel.xpath("//p[@class='name']/a/text()").extract_first().strip()
                food_item['name'] = name
                url = sel.xpath("//a[1]/@href").extract_first()
                food_item['url'] = "https://www.xiachufang.com" + url
                food_item['score'] = sel.xpath("//p[@class='stats']/span/text()").extract_first().strip()
                yield food_item

    def error_parse(self, faiture):
        request = faiture.request