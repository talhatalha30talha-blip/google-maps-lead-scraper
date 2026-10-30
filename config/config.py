# config.py
import os

BASE_URL = "https://www.google.com/maps"
HEADLESS_MODE = False
INACTIVITY_TIMEOUT = 120  # 2 minutes in seconds
SLOW_MO = 50

# Master tracking ledger stored in the data folder
TRACKING_FILE = os.path.join("data", "seen_leads.txt")

SELECTORS = {
    # Fallback list for the Google Maps search input box to prevent timeouts
    "search_inputs": [
        "input#searchboxinput",
        "input[aria-label*='Search']",
        "input[name='q']",
        "*[role='combobox']"
    ],
    "results_feed": "div[role='feed']",
    "business_links": "a.hfpxzc, div[role='feed'] a[href*='/maps/place/']",
    "business_name": "h1.DUwDvf",
    "business_rating": "div.F7nice span[aria-hidden='true']",
    "business_reviews_count": "div.F7nice span:last-child",
    "business_address": "button[data-item-id='address'] div.fontBodyMedium",
    "business_hours": "div[data-item-id='oh'] div.fontBodyMedium",
    "business_phone": "button[data-item-id^='phone:'] div.fontBodyMedium",
    "business_website": "a[data-item-id='authority'] div.fontBodyMedium",
    "plus_code": "button[data-item-id='oloc'] div.fontBodyMedium"
}