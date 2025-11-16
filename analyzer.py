import re
from dateutil import parser
from collections import defaultdict
import math

def parse_date(text):
    try:
        return parser.parse(text).date().isoformat()
    except Exception:
        return None

class TimelineBuilder:
    def __init__(self, articles):
        """
        articles: list of dicts with keys title, publishedAt, content, url, source
        """
        self.articles = articles

    def extract_milestones_from_text(self, text):
        # simple heuristic: find sentences with dates or milestone keywords
        sentences = re.split(r'(?<=[.!?])\s+', text)
        milestones = []
        keywords = ["launch", "landed", "launched", "announced", "confirmed", "arrived", "failed", "succeeded", "soft landing", "lifted off", "docked", "collision", "update", "said"]
        for s in sentences:
            for kw in keywords:
                if kw in s.lower():
                    # try to find a date in sentence
                    # look for YYYY or month names
                    m = re.search(r'(\b\d{4}\b)|\\b(January|February|March|April|May|June|July|August|September|October|November|December)\\b', s, re.I)
                    date_text = None
                    if m:
                        date_text = m.group(0)
                    milestones.append({"sentence": s.strip(), "date_hint": date_text})
                    break
        return milestones

    def build_timeline(self):
        # Collect candidate events with dates from publishedAt and sentence hints
        events = []
        for a in self.articles:
            pub = a.get("publishedAt")
            date = None
            if pub:
                try:
                    date = parser.parse(pub).date().isoformat()
                except:
                    date = None
            # title as quick event
            title = a.get("title") or ""
            events.append({"date": date or "unknown", "event": title, "sources":[a.get("source") or a.get("url")]})
            # from content
            content = a.get("content") or ""
            for m in self.extract_milestones_from_text(content):
                # attach published date as fallback
                events.append({"date": date or (m.get("date_hint") or "unknown"), "event": m.get("sentence"), "sources":[a.get("source")]})
        # normalize unknowns
        for e in events:
            if e["date"] == "unknown":
                e["date_sort"] = "9999-12-31"
            else:
                try:
                    e["date_sort"] = parser.parse(e["date"]).date().isoformat()
                except:
                    e["date_sort"] = "9999-12-31"
        # sort by date_sort
        events_sorted = sorted(events, key=lambda x: x["date_sort"])
        # compress similar events (simple dedupe)
        compressed = []
        seen = set()
        for e in events_sorted:
            key = (e["date_sort"], e["event"][:80])
            if key in seen: 
                continue
            seen.add(key)
            compressed.append({"date": e["date_sort"] if e["date_sort"]!='9999-12-31' else 'unknown', "event": e["event"], "sources": list(set(e.get("sources",[])))})
        return compressed

    def source_checks(self):
        # Very simple authenticity check: score by domain name length and presence in known list
        trusted = ["bbc.co", "reuters", "theguardian", "nytimes", "indiatoday", "thehindu", "cnn", "timesofindia"]
        scores = {}
        for a in self.articles:
            s = a.get("source") or a.get("url") or "unknown"
            name = s.lower()
            score = 0.5
            for t in trusted:
                if t in name:
                    score = 0.9
            # penalize very short/unknown
            if name == "unknown":
                score = 0.1
            scores[s] = score
        return scores
