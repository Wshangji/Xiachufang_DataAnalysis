# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# 下厨房菜单分类的爬虫
# 根据分类菜单爬取全部食谱

import scrapy


class FoodItem(scrapy.Item):
    # 菜品名称
    name = scrapy.Field()
    # url地址
    url = scrapy.Field()
    # 网站评分
    score = scrapy.Field()
    pass


# 菜单数据
class CategoryItem(scrapy.Item):
    # 一级菜单分类
    category_father = scrapy.Field()
    # 二级菜单分类
    item_name = scrapy.Field()
    # url地址
    item_url = scrapy.Field()
    pass