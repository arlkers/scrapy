# -*- coding: utf-8 -*-
import scrapy

from tutorial.items import TutorialItem


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['www.27270.com']
    start_urls = ['http://www.27270.com/ent/meinvtupian/','http://www.27270.com/ent/lianglimeimo/','http://www.27270.com/ent/rentiyishu/']

    def parse(self, response):
        item = TutorialItem()
        for sel in response.css('a[class*=MMPic]'):
            title1=sel.xpath("@title").extract()[0]
            item['link'] = sel.xpath("@href").extract()[0]
            item['title'] = title1
            item['pic']=sel.xpath("i/img/@src").extract()[0] or sel.xpath("img/@src").extract()[0]
            yield item

    def parse_pos(self, response):
        result=response.xpath('//a[@class="MMPic"]')
        print(len(result))
        for sel in result:
            # print(sel.extract())
            item = TutorialItem()
            title1=sel.xpath("@title").extract()[0]
            # print(type(title1))
            item['title'] = title1
            item['link'] = sel.xpath("@href").extract()[0]
            # print(sel.xpath('@src'))
            item['pic']=(sel.xpath('i/img/@src').extract() or sel.xpath('img/@src').extract())[0]
            yield item
        #url跟进开始
        return
        #获取下一页的url信息
        url = response.xpath("//a[contains(text(),'下一页')]/@href").extract()
        if url :
            #将信息组合成下一页的url
            page = 'http://www.27270.com/' + url[0]
            #返回url
            yield scrapy.Request(page, callback=self.parse)
        #url跟进结束
