"""Scrapy ayarları — etik scraping için konfigüre edilmiştir."""
import os

BOT_NAME = "emlak_scraper"
SPIDER_MODULES = ["emlak_scraper.spiders"]
NEWSPIDER_MODULE = "emlak_scraper.spiders"

# robots.txt'ye uymak ZORUNLUDUR
ROBOTSTXT_OBEY = True

# Etik rate limiting
USER_AGENT = os.getenv("SCRAPER_USER_AGENT",
                      "EmlakTahminBot/1.0 (Bitirme Projesi; iletisim@example.com)")
DOWNLOAD_DELAY = float(os.getenv("SCRAPER_DOWNLOAD_DELAY", "3"))
CONCURRENT_REQUESTS = int(os.getenv("SCRAPER_CONCURRENT_REQUESTS", "2"))
CONCURRENT_REQUESTS_PER_DOMAIN = 2

# AutoThrottle — otomatik rate limit
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 30
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# HTTP cache (geliştirme esnasında tekrar tekrar istek atmayı önler)
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400  # 1 gün
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 429]

# Retry
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]

# Playwright (dinamik sayfalar için)
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
PLAYWRIGHT_BROWSER_TYPE = "chromium"

# Pipelines
ITEM_PIPELINES = {
    "emlak_scraper.pipelines.DuplicatesPipeline": 100,
    "emlak_scraper.pipelines.PostgresPipeline": 300,
}

# Feed export
FEED_EXPORT_ENCODING = "utf-8"

# Log level
LOG_LEVEL = "INFO"
