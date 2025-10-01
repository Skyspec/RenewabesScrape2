import argparse
from scraper.pipeline import run_pipeline
from scraper.sources import AVAILABLE_SOURCES

def main():
    parser = argparse.ArgumentParser(description="Energy Projects Scraper — Eastern (AU)")
    parser.add_argument("--states", nargs="+", default=["NSW","QLD","VIC","ACT","TAS"])
    parser.add_argument("--sources", nargs="+", default=list(AVAILABLE_SOURCES.keys()))
    parser.add_argument("--query", default="")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    run_pipeline(states=args.states, sources=args.sources, query=args.query, limit=args.limit)

if __name__ == "__main__":
    main()
