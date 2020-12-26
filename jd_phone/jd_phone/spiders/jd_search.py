from ..items import JdPhoneItem
import scrapy
import requests
import json


class JdSearchSpider(scrapy.Spider):
    name = 'jd_search'
    allowed_domains = ['jd.com']  # 有的时候写个www.jd.com会导致search.jd.com无法爬取
    keyword = ['华为手机', '苹果手机', 'oppo手机']
    page = 1
    url = 'https://search.jd.com/Search?keyword=%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%s&cid2=653&cid3=655&page=%d&click=0'
    next_url = 'https://search.jd.com/s_new.php?keyword=%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%s&cid2=653&cid3=655&page=%d&scrolling=y&show_items=%s'

    def start_requests(self):
        for word in self.keyword:
            yield scrapy.Request(self.url % (word, word, self.page), callback=self.parse)

    def parse(self, response):
        """
        爬取每页的前三十个商品，数据直接展示在原网页中
        :param response:
        :return:
        """
        headers = {'referer': response.url}
        ids = []
        for li in response.xpath('//*[@id="J_goodsList"]/ul/li'):
            item = JdPhoneItem()
            # title = li.xpath('div/div/a/em/text()').extract()  # 标题
            id = li.xpath('@data-sku').extract()  # id
            p = requests.get(
                'https:' + '//p.3.cn/prices/mgets?skuIds=J_' + id[0], headers=headers)  # 请求商品价格json
            [product_dict] = json.loads(p.text)  # 获取商品价格
            # product_m_price = product_dict['m']
            product_price = product_dict['p']
            product_o_price = product_dict['op']
            c = requests.get('https://club.jd.com/comment/productCommentSummaries.action?referenceIds=' + id[0],
                            headers=headers)  # 请求评论json
            comment_dict = json.loads(c.text.split(
                '[')[-1].split(']')[0])  # json内容截取
            total_comment_num = comment_dict['CommentCount']
            good_comment_num = comment_dict['ShowCount']
            good_percent_com = comment_dict['GoodRate']
            bad_comment_num = comment_dict['PoorCount']
            bad_percent_com = comment_dict['PoorRate']
            url = li.xpath(
                'div/div[@class="p-name p-name-type-2"]/a/@href').extract()  # 需要跟进的链接
            # item['title'] = ''.join(title)
            # item['product_m_price'] = ''.join(product_m_price)
            item['product_price'] = ''.join(product_price)
            item['product_o_price'] = ''.join(product_o_price)
            item['total_comment_num'] = total_comment_num
            item['good_comment_num'] = good_comment_num
            item['good_percent_com'] = good_percent_com
            item['bad_comment_num'] = bad_comment_num
            item['bad_percent_com'] = bad_percent_com
            item['url'] = ''.join(url)
            if item['url'].startswith('//'):
                item['url'] = 'https:' + item['url']
            elif not item['url'].startswith('https:'):
                item['info'] = None
                yield item
                continue
            yield scrapy.Request(item['url'], callback=self.info_parse, meta={"item": item})
        # 后三十页的链接访问会检查referer，referer是就是本页的实际链接
        # referer错误会跳转到：https://www.jd.com/?se=deny
        self.page += 1
        yield scrapy.Request(self.next_url % (self.keyword, self.keyword, self.page, ','.join(ids)),
                            callback=self.next_parse, headers=headers)

    def next_parse(self, response):
        """
        爬取每页的后三十个商品，数据展示在一个特殊链接中：url+id(这个id是前三十个商品的id)
        :param response:
        :return:
        """
        headers = {'referer': response.url}
        for li in response.xpath('//*[@id="J_goodsList"]/ul/li'):
            item = JdPhoneItem()
            # title = li.xpath('div/div/a/em/text()').extract()  # 标题
            id = li.xpath('@data-sku').extract()  # id
            p = requests.get(
                'https:' + '//p.3.cn/prices/mgets?skuIds=J_' + id[0], headers=headers)  # 请求商品价格json
            [product_dict] = json.loads(p.text)  # 获取商品价格
            # product_m_price = product_dict['m']
            product_price = product_dict['p']
            product_o_price = product_dict['op']
            c = requests.get('https://club.jd.com/comment/productCommentSummaries.action?referenceIds=' + id[0],
                            headers=headers)  # 请求评论json
            comment_dict = json.loads(c.text.split(
                '[')[-1].split(']')[0])  # json内容截取
            total_comment_num = comment_dict['CommentCount']
            good_comment_num = comment_dict['ShowCount']
            good_percent_com = comment_dict['GoodRate']
            bad_comment_num = comment_dict['PoorCount']
            bad_percent_com = comment_dict['PoorRate']
            url = li.xpath(
                'div/div[@class="p-name p-name-type-2"]/a/@href').extract()  # 需要跟进的链接
            # item['title'] = ''.join(title)
            # item['product_m_price'] = ''.join(product_m_price)
            item['product_price'] = ''.join(product_price)
            item['product_o_price'] = ''.join(product_o_price)
            item['total_comment_num'] = total_comment_num
            item['good_comment_num'] = good_comment_num
            item['good_percent_com'] = good_percent_com
            item['bad_comment_num'] = bad_comment_num
            item['bad_percent_com'] = bad_percent_com
            item['url'] = ''.join(url)
            if item['url'].startswith('//'):
                item['url'] = 'https:' + item['url']
            elif not item['url'].startswith('https:'):
                item['info'] = None
                yield item
                continue

            yield scrapy.Request(item['url'], callback=self.info_parse, meta={"item": item})

        if self.page < 2:
            self.page += 1
            yield scrapy.Request(self.url % (self.keyword, self.keyword, self.page), callback=self.parse)

    def info_parse(self, response):

        item = response.meta['item']
        # item['info'] = {}
        brand = response.xpath(
            '//div[@class="inner border"]/div[@class="head"]/a/text()').extract()
        product_name = response.xpath(
            '//div[@class="item ellipsis"]/text()').extract()
        item['brand'] = ''.join(brand)
        item['product_name'] = ''.join(product_name)

        for div in response.xpath('//div[@class="Ptable"]/div[@class="Ptable-item"]'):
            h3 = ''.join(div.xpath('h3/text()').extract())
            if h3 == '主体':
                # h3 = "未知"
                dt = div.xpath('dl/dl/dt/text()').extract()
                dd = div.xpath('dl/dl/dd[not(@class)]/text()').extract()
                # item['info'][h3] = {}
                info_key = {
                    '品牌': 'brand',
                    '产品名称': 'product_name',
                    '入网型号': 'Net_model',
                    '上市年份': 'year',
                    '上市月份': 'month',
                }
                for t, d in zip(dt, dd):
                    if t in info_key.keys():
                        item[info_key[t]] = d
                break
        yield item
