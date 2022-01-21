import scrapy
from scrapy import Selector


class CategorySpider(scrapy.Spider):
    name = 'category'
    allowed_domains = ['www.xiachufang.com/category']
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    }
    start_urls = ['http://www.xiachufang.com/category/']

    def parse(self, response):
        categorys = response.xpath("//div[@class='cates-list-all clearfix hidden']").extract()
        for category in categorys:
            sel_category = Selector(text=category)
            # 一级菜单分类
            # category_father = sel_category.xpath("//h4/text()").extract_first().strip()

            # 二级菜单分类
            items = sel_category.xpath("//ul/li/a").extract()
            for item in items:
                sel = Selector(text=item)
                url = sel.xpath("//@href").extract_first()
                name = sel.xpath("//text()").extract_first()
                print(name+"\n"+url+"\n")