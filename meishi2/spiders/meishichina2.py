# -*- coding: utf-8 -*-
import scrapy
from meishi2.items import Meishi2Item
from bs4 import BeautifulSoup

class MeishichinaSpider(scrapy.Spider):
    name = 'meishichina2'
    allowed_domains = ['meishichina2.py']

    start_urls = ['https://www.meishichina.com/YuanLiao/zheergen/']

    base_url = 'https://www.meishichina.com/YuanLiao/zheergen/%d/'
    pagenum = 0


    def parse(self, response):
        while self.pagenum < 50:  # 页数限制
            self.pagenum += 1
            new_url = self.base_url % self.pagenum
            if new_url:
                yield response.follow(new_url, callback=self.recipe_url, dont_filter=True)
            else:
                continue


    # 爬取每一页的食谱url(二级页面)
    def recipe_url(self, response):
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        urllist = soup.find('div', class_='left3_list clear mt20')
        if urllist:
            li_list = urllist.find('ul')
            hrefs = []
            for li_item in li_list.find_all('li'):
                href = li_item.find_all('a')[0].get('href')
                if href not in hrefs:
                    hrefs.append(href)
                    yield scrapy.Request(href, callback=self.recipe_Info, dont_filter=True)

    # 爬取食谱具体信息(三级页面)
    def recipe_Info(self, response):
        selector = scrapy.Selector(response)
        item = Meishi2Item()
        item['Title'] = selector.xpath('//*[@id="recipe_title"]/text()').extract()[0]
        item['Src'] = selector.xpath('//*[@id="recipe_De_imgBox"]/a/img/@src').extract()[0]
        item['Main_ing'] = selector.xpath('/html/body/div[5]/div/div[1]/div[2]/div/fieldset[1]/div').xpath('string(.)').extract()[0].strip().replace('\n', ' ')
        item['Acces'] = selector.xpath('/html/body/div[5]/div/div[1]/div[2]/div/fieldset[2]/div').xpath('string(.)').extract()[0].strip().replace('\n', ' ')
        try:
            item['Mix_ing'] = selector.xpath('/html/body/div[5]/div/div[1]/div[2]/div/fieldset[3]').xpath('string(.)').extract()[0].strip().replace('\n', ' ')
        except:
            item['Mix_ing'] = ''
        item['Cooks'] = selector.xpath('/html/body/div[5]/div/div[1]/div[2]/div/div[3]').xpath('string(.)').extract()[0].strip().replace('\n', ' ')
        item['Steps'] = selector.xpath('/html/body/div[5]/div/div[1]/div[2]/div/div[5]').xpath('string(.)').extract()[0].strip().replace('\n', ' ')
        tip = selector.xpath('/html/body/div[5]/div/div[1]/div[2]/div/div[6]').xpath('string(.)').extract()[0]
        if '小窍门' in tip:
            item['Tips'] = selector.xpath('/html/body/div[5]/div/div[1]/div[2]/div/div[7]').xpath('string(.)').extract()[0].strip().replace('\n', ' ')
            item['Types'] = selector.xpath('/html/body/div[5]/div/div[1]/div[2]/div/div[10]').xpath('string(.)').extract()[0].strip(). \
                            replace('\xa0\xa0', '').replace('\n', ' ')
            if '所属分类：' not in item['Types']:
                item['Types'] = selector.xpath('/html/body/div[5]/div/div[1]/div[2]/div/div[9]').xpath('string(.)').extract()[0].strip(). \
                    replace('所属分类：', '').replace('\xa0\xa0', '').replace('\n', ' ')
            else:
                item['Types'] = item['Types'].replace('所属分类：', '')
        else:
            item['Tips'] = ''
            item['Types'] = selector.xpath('/html/body/div[5]/div/div[1]/div[2]/div/div[8]').xpath('string(.)').extract()[0].strip(). \
                            replace('\xa0\xa0', '').replace('\n', ' ')
            if '所属分类：' not in item['Types']:
                item['Types'] = selector.xpath('/html/body/div[5]/div/div[1]/div[2]/div/div[7]').xpath('string(.)').extract()[0].strip(). \
                    replace('所属分类：', '').replace('\xa0\xa0', '').replace('\n', ' ')
            else:
                item['Types'] = item['Types'].replace('所属分类：', '')

        yield item
