import os, csv, time
import requests
from datetime import datetime
from dateutil import tz
from pathlib import Path

DATA_PATH = Path("data/reviews.csv")

API_KEY  = os.getenv("GOOGLE_PLACES_API_KEY")
PLACE_ID = os.getenv("GOOGLE_PLACE_ID")   # your restaurant Place ID

def fetch_google_reviews():
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": PLACE_ID,
        "fields": "reviews",
        "reviews_sort": "newest",
        "key": API_KEY,
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    payload = r.json()
    reviews = payload.get("result", {}).get("reviews", []) or []
    out = []
    for rv in reviews:
        created = datetime.fromtimestamp(rv["time"], tz=tz.UTC).astimezone(tz.gettz("America/Toronto"))
        out.append({
            "platform": "google",
            "review_id": str(rv["time"]),            # surrogate id
            "business_id": PLACE_ID,
            "author_name": rv.get("author_name"),
            "rating": rv.get("rating"),
            "text": (rv.get("text") or "").strip(),
            "language": rv.get("language") or "",
            "created_at": created.isoformat(),
            "fetched_at": datetime.now(tz.gettz("America/Toronto")).isoformat(),
            "review_url": "",                         # API doesn't give per-review URL
        })
    return out

def load_existing():
    if not DATA_PATH.exists():
        return {}
    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return { (r["platform"], r["review_id"]): r for r in reader }

def save_merged(rows_dict):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["platform","review_id","business_id","author_name","rating","text","language","created_at","fetched_at","review_url"]
    with open(DATA_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for _, row in rows_dict.items():
            w.writerow(row)

def main():
    assert API_KEY and PLACE_ID, "Set GOOGLE_PLACES_API_KEY and GOOGLE_PLACE_ID"
    fresh = fetch_google_reviews()
    existing = load_existing()
    for r in fresh:
        existing[(r["platform"], r["review_id"])] = r
    save_merged(existing)

if __name__ == "__main__":
    main()
