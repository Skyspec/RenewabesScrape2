ABOUT_TO_BUILD_HINTS = [
    "approved","determination","financial close","construction to commence",
    "contract awarded","epc","mobilisation",
]
READY_TO_COMMISSION_HINTS = [
    "commissioning","energisation","registration","hold point","grid connection complete"
]

def score_lead(rec):
    text = f"{rec.get('stage_text') or ''} {rec.get('raw_text') or ''}".lower()
    if any(k in text for k in READY_TO_COMMISSION_HINTS):
        return "ready_to_commission"
    if any(k in text for k in ABOUT_TO_BUILD_HINTS):
        return "about_to_build"
    if "tender" in text or "rfq" in text or "rft" in text:
        return "tender_signal"
    return None

def pick_service_fit(rec):
    lead = rec.get("lead_flag")
    tech = (rec.get("technology") or "").lower()
    if lead == "about_to_build":
        return "DSM_prebuild"
    if lead == "tender_signal":
        return "Progress/As-Built (depends)"
    if lead == "ready_to_commission":
        if "solar" in tech:
            return "Baseline_thermography"
        return "Commissioning_support"
    if "wind" in tech:
        return "Wind_inspection"
    return None
