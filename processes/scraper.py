# scraper.py
import asyncio
import time
from playwright.async_api import async_playwright
from config.config import SELECTORS, BASE_URL, HEADLESS_MODE, INACTIVITY_TIMEOUT, SLOW_MO
from processes.parser import GoogleMapsParser
from processes.storage import LeadStorage

class GoogleMapsScraper:
    def __init__(self, query, output_filename):
        self.query = query
        self.output_filename = output_filename
        self.storage = LeadStorage(output_filename)

    async def scroll_results_feed(self, page):
        feed_selector = SELECTORS["results_feed"]
        try:
            await page.evaluate(f"""
                const feed = document.querySelector("{feed_selector}");
                if (feed) {{
                    feed.scrollTop = feed.scrollHeight;
                }}
            """)
        except Exception as e:
            print(f"Error while scrolling: {e}")

    async def run(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=HEADLESS_MODE,
                slow_mo=SLOW_MO,
                args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
            )
            
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = await context.new_page()

            print(f"[*] Navigating to Google Maps...")
            await page.goto(BASE_URL, timeout=60000)

            # Cookie banner handling
            try:
                accept_button = page.locator("button:has-text('Accept all'), button:has-text('I agree'), form[action*='consent'] button")
                if await accept_button.count() > 0:
                    await accept_button.first.click()
                    await asyncio.sleep(2)
            except Exception:
                pass

            # Search box interaction using multi-selector fallback list
            print(f"[*] Searching for query: '{self.query}'")
            search_box_filled = False
            for selector in SELECTORS["search_inputs"]:
                try:
                    locator = page.locator(selector)
                    if await locator.count() > 0:
                        await locator.first.wait_for(state="visible", timeout=5000)
                        await locator.first.fill(self.query)
                        search_box_filled = True
                        break
                except Exception:
                    continue

            if not search_box_filled:
                raise Exception("Could not find search input using any provided selector.")

            await page.keyboard.press("Enter")
            
            # Wait for results feed
            await page.locator(SELECTORS["results_feed"]).wait_for(state="visible", timeout=15000)
            print("[*] Results feed loaded successfully. Beginning extraction loop...")

            last_lead_time = time.time()
            processed_indices = set()

            while True:
                if time.time() - last_lead_time > INACTIVITY_TIMEOUT:
                    print("\n[!] No new leads found for 2 minutes. Stopping scraper...")
                    break

                links = page.locator(SELECTORS["business_links"])
                count = await links.count()

                for i in range(count):
                    if i in processed_indices:
                        continue

                    processed_indices.add(i)

                    try:
                        item = links.nth(i)
                        await item.scroll_into_view_if_needed()
                        await item.click()
                        await asyncio.sleep(1.5)

                        lead_data = await GoogleMapsParser.parse_business_details(page)
                        saved = self.storage.save_lead(lead_data)

                        if saved:
                            last_lead_time = time.time()
                            print(f"[Saved] {lead_data.get('name')} | Phone: {lead_data.get('phone')}")
                        else:
                            print(f"[Duplicate Skipped] {lead_data.get('name')}")

                    except Exception as e:
                        print(f"[Error processing listing {i}]: {e}")
                        continue

                await self.scroll_results_feed(page)
                await asyncio.sleep(2)

            await browser.close()