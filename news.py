import feedparser, anthropic

client = anthropic.Anthropic()

FEEDS = {
    "France": ["https://www.lemonde.fr/rss/une.xml"],
    "Monde": ["http://feeds.bbci.co.uk/news/world/rss.xml"],
    "Cameroun": ["https://news.google.com/rss/search?q=Cameroun&hl=fr&gl=CM&ceid=CM:fr"],
}

def fetch_headlines(urls, n=8):
    items = []
    for url in urls:
        for e in feedparser.parse(url).entries[:n]:
            items.append(f"- {e.title} : {e.get('summary', '')[:200]}")
    return "\n".join(items)

def news_briefing():
    sections = [f"## {zone}\n{fetch_headlines(urls)}"
                for zone, urls in FEEDS.items() if urls]
    prompt = ("Voici les titres du jour. Rédige en français un briefing court : "
              "pour chaque zone, 3 à 5 points essentiels, une phrase chacun.\n\n"
              + "\n\n".join(sections))
    r = client.messages.create(model="claude-sonnet-5-5", max_tokens=4000,
                               messages=[{"role": "user", "content": prompt}])
    return "".join(b.text for b in r.content if b.type == "text")

if __name__ == "__main__":
    print(news_briefing())