import scrapy
from urllib.parse import urlencode
from lxml.html import fromstring
from hotel_scraper.helpers.headers import headers
from html import unescape
from hotel_scraper.items import HotelScraperItem
import csv
import os

class MainSpider(scrapy.Spider):
    name = "main"
    allowed_domains = ["www.booking.com", "www.example.com"]
    start_urls = ["https://www.example.com"]
    custom_settings = {
		'FEEDS': { 'output.csv': { 'format': 'csv', 'overwrite': True}},
        'FEED_EXPORT_FIELDS': [
            'hotel_name',
            'check_in_date',
            'check_out_date',
            'price',
            'extra_charges',
            'address',
            'price_div_content',
            'hotel_url',
            'input_hotel_name',
            'input_check_in_date',
            'input_check_out_date'
        ]
	}

    def parse(self, response):
        url_reader = list(csv.DictReader(open(os.path.join(os.path.dirname('__file__'), 'input_hotel_names.csv'))))
        for item in url_reader:
            input_hotel_name = item.get("input_hotel_name")
            input_check_in_date = item.get("check_in_date")
            input_check_out_date = item.get("check_out_date")
            meta = {
                "input_hotel_name": input_hotel_name,
                "input_check_in_date": input_check_in_date,
                "input_check_out_date": input_check_out_date
            }
            params = {
                'ss': input_hotel_name,
                'label': 'gen173nr-1FCAEoggI46AdIM1gEaGyIAQGYAQm4ARnIAQzYAQHoAQH4AQuIAgGoAgO4ArvwmK4GwAIB0gIkY2ZlMDE5NTctNDc1OS00M2EyLWJkNTItZTE2Y2JkN2FkYTg42AIG4AIB',
                'sid': '35e3b28fbfa5ab6420356fcf7ab00646',
                'aid': '304142',
                'lang': 'en-gb',
                'sb': '1',
                'src_elem': 'sb',
                'src': 'searchresults',
                'dest_type': 'hotel',
                'ac_position': '0',
                'ac_click_type': 'b',
                'ac_langcode': 'en',
                'ac_suggestion_list_length': '1',
                'search_selected': 'true',
                'search_pageview_id': '9c5c6a16f6d60385',
                'ac_meta': 'GhA5YzVjNmExNmY2ZDYwMzg1IAAoATICZW46DXRhaiBrdW1hcmFrb21AAEoAUAA=',
                'checkin': input_check_in_date,
                'checkout': input_check_out_date,
                'group_adults': '2',
                'no_rooms': '1',
                'group_children': '0',
            }
            url = f"https://www.booking.com/searchresults.en-gb.html?{urlencode(params)}"
            yield scrapy.Request(url, headers=headers, meta=meta, callback=self.parse_hotels_listing_page)

    def parse_hotels_listing_page(self, response):
        response_text = fromstring(response.text)
        hotel_urls = response_text.xpath("//div[@data-testid='property-card']//a/@href")
        most_matched_hotel_url = hotel_urls[0] if hotel_urls else None
        response.meta['hotel_url'] = most_matched_hotel_url
        if most_matched_hotel_url:
            yield scrapy.Request(url=most_matched_hotel_url, headers=headers, meta=response.meta, callback=self.parse_hotel_page)

    def parse_hotel_page(self, response):
        meta = response.meta
        response_text = fromstring(response.text)
        hotel_name = response_text.xpath("//h2[contains(@class, 'pp-header__title')]/text()")
        check_in_date = response_text.xpath("//button[@data-testid='date-display-field-start']/span/text()")
        check_out_date = response_text.xpath("//button[@data-testid='date-display-field-end']/span/text()")
        price_list = response_text.xpath("//div[@class='hprt-table-column']//tbody/tr")
        main_price = price_list[0].xpath("./@data-hotel-rounded-price") if price_list else None
        main_price = main_price[0] if main_price else None
        extra_charges = price_list[0].xpath(".//div[contains(@class, 'prd-taxes-and-fees-under-price')]/text()") if price_list else None
        extra_charges = self.clean_text(extra_charges[0]) if extra_charges else None
        address = response_text.xpath("//p[contains(@class, 'address')]//span[contains(@class, 'hp_address_subtitle')]/text()")
        address = self.clean_text(address[0]) if address else None
        price_content = price_list[0].xpath(".//td//text()") if price_list else []
        price_content_extracted = list(map(lambda x: self.clean_text(x), price_content))
        price_content_extracted = list(filter(None, price_content_extracted))
        price_content_extracted = " ".join(price_content_extracted)
        price_content_extracted = price_content_extracted if price_content_extracted else None
        data = {
            "hotel_name": hotel_name[0] if hotel_name else None,
            "check_in_date": check_in_date[-1] if check_in_date else None,
            "check_out_date": check_out_date[-1] if check_out_date else None,
            "price": main_price,
            "extra_charges": extra_charges,
            "address": address,
            "price_div_content": price_content_extracted,
            "hotel_url": meta["hotel_url"],
            "input_hotel_name": meta["input_hotel_name"],
            "input_check_in_date": meta["input_check_in_date"],
            "input_check_out_date": meta["input_check_out_date"]
        }
        yield HotelScraperItem(**data)

    def clean_text(self, text):
        if not text or not str(text).strip():
            return
        return ' '.join(unescape(text).split()).strip()