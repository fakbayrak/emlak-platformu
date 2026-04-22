"""Scrapy Item tanımı — toplanan alanlar."""
import scrapy


class ListingItem(scrapy.Item):
    # Konum
    city = scrapy.Field()
    district = scrapy.Field()
    neighborhood = scrapy.Field()

    # Fiziksel özellikler
    m2 = scrapy.Field()
    room_count = scrapy.Field()
    building_age = scrapy.Field()
    floor = scrapy.Field()
    heating_type = scrapy.Field()
    furnished = scrapy.Field()
    has_elevator = scrapy.Field()
    has_parking = scrapy.Field()

    # Fiyat ve meta
    price = scrapy.Field()
    listing_type = scrapy.Field()   # "sale" | "rent"
    listing_date = scrapy.Field()

    # İzlenebilirlik (KİŞİSEL VERİ TOPLANMAZ)
    source_url_hash = scrapy.Field()
