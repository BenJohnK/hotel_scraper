# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelScraperItem(scrapy.Item):
    # define the fields for your item here like:
    hotel_name = scrapy.Field()
    check_in_date = scrapy.Field()
    check_out_date = scrapy.Field()
    price = scrapy.Field()
    extra_charges = scrapy.Field()
    address = scrapy.Field()
    price_div_content = scrapy.Field()
    hotel_url = scrapy.Field()
    input_hotel_name = scrapy.Field()
    input_check_in_date = scrapy.Field()
    input_check_out_date = scrapy.Field()

