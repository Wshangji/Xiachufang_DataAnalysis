# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 代理ip信息
class ProxyItem(scrapy.Item):
    proxy = scrapy.Field()
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


# 菜品简介
class FoodItem(scrapy.Item):
    # 菜品名称
    name = scrapy.Field()
    # url地址
    url = scrapy.Field()
    # 网站评分
    score = scrapy.Field()
    pass


# 菜品详细信息
class Food(scrapy.Item):
    # 菜品名称
    title = scrapy.Field()
    # 用料列表
    materials_list = scrapy.Field()
    # 步骤列表
    contents_list = scrapy.Field()
    # 评论地址
    comment_url = scrapy.Field()
    pass

# 评论数据
class Comment(scrapy.Item):
    # 菜单名称
    title = scrapy.Field()
    # 评论内容
    comment = scrapy.Field()