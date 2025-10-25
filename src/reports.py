import os
import pandas as pd
from pathlib import Path
from jinja2 import Template
from collections import Counter
from dateutil import parser as dp
from utils import week_window_ref

ANALYZED = Path("data/reviews_analyzed.csv")
REPORTS  = Path("reports")
TPL = Path("templates/report.html.j2")

def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(ANALYZED)

    start, end = week_window_ref()
    df["created_at_dt"] = pd.to_datetime(df["created_at"], errors="coerce")
    wk = df[(df["created_at_dt"] >= start) & (df["created_at_dt"] < end)].copy()

    total = len(wk)
    pos = (wk["sentiment_label"]=="positive").sum()
    neg = (wk["sentiment_label"]=="negative").sum()
    neu = (wk["sentiment_label"]=="neutral").sum()
    # simple index: 1 for positive, 0.5 for neutral, 0 for negative
    idx = 0
    if total:
        idx = round(((pos*1.0 + neu*0.5) / total), 3)

    # topics
    topics = []
    if total:
        for ts in wk["topics"].fillna(""):
            topics.extend([t for t in ts.split(",") if t])
    top_topics = Counter(topics).most_common(5)

    # samples
    best = wk.sort_values(["sentiment_label","sentiment_score"], ascending=[True,False])
    best = best[best["sentiment_label"]=="positive"].head(5).to_dict(orient="records")
    worst = wk[wk["sentiment_label"]=="negative"].sort_values("sentiment_score", ascending=False).head(5).to_dict(orient="records")

    # render
    with open(TPL, "r", encoding="utf-8") as f:
        template = Template(f.read())
    html = template.render(
        week_label=f"{start.date()} to {end.date()}",
        total_reviews=total,
        pos=pos, neu=neu, neg=neg,
        sentiment_index=idx,
        top_topics=top_topics,
        best_samples=best,
        worst_samples=worst,
        week_rows=wk.to_dict(orient="records"),
    )
    out_path = REPORTS / f"weekly-{end.date()}.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()
