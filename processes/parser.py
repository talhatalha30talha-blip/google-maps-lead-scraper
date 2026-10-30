# parser.py
import asyncio
from config.config import SELECTORS

class GoogleMapsParser:
    @staticmethod
    async def extract_text_safely(page, selector):
        try:
            locator = page.locator(selector)
            if await locator.count() > 0:
                text = await locator.first.inner_text()
                return text.strip() if text else "N/A"
        except Exception:
            pass
        return "N/A"

    @classmethod
    async def parse_business_details(cls, page):
        await asyncio.sleep(1.0)

        name = await cls.extract_text_safely(page, SELECTORS["business_name"])
        rating = await cls.extract_text_safely(page, SELECTORS["business_rating"])
        reviews_count = await cls.extract_text_safely(page, SELECTORS["business_reviews_count"])
        address = await cls.extract_text_safely(page, SELECTORS["business_address"])
        hours = await cls.extract_text_safely(page, SELECTORS["business_hours"])
        phone = await cls.extract_text_safely(page, SELECTORS["business_phone"])
        website = await cls.extract_text_safely(page, SELECTORS["business_website"])
        plus_code = await cls.extract_text_safely(page, SELECTORS["plus_code"])

        return {
            "name": name,
            "rating": rating,
            "reviews_count": reviews_count,
            "address": address,
            "hours": hours,
            "phone": phone,
            "website": website,
            "plus_code": plus_code
        }