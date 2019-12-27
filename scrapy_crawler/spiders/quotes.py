# -*- coding: utf-8 -*-
import scrapy

from scrapy.http import Request
from ..items import ScrapyCrawlerItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    login_url = ['ucon.umax.co.jp']
    start_urls = ['https://ucon.umax.co.jp/carbasic/']
  
    def parse(self, response):
      
        return scrapy.FormRequest.from_response(
            response,
            formdata={'USERID': 'A33230', 'UPASSWORD': '2416515'},
            callback=self.after_login,
            dont_click=True
           )
    def after_login(self, response):
        return Request(url="https://ucon.umax.co.jp/carbasic/", callback=self.parse_truck)
 
    def parse_truck(self, response):
      
        for sel in response.css(".search_list .list_image"):
            # １ページ目だけ取得
            detail_truck_page = sel.css("a::attr(href)").extract_first()
            if detail_truck_page:
                url = response.urljoin(detail_truck_page)
                yield scrapy.Request(url, callback=self.parse_detail_truck)

        #pagination link      
        next_page = ""
        for page_navi in response.css(".pagenation li"):
            if page_navi.css("::attr(class)").extract_first() == "next":
                next_page = page_navi.css("a::attr(href)").get()
        #next_page = response.css(".pagenation li[class='next'] a::attr('href')").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_truck, errback=self.process_exception)
                
    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.
 
        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        if isinstance(exception,TimeoutError):
            return request

            
    def parse_detail_truck(self, response):
         article = ScrapyCrawlerItem()
         
         car_accessories=[]
         car_maker =""
         car_category =""
         car_distance=""
         price = str(response.css("#detail_total tr:nth-child(1) td span::text").extract_first())
         title = "-" if len(response.css('#h1_title h1::text').extract_first()) == 0 else (response.css('#h1_title h1::text').extract_first()).split()
         
         for accessories in response.css(".table_accessory tr td"):
             if not accessories.css('::attr(class)').extract_first():
                car_accessories.append(accessories.css("td::text").extract_first())

         
         if len(title) == 5:
             car_maker = title[0]
             car_category = title[2]
             run_distance = title[4]
         elif len(title) == 4:
             car_maker = title[0]
             car_category = title[1]
             run_distance = title[3]
         elif len(title) == 3:
             car_maker = "-"
             car_category = title[0]
             run_distance = "-"
         else:
             car_maker = "-"
             car_category = "-"
             run_distance = "-"
             
         article['title'] = response.css('#h1_title h1::text').extract_first().strip()   
         article['car_maker'] = car_maker.strip() 
         article['car_category'] = car_category.strip()
         article['run_distance'] = run_distance.strip()
         article['car_option'] = "-"  if len(car_accessories) ==0 else ("|".join(car_accessories)).strip() 
         article['url'] =(response.url).strip()
         article['price'] =  polish(price+ (" ".join(response.css("#detail_total tr:nth-child(1) td::text").extract())))
         article['control_number'] = response.css("#detail_date table:nth-child(1) tr:nth-child(1) td::text").extract_first().strip()
         article['price_iclude_tax'] = response.css("#detail_date table:nth-child(2) tr:nth-child(2) td:nth-child(1)::text").extract_first().strip()
         article['inventory'] = polish(" ".join(response.css("#detail_date table:nth-child(3) tr:nth-child(1) td::text").extract()))
         article['type'] = response.css("#detail_spec  tr:nth-child(1) td:nth-child(2)::text").extract_first().strip()
         article['chassis_no'] = response.css("#detail_spec  tr:nth-child(2) td:nth-child(2)::text").extract_first().strip()
         article['max_load_capacity'] = response.css("#detail_spec  tr:nth-child(3) td:nth-child(2)::text").extract_first().strip()
         article['no_of_door'] = response.css("#detail_spec  tr:nth-child(4) td:nth-child(2)::text").extract_first().strip()
         article['tire_shape'] = response.css("#detail_spec  tr:nth-child(5) td:nth-child(2)::text").extract_first().strip()
         article['clutch_pedal'] = response.css("#detail_spec  tr:nth-child(6) td:nth-child(2)::text").extract_first().strip()
         article['color'] = response.css("#detail_spec  tr:nth-child(7) td:nth-child(2)::text").extract_first().strip()
         article['external_height'] = response.css("#detail_spec  tr:nth-child(8) td:nth-child(2)::text").extract_first().strip()
         article['external_width'] = response.css("#detail_spec  tr:nth-child(9) td:nth-child(2)::text").extract_first().strip()
         article['external_high'] = response.css("#detail_spec  tr:nth-child(10) td:nth-child(2)::text").extract_first().strip()
         article['body_size_height'] = response.css("#detail_spec  tr:nth-child(11) td:nth-child(2)::text").extract_first().strip()
         article['body_size_width'] = response.css("#detail_spec  tr:nth-child(12) td:nth-child(2)::text").extract_first().strip()
         article['body_size_high'] = response.css("#detail_spec  tr:nth-child(13) td:nth-child(2)::text").extract_first().strip()
         article['notes'] =  response.css("#detail_spec  tr:nth-child(14) td:nth-child(2)::text").extract_first().strip()
         article['notices'] =  response.css("#detail_spec  tr:nth-child(15) td:nth-child(2)::text").extract_first().strip()
         article['common_name'] = response.css("#detail_spec  tr:nth-child(1) td:nth-child(4)::text").extract_first().strip()
         article['first_year_registration'] = polish(response.css("#detail_spec  tr:nth-child(2) td:nth-child(4)::text").extract_first())
         article['capacity'] = response.css("#detail_spec  tr:nth-child(3) td:nth-child(4)::text").extract_first().strip()
         article['roof_shape'] = response.css("#detail_spec  tr:nth-child(4) td:nth-child(4)::text").extract_first().strip()
         article['drive_system'] = response.css("#detail_spec  tr:nth-child(5) td:nth-child(4)::text").extract_first().strip()
         article['mission'] = response.css("#detail_spec  tr:nth-child(6) td:nth-child(4)::text").extract_first().strip()
         article['engine_model'] = response.css("#detail_spec  tr:nth-child(7) td:nth-child(4)::text").extract_first().strip()
         article['fuel'] = response.css("#detail_spec  tr:nth-child(8) td:nth-child(4)::text").extract_first().strip()
         article['horsepower'] = polish(response.css("#detail_spec  tr:nth-child(9) td:nth-child(4)::text").extract_first())
         article['battery'] = response.css("#detail_spec  tr:nth-child(10) td:nth-child(4)::text").extract_first().strip()
         article['body_maker'] = response.css("#detail_spec  tr:nth-child(11) td:nth-child(4)::text").extract_first().strip()
         article['body_specification'] = response.css("#detail_spec tr:nth-child(12) td:nth-child(4)::text").extract_first().strip()
         article['grade'] = response.css("#detail_spec  tr:nth-child(13) td:nth-child(4)::text").extract_first().strip()
         article['registration_type'] = response.css("#detail_spec  tr:nth-child(1) td:nth-child(6)::text").extract_first().strip()
         article['vehicle_inspection_expire_date'] = response.css("#detail_spec  tr:nth-child(2) td:nth-child(6)::text").extract_first().strip()
         article['cab_width_and_shape'] = polish(response.css("#detail_spec  tr:nth-child(3) td:nth-child(6)::text").extract_first())
         article['body_length'] =  response.css("#detail_spec  tr:nth-child(4) td:nth-child(6)::text").extract_first().strip()
         article['auxiliary_brake'] = response.css("#detail_spec  tr:nth-child(5) td:nth-child(6)::text").extract_first().strip()
         article['displacement'] = response.css("#detail_spec  tr:nth-child(7) td:nth-child(6)::text").extract_first().strip()
         article['nox'] = response.css("#detail_spec tr:nth-child(8) td:nth-child(6)::text").extract_first().strip()
         article['turbo'] = response.css("#detail_spec  tr:nth-child(9) td:nth-child(6)::text").extract_first().strip()
         article['car_history'] = response.css("#detail_spec  tr:nth-child(10) td:nth-child(6)::text").extract_first().strip()
         article['body_year'] = polish(response.css("#detail_spec  tr:nth-child(11) td:nth-child(6)::text").extract_first())
         yield article
       
                      
def polish(str):
    if not str:
        return ""
    str = str.replace(' ', '')
    str = str.replace('\n', '')
    str = str.replace('\t', '')
    str = str.strip()
    return str





       
