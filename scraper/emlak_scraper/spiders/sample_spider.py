"""
Örnek spider iskeleti.

UYARI: Bu dosya gerçek bir siteyi hedeflemez. Kendi seçeceğiniz sitenin
robots.txt ve kullanım şartlarını onayladıktan sonra allowed_domains,
start_urls ve parse() metodunu doldurunuz.
"""
from emlak_scraper.spiders.base_spider import BaseListingSpider


class SampleSpider(BaseListingSpider):
    name = "sample"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com/emlak/satilik/istanbul/kadikoy"]

    custom_settings = {
        "DOWNLOAD_DELAY": 5,
        "CONCURRENT_REQUESTS": 1,
    }

    def parse(self, response):
        """
        TODO:
        1) Liste sayfasındaki ilanların detay linklerini yakala
        2) Her detay linkine request at (parse_detail)
        3) Sonraki sayfa linkini takip et
        """
        for link in response.css("a.listing-card::attr(href)").getall():
            yield response.follow(link, callback=self.parse_detail)

        next_page = response.css("a.next-page::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        """Tek ilanın detay sayfasını parse eder."""
        from emlak_scraper.pipelines import url_to_hash

        item = self.new_item()
        item["source_url_hash"] = url_to_hash(response.url)
        item["city"] = response.css("span.city::text").get()
        item["district"] = response.css("span.district::text").get()
        item["m2"] = self.clean_int(response.css("span.m2::text").get())
        item["price"] = self.clean_price(response.css("span.price::text").get())
        item["listing_type"] = "sale"
        # ... diğer alanlar
        yield item
