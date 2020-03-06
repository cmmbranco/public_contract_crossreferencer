# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VerificadorBaseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    contract_url = scrapy.Field()
    poster_nif = scrapy.Field()
    winner_nif = scrapy.Field()
    contract_value = scrapy.Field()
    procedimento = scrapy.Field()



class RaciusItem(scrapy.Item):

    nif = scrapy.Field()
    creation_date = scrapy.Field()
