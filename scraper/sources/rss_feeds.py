
import time, re, xml.etree.ElementTree as ET
import requests
from .base import BaseSource

HEADERS = {"User-Agent": "SkyspecLeadBot/0.2 (+info@skyspec.com.au)"}

KEY_HINTS_ABOUT_BUILD = ["financial close","ntp","notice to proceed","construction to begin","contract awarded","epc"]
KEY_HINTS_READY_TO_COMMISSION = ["commissioning","energisation","first power","registration","r2","grid connection complete"]

class RSSFeeds(BaseSource):
    name = "RSS Feeds"

    def search(self, states, query, limit=120):
        import pathlib, yaml
        feeds_path = pathlib.Path(__file__).resolve().parents[2] / "data" / "feeds.yaml"
        if not feeds_path.exists():
            return []
        feeds = yaml.safe_load(feeds_path.read_text(encoding="utf-8")) or []
        count = 0
        for entry in feeds:
            url = entry.get("url")
            if not url:
                continue
            try:
                r = requests.get(url, headers=HEADERS, timeout=30)
                r.raise_for_status()
            except Exception:
                continue
            items = self._parse_items(r.text)
            kw = [k.lower() for k in (entry.get("keywords") or [])]
            for it in items:
                title = (it.get("title") or "").strip()
                summary = (it.get("summary") or it.get("description") or "")
                link = it.get("link")
                tl = f"{title} {summary}".lower()

                ok = True
                if query:
                    qs = [x.strip().lower() for x in re.split(r"\s+OR\s+|\s+", query) if x.strip()]
                    ok = any(q in tl for q in qs)
                if kw:
                    ok = ok and any(k in tl for k in kw)

                if not ok:
                    continue

                yield {
                    "source_system_id": link or title,
                    "title": title or "RSS item",
                    "jurisdiction": None,
                    "technology": None,
                    "capacity_mw": None,
                    "developer": None,
                    "stage_text": self._guess_stage(tl),
                    "status_date": it.get("pubDate"),
                    "location_text": None,
                    "lat": None,
                    "lon": None,
                    "url": link,
                    "raw_text": summary[:2000],
                }
                count += 1
                if count >= limit:
                    return

    def _parse_items(self, xml_text):
        items = []
        try:
            root = ET.fromstring(xml_text)
        except Exception:
            return items
        for item in root.findall(".//item"):
            items.append({
                "title": (item.findtext("title") or ""),
                "link": (item.findtext("link") or ""),
                "summary": (item.findtext("description") or ""),
                "pubDate": (item.findtext("pubDate") or ""),
            })
        for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
            link_el = entry.find("{http://www.w3.org/2005/Atom}link")
            link = link_el.get("href") if link_el is not None else ""
            summ = entry.findtext("{http://www.w3.org/2005/Atom}summary") or entry.findtext("{http://www.w3.org/2005/Atom}content") or ""
            items.append({
                "title": (entry.findtext("{http://www.w3.org/2005/Atom}title") or ""),
                "link": link,
                "summary": summ,
                "pubDate": (entry.findtext("{http://www.w3.org/2005/Atom}updated") or ""),
            })
        return items

    def _guess_stage(self, tl):
        if any(k in tl for k in KEY_HINTS_READY_TO_COMMISSION):
            return "ready_to_commission (feed)"
        if any(k in tl for k in KEY_HINTS_ABOUT_BUILD):
            return "about_to_build (feed)"
        if "tender" in tl or "rfq" in tl or "rft" in tl or "eoi" in tl:
            return "tender/eoi (feed)"
        return "news"
