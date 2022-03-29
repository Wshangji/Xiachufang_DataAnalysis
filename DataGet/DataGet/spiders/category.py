import scrapy
from scrapy import Selector
from DataGet.items import CategoryItem


# @author Nanf_bunan
# 分类页爬虫，用于爬取一二级菜单分类
class CategorySpider(scrapy.Spider):
    name = 'category'
    allowed_domains = ['www.xiachufang.com']
    start_url = 'https://www.xiachufang.com/category/'

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse_all)

    def parse_all(self, response):
        categorys = response.xpath("//div[@class='cates-list-all clearfix hidden']").getall()
        for category in categorys:
            sel_category = Selector(text=category)
            # 一级菜单分类
            category_father = sel_category.xpath("//h4/text()").extract_first().strip()

            # 二级菜单分类
            items = sel_category.xpath("//ul/li/a").getall()
            for item in items:
                category_item = CategoryItem()
                category_item['category_father'] = category_father
                sel = Selector(text=item)
                url = sel.xpath("//@href").get()
                category_item['item_name'] = sel.xpath("//text()").get()
                category_item['item_url'] = response.urljoin(url)
                yield category_item
                # print("fewrgwe")
    def error_parse(self, faiture):
        request = faiture.request
