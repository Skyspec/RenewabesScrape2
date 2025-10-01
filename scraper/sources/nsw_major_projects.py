import time
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
from .base import BaseSource

HEADERS = {"User-Agent": "SkyspecLeadBot/0.1 (+info@skyspec.com.au)"}

class NSWMajorProjects(BaseSource):
    name = "NSW Major Projects"
    BASE_URL = "https://www.planningportal.nsw.gov.au/major-projects/projects"

    def search(self, states, query, limit=50):
        if "NSW" not in states:
            return []
        params = {"search": query or "solar OR wind"}
        url = f"{self.BASE_URL}?{urlencode(params)}"
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        cards = soup.select("article.project, div.views-row")
        count = 0
        for c in cards:
            a = c.select_one("a[href]")
            h = a.get("href") if a else None
            if h and h.startswith("/"):
                h = "https://www.planningportal.nsw.gov.au" + h
            title_el = c.select_one("h2, h3, .project-title")
            title = title_el.get_text(strip=True) if title_el else (a.get_text(strip=True) if a else "NSW Major Project")
            summary = c.get_text(" ", strip=True)
            yield {
                "source_system_id": h or title,
                "title": title,
                "jurisdiction": "NSW",
                "technology": None,
                "capacity_mw": None,
                "developer": None,
                "stage_text": "unknown",
                "status_date": None,
                "location_text": None,
                "lat": None,
                "lon": None,
                "url": h,
                "raw_text": summary[:2000],
            }
            count += 1
            if count >= limit:
                break
            time.sleep(0.5)
