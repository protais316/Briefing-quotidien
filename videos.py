import feedparser, json, os, anthropic

client = anthropic.Anthropic()
HISTORY_FILE = "videos_history.json"

CHANNELS = {
    "StatQuest with Josh Starmer": "UCtYLUTtgS3k1Fg4y5tAhLbw",
    "3Blue1Brown": "UCYO_jab_esuFRV4b17AJtAw",
    "Andrej Karpathy": "UCXUPKJO5MZQN11PqgIvyuvQ",
    "Umar Jamil": "UCtAcpQcYerN8xxZJYTfWBMw",
    "Machine Learnia": "UCmpptkXu8iIFe6kfDK5o7VQ"# à compléter avec vos chaînes
}

def load_seen():
    # Liste des liens de vidéos déjà proposées
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_seen(seen):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(seen, f, ensure_ascii=False, indent=2)

def fetch_recent_videos(n=5):
    videos = []
    for name, channel_id in CHANNELS.items():
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        for e in feedparser.parse(url).entries[:n]:
            videos.append({"channel": name, "title": e.title, "link": e.link})
    return videos

def pick_video():
    seen = load_seen()
    videos = [v for v in fetch_recent_videos() if v["link"] not in seen]
    if not videos:
        return "Aucune nouvelle vidéo à proposer aujourd'hui."

    listing = "\n".join(f"{i}. [{v['channel']}] {v['title']}"
                        for i, v in enumerate(videos))
    prompt = ("Je suis étudiant en data science et IA, à la recherche d'un stage. "
              "Voici des vidéos récentes :\n" + listing +
              "\n\nChoisis la plus utile à regarder aujourd'hui. "
              "Réponds avec uniquement son numéro sur la première ligne, "
              "puis en 2 phrases, en français, pourquoi la regarder.")
    r = client.messages.create(model="claude-sonnet-5-5", max_tokens=4000,
                               messages=[{"role": "user", "content": prompt}])
    text = "".join(b.text for b in r.content if b.type == "text").strip()
    lines = text.split("\n")

    try:
        choice = videos[int(lines[0].strip().strip("."))]
    except (ValueError, IndexError):
        return text

    save_seen(seen + [choice["link"]])
    return (f"{choice['title']} ({choice['channel']})\n{choice['link']}\n\n"
            + "\n".join(lines[1:]).strip())

if __name__ == "__main__":
    print(pick_video())