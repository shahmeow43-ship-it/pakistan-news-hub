#!/usr/bin/env python3
"""Fetch headline metadata from RSS feeds and publish a small JSON index."""
import json, re, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from html import unescape

FEEDS = [
    ("Pakistan", "Google News · Pakistan", "https://news.google.com/rss/search?q=Pakistan&hl=en-PK&gl=PK&ceid=PK:en"),
    ("World", "BBC News", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("World", "Google News · World", "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en&gl=US&ceid=US:en"),
]

def clean(value):
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", unescape(value)).strip()

def get_text(node, *paths):
    for path in paths:
        found = node.find(path)
        if found is not None and found.text:
            return found.text.strip()
    return ""

articles, seen = [], set()
for category, source, url in FEEDS:
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"PakistanNewsHub/1.0 (RSS headline index)"})
        with urllib.request.urlopen(req, timeout=20) as response:
            xml = response.read()
        root = ET.fromstring(xml)
        items = root.findall(".//item")
        if not items:
            # Atom fallback
            ns = {"a":"http://www.w3.org/2005/Atom"}
            entries = root.findall(".//a:entry", ns)
            for e in entries:
                title = get_text(e, "{http://www.w3.org/2005/Atom}title")
                link_el = e.find("{http://www.w3.org/2005/Atom}link")
                link = link_el.attrib.get("href","") if link_el is not None else ""
                summary = get_text(e, "{http://www.w3.org/2005/Atom}summary")
                pub = get_text(e, "{http://www.w3.org/2005/Atom}updated")
                items.append((title, link, summary, pub))
            atom_mode = True
        else:
            atom_mode = False
        for item in items:
            if atom_mode:
                title, link, summary, pub = item
            else:
                title = get_text(item, "title")
                link = get_text(item, "link")
                summary = get_text(item, "description")
                pub = get_text(item, "pubDate")
            title, link, summary = clean(title), (link or "").strip(), clean(summary)
            if not title or not link or link in seen:
                continue
            seen.add(link)
            date = pub
            try:
                date = parsedate_to_datetime(pub).astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            except Exception:
                try:
                    date = datetime.fromisoformat(pub.replace("Z","+00:00")).strftime("%Y-%m-%d %H:%M")
                except Exception:
                    pass
            # Google News sometimes appends the publisher after " - "
            actual_source = source
            if "Google News" in source and " - " in title:
                maybe_title, maybe_source = title.rsplit(" - ", 1)
                if maybe_title and maybe_source:
                    title, actual_source = maybe_title, maybe_source
            articles.append({"title":title, "url":link, "summary":summary[:420], "date":date, "category":category, "source":actual_source})
    except Exception as exc:
        print(f"Feed failed: {source}: {exc}")

articles.sort(key=lambda x: x.get("date",""), reverse=True)
out = {"updated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "articles": articles[:90]}
Path("articles.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {len(out['articles'])} headlines.")
if not out["articles"]:
    raise SystemExit("No feed items fetched; failing this run so it can be checked.")
