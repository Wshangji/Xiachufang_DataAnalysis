import scrapy
from scrapy import Selector
import csv

class FooditemSpider(scrapy.Spider):
    name = 'fooditem'
    allowed_domains = ['www.xiachufang.com']
    base_url = "https://www.xiachufang.com"

    def start_requests(self):
        # 读取csv至字典
        csvFile = open("category.csv", "r")
        reader = csv.reader(csvFile)
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
        if response.status == 200:
            recipes = response.xpath("//div[@class='normal-recipe-list']/ul/li").extract()
            self.parse_recipes(recipes)
            nextPage = response.xpath("//div[@class='pager']/a[@class='next']/@href").extract_first()
            # print(recipes)

            if nextPage:
                yield scrapy.Request(
                    url = self.base_url + nextPage,
                    callback = self.parse_all,
                    errback = self.error_parse,
                )

    def parse_recipes(self, recipes):
        for recipe in recipes:
            sel = Selector(text=recipe)
            food_item = FoodItem()
            food_item['name'] = sel.xpath("//p[@class='name']/a/text()").extract_first().strip()
            food_item['url'] = sel.xpath("//a[1]/@href").extract_first()
            # item_id = recipe.compile("/recipe/(.*?)/").findall(url)[0]
            food_item['score'] = sel.xpath("//p[@class='stats']/span/text()").extract_first().strip()
            yield food_item

    def error_parse(self, faiture):
        request = faiture.request
        # utils.log('error_parse url:%s meta:%s' % (request.url, request.meta))
