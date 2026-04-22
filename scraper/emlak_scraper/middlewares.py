"""Scrapy middleware'leri — User-Agent rotasyonu vb."""
import random


class RotateUserAgentMiddleware:
    """User-Agent'ları rotasyona sokar."""

    USER_AGENTS = [
        "EmlakTahminBot/1.0 (Bitirme Projesi; iletisim@example.com)",
        # Ek varyantlar eklenebilir
    ]

    def process_request(self, request, spider):
        request.headers["User-Agent"] = random.choice(self.USER_AGENTS)
