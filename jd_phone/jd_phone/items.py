# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdPhoneItem(scrapy.Item):
    # define the fields for your item here like:
    # title = scrapy.Field()  # 标题
    brand = scrapy.Field()  # 品牌
    product_name = scrapy.Field()  # 产品名称
    # info = scrapy.Field()  # 详细信息
    Net_model = scrapy.Field()  # 入网型号
    url = scrapy.Field()  # 商品链接
    year = scrapy.Field()  # 上市年份
    month = scrapy.Field()  # 上市月份
    # product_m_price = scrapy.Field()  # 最高价格
    product_price = scrapy.Field()  # 当前价格
    product_o_price = scrapy.Field()  # 指导价格
    total_comment_num = scrapy.Field()  # 总评论数
    good_comment_num = scrapy.Field()  # 好评数
    good_percent_com = scrapy.Field()  # 好评率
    bad_comment_num = scrapy.Field()  # 差评数
    bad_percent_com = scrapy.Field()  # 差评率
