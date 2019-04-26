# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Meishi2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # links = scrapy.Field()
    Food = scrapy.Field()
    Title = scrapy.Field()
    Src = scrapy.Field()
    Main_ing = scrapy.Field()
    Acces = scrapy.Field()
    Mix_ing = scrapy.Field()
    Cooks = scrapy.Field()
    Steps = scrapy.Field()
    Types = scrapy.Field()
    Tips = scrapy.Field()
    pass
