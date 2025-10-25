import pandas as pd
from pathlib import Path
from transformers import pipeline

DATA_PATH = Path("data/reviews.csv")
OUT_PATH  = Path("data/reviews_analyzed.csv")

def infer_topics(text:str):
    text_l = (text or "").lower()
    m = {
        "food":["taste","delicious","bland","spicy","undercooked","overcooked","portion","fresh"],
        "service":["server","staff","rude","friendly","waiter","service","attentive"],
        "wait_time":["wait","line","queue","slow","delay","quick"],
        "price":["price","expensive","cheap","value","overpriced"],
        "ambience":["ambience","atmosphere","music","noise","decor","vibe"],
        "cleanliness":["dirty","clean","hygiene","smell"],
        "delivery":["delivery","ubereats","doordash","skip","cold","late"],
        "reservations":["reservation","booked","table","seating"],
    }
    topics=set()
    for k, words in m.items():
        if any(w in text_l for w in words): topics.add(k)
    return ",".join(sorted(topics)) if topics else ""

def main():
    df = pd.read_csv(DATA_PATH)
    df = df.sort_values("created_at")
    clf = pipeline("sentiment-analysis")
    sentiments = clf(df["text"].fillna("").tolist())
    df["sentiment_label"] = [s["label"].lower() for s in sentiments]  # positive/negative
    df["sentiment_score"] = [round(float(s["score"]),4) for s in sentiments]
    df.loc[df["text"].fillna("").str.len()<5,"sentiment_label"]="neutral"
    df["topics"] = df["text"].fillna("").apply(infer_topics)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

if __name__ == "__main__": main()
