import datetime, os
from news import news_briefing
from ideas import daily_idea
from videos import pick_video

def safe(title, func, *args):
    # Exécute un module ; si l'un plante, les autres continuent
    try:
        return f"## {title}\n\n{func(*args)}"
    except Exception as e:
        return f"## {title}\n\nSection indisponible ({type(e).__name__} : {e})"

def build_briefing():
    today = datetime.date.today().strftime("%d/%m/%Y")
    if datetime.date.today().weekday() in [3, 6]:
        mode = "deepen"
    else:
        mode = "new"
    parts = [
        f"# Briefing du {today}",
        safe("Actualité", news_briefing),
        safe("Idée de business", daily_idea, mode),
        safe("Vidéo du jour", pick_video),
    ]
    return "\n\n".join(parts)

if __name__ == "__main__":
    briefing = build_briefing()
    os.makedirs("briefings", exist_ok=True)
    path = os.path.join("briefings", f"{datetime.date.today().isoformat()}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(briefing)
    print(briefing)
    print(f"\n(Enregistré dans {path})")