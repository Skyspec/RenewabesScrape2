# Australia Energy Projects Scraper — Eastern States (Starter Kit)

This starter kit helps discover **upcoming** and **commissioning** energy projects in Australia's eastern states (QLD, NSW, ACT, VIC, TAS), then flag those likely to need **DSM (pre‑build)**, **As‑Built/Progress**, **baseline thermography (solar)**, and **wind inspections**.

## Quickstart
1. Create venv and install:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run a sample:
   ```bash
   python run.py --states NSW QLD --sources nsw_major_projects qld_qtenders --query "solar OR wind" --limit 50
   ```

Outputs:
- SQLite at `data/projects.sqlite`
- CSV snapshot at `data/projects_snapshot.csv`

> Note: Portals change. You may need to adjust selectors or use Playwright for JS-heavy pages. Respect robots.txt and T&Cs.


## GitHub Automation

1. Push this project to a new GitHub repo.
2. Go to **Actions → Scrape Energy Projects (AU East)** and click **Run workflow** (or wait for the daily schedule).
3. After it completes, open the workflow run → **Artifacts** to download `projects_snapshot.csv` (and `projects.sqlite`).

> The schedule uses `0 14 * * *` (14:00 UTC), which aligns to about **1:00am Sydney** during AEDT.
> If some portals block GitHub IPs, switch to a **self‑hosted runner** or a small VM and keep this workflow file.
