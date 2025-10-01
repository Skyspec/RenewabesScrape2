from datetime import datetime
from .heuristics import score_lead, pick_service_fit

def normalise_record(raw, source_name):
    now = datetime.utcnow().isoformat()
    rec = {
        "source_system_id": raw.get("source_system_id") or raw.get("url") or raw.get("title"),
        "source_name": source_name,
        "title": raw.get("title"),
        "jurisdiction": raw.get("jurisdiction"),
        "technology": raw.get("technology"),
        "capacity_mw": raw.get("capacity_mw"),
        "developer": raw.get("developer"),
        "stage_text": raw.get("stage_text"),
        "status_date": raw.get("status_date"),
        "location_text": raw.get("location_text"),
        "lat": raw.get("lat"),
        "lon": raw.get("lon"),
        "url": raw.get("url"),
        "raw_text": raw.get("raw_text"),
        "lead_flag": None,
        "service_fit": None,
        "first_seen": now,
        "last_seen": now,
    }
    rec["lead_flag"] = score_lead(rec)
    rec["service_fit"] = pick_service_fit(rec)
    return rec
