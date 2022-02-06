import scrapy
from scrapy import Selector


class CategorySpider(scrapy.Spider):
    name = 'category'
    allowed_domains = ['www.xiachufang.com']
    start_urls = ['http://www.xiachufang.com/category/']

    def parse(self, response):
        categorys = response.xpath("//div[@class='cates-list-all clearfix hidden']").getall()
        for category in categorys:
            sel_category = Selector(text=category)
            # 一级菜单分类
            # category_father = sel_category.xpath("//h4/text()").extract_first().strip()

            # 二级菜单分类
            items = sel_category.xpath("//ul/li/a").getall()
            for item in items:
                sel = Selector(text=item)
                url = sel.xpath("//@href").get()
                name = sel.xpath("//text()").get()
                next_url = response.urljoin(url)
                print(name + "\n" + next_url + "\n")