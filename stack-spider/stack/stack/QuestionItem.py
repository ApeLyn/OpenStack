# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class QuestionItem(Item):
    source = Field()
    title = Field()
    url = Field()
    desc = Field()
    votes = Field()
    tag = Field()
    start_time = Field()
    update_time = Field()
    user_id = Field()

