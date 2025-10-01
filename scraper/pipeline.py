from pathlib import Path
import pandas as pd
from .sources import AVAILABLE_SOURCES
from .utils.db import DB
from .utils.normalise import normalise_record

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

def run_pipeline(states, sources, query, limit=100):
    db = DB(DATA_DIR / "projects.sqlite")
    all_rows = []

    for key in sources:
        cls = AVAILABLE_SOURCES.get(key)
        if not cls:
            print(f"[WARN] Unknown source: {key}")
            continue
        src = cls()
        print(f"[INFO] Running: {src.name}")
        try:
            for raw in src.search(states=states, query=query, limit=limit):
                rec = normalise_record(raw, src.name)
                db.upsert_project(rec)
                all_rows.append(rec)
        except Exception as e:
            print(f"[ERROR] {src.name} failed: {e}")

    if all_rows:
        df = pd.DataFrame(all_rows).drop_duplicates(subset=["source_system_id","source_name"])
        df.to_csv(DATA_DIR / "projects_snapshot.csv", index=False)
        print("[OK] Wrote snapshot CSV")
    else:
        print("[WARN] No rows produced")
