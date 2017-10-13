# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class UserItem(Item):
    url = Field()
    source = Field()
    name = Field()
    answer_num = Field()
    tags = Field()
    votes = Field()
    ranking = Field()
