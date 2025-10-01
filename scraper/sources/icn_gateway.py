
import time, re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from .base import BaseSource

HEADERS = {"User-Agent": "SkyspecLeadBot/0.2 (+info@skyspec.com.au)"}

class ICNGateway(BaseSource):
    name = "ICN Gateway"
    BASE = "https://icn.org.au"
    LIST = "https://icn.org.au/project/"

    def search(self, states, query, limit=80):
        r = requests.get(self.LIST, headers=HEADERS, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        cards = soup.select("article a[href*='/project/']")
        count = 0
        seen = set()
        for a in cards:
            href = a.get("href")
            if not href:
                continue
            if not href.startswith("http"):
                href = urljoin(self.BASE, href)
            if href in seen:
                continue
            seen.add(href)

            try:
                pr = requests.get(href, headers=HEADERS, timeout=30)
                pr.raise_for_status()
            except Exception:
                continue

            psoup = BeautifulSoup(pr.text, "lxml")
            title_el = psoup.select_one("h1")
            title = title_el.get_text(strip=True) if title_el else "ICN Project"
            body = psoup.get_text(" ", strip=True)

            yield {
                "source_system_id": href,
                "title": title,
                "jurisdiction": None,
                "technology": None,
                "capacity_mw": None,
                "developer": None,
                "stage_text": "ICN listing/EOI",
                "status_date": None,
                "location_text": None,
                "lat": None,
                "lon": None,
                "url": href,
                "raw_text": body[:2000],
            }
            count += 1
            if count >= limit:
                break
            time.sleep(0.6)
