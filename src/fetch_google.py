import os, csv, requests
from datetime import datetime, timezone
from pathlib import Path

DATA_PATH = Path("data/reviews.csv")
API_KEY  = os.getenv("GOOGLE_PLACES_API_KEY")
PLACE_ID = os.getenv("GOOGLE_PLACE_ID")

def fetch_google_reviews():
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {"place_id": PLACE_ID, "fields": "reviews", "reviews_sort": "newest", "key": API_KEY}
    r = requests.get(url, params=params, timeout=30); r.raise_for_status()
    reviews = (r.json().get("result", {}) or {}).get("reviews", []) or []
    out = []
    for rv in reviews:
        created = datetime.fromtimestamp(rv["time"], tz=timezone.utc).astimezone()
        out.append({
            "platform":"google","review_id":str(rv["time"]),"business_id":PLACE_ID,
            "author_name":rv.get("author_name"),"rating":rv.get("rating"),
            "text":(rv.get("text") or "").strip(),"language":rv.get("language") or "",
            "created_at":created.isoformat(),"fetched_at":datetime.now().isoformat(),
            "review_url":""
        })
    return out

def load_existing():
    if not DATA_PATH.exists(): return {}
    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        return {(r["platform"], r["review_id"]): r for r in csv.DictReader(f)}

def save_merged(rows_dict):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["platform","review_id","business_id","author_name","rating","text","language","created_at","fetched_at","review_url"]
    with open(DATA_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames); w.writeheader()
        for _, row in rows_dict.items(): w.writerow(row)

def main():
    assert API_KEY and PLACE_ID, "Set GOOGLE_PLACES_API_KEY and GOOGLE_PLACE_ID"
    fresh = fetch_google_reviews(); existing = load_existing()
    for r in fresh: existing[(r["platform"], r["review_id"])] = r
    save_merged( clear
clear
clc
cat > src/fetch_google.py <<'EOF'
import os, csv, requests
from datetime import datetime, timezone
from pathlib import Path

DATA_PATH = Path("data/reviews.csv")
API_KEY  = os.getenv("GOOGLE_PLACES_API_KEY")
PLACE_ID = os.getenv("GOOGLE_PLACE_ID")

def fetch_google_reviews():
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {"place_id": PLACE_ID, "fields": "reviews", "reviews_sort": "newest", "key": API_KEY}
    r = requests.get(url, params=params, timeout=30); r.raise_for_status()
    reviews = (r.json().get("result", {}) or {}).get("reviews", []) or []
    out = []
    for rv in reviews:
        created = datetime.fromtimestamp(rv["time"], tz=timezone.utc).astimezone()
        out.append({
            "platform":"google","review_id":str(rv["time"]),"business_id":PLACE_ID,
            "author_name":rv.get("author_name"),"rating":rv.get("rating"),
            "text":(rv.get("text") or "").strip(),"language":rv.get("language") or "",
            "created_at":created.isoformat(),"fetched_at":datetime.now().isoformat(),
            "review_url":""
        })
    return out

def load_existing():
    if not DATA_PATH.exists(): return {}
    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        return {(r["platform"], r["review_id"]): r for r in csv.DictReader(f)}

def save_merged(rows_dict):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["platform","review_id","business_id","author_name","rating","text","language","created_at","fetched_at","review_url"]
    with open(DATA_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames); w.writeheader()
        for _, row in rows_dict.items(): w.writerow(row)

def main():
    assert API_KEY and PLACE_ID, "Set GOOGLE_PLACES_API_KEY and GOOGLE_PLACE_ID"
    fresh = fetch_google_reviews(); existing = load_existing()
    for r in fresh: existing[(r["platform"], r["review_id"])] = r
    save_merged(existing)

if __name__ == "__main__": main()
