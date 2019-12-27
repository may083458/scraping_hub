# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    no_detail_spec = scrapy.Field()
    title = scrapy.Field()
    car_maker = scrapy.Field()
    car_category =scrapy.Field()
    run_distance = scrapy.Field()
    control_number = scrapy.Field()
    price  = scrapy.Field()
    price_iclude_tax  = scrapy.Field()
    inventory  = scrapy.Field()
    type  = scrapy.Field()
    chassis_no  = scrapy.Field()
    max_load_capacity  = scrapy.Field()
    no_of_door  = scrapy.Field()
    tire_shape  = scrapy.Field()
    clutch_pedal  = scrapy.Field()
    color  = scrapy.Field()
    external_height  = scrapy.Field()
    external_width  = scrapy.Field()
    external_high  = scrapy.Field()
    body_size_height  = scrapy.Field()
    body_size_width  = scrapy.Field()
    body_size_high  = scrapy.Field()
    notes  = scrapy.Field()
    notices  = scrapy.Field()
    common_name  = scrapy.Field()
    first_year_registration  = scrapy.Field()
    capacity  = scrapy.Field()
    roof_shape  = scrapy.Field()
    drive_system  = scrapy.Field()
    mission  = scrapy.Field()
    engine_model  = scrapy.Field()
    fuel  = scrapy.Field()
    horsepower  = scrapy.Field()
    battery  = scrapy.Field()
    body_maker  = scrapy.Field()
    body_specification  = scrapy.Field()
    grade  = scrapy.Field()
    registration_type  = scrapy.Field()
    vehicle_inspection_expire_date  = scrapy.Field()
    cab_width_and_shape  = scrapy.Field()
    body_length  = scrapy.Field()
    auxiliary_brake  = scrapy.Field()
    displacement  = scrapy.Field()
    nox  = scrapy.Field()
    turbo  = scrapy.Field()
    car_history  = scrapy.Field()
    body_year  = scrapy.Field()
    car_option = scrapy.Field()
    url = scrapy.Field()

