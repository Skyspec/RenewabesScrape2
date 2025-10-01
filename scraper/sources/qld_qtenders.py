import time
import requests
from bs4 import BeautifulSoup
from .base import BaseSource

HEADERS = {"User-Agent": "SkyspecLeadBot/0.1 (+info@skyspec.com.au)"}

class QLDQTenders(BaseSource):
    name = "QLD QTenders"
    BASE_URL = "https://www.hpw.qld.gov.au/qtenders/tender/search/tenders"

    def search(self, states, query, limit=50):
        if "QLD" not in states:
            return []
        params = {"keyword": query or "solar OR wind OR energy OR substation"}
        r = requests.get(self.BASE_URL, params=params, headers=HEADERS, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        rows = soup.select("table tbody tr")
        count = 0
        for row in rows:
            a = row.select_one("a[href]")
            href = a.get("href") if a else None
            if href and href.startswith("/"):
                href = "https://www.hpw.qld.gov.au" + href
            cols = [td.get_text(' ', strip=True) for td in row.select("td")]
            title = cols[0] if cols else "QTenders item"
            yield {
                "source_system_id": href or title,
                "title": title,
                "jurisdiction": "QLD",
                "technology": None,
                "capacity_mw": None,
                "developer": None,
                "stage_text": "tender",
                "status_date": None,
                "location_text": None,
                "lat": None,
                "lon": None,
                "url": href,
                "raw_text": " | ".join(cols)[:2000],
            }
            count += 1
            if count >= limit:
                break
            time.sleep(0.5)
