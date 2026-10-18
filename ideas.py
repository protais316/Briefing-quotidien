import json, os, sys, datetime, anthropic

client = anthropic.Anthropic()
MEMORY_FILE = "ideas_history.json"

def load_history():
    # Lit la liste des idées déjà proposées (liste vide si le fichier n'existe pas encore)
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    # Réécrit le fichier avec l'historique mis à jour
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def daily_idea(mode="new"):
    history = load_history()
    titles = [h["title"] for h in history]

    if mode == "deepen" and history:
        last = history[-1]
        prompt = (f"Voici une idée de business passif en ligne déjà proposée :\n{last['content']}\n\n"
                  "Approfondis-la : plan d'action sur 30 jours, outils nécessaires, "
                  "budget de départ, et principaux risques. Première ligne : le titre seul.")
    else:
        prompt = ("Propose UNE idée de business passif en ligne, réaliste pour un étudiant "
                  "en data science et IA avec un petit budget. "
                  f"Évite ces idées déjà proposées : {titles}. "
                  "Première ligne : le titre seul. Ensuite : le principe, le public visé, "
                  "comment démarrer en 3 étapes, le temps nécessaire et les risques. "
                  "Sois réaliste : ne promets aucun revenu garanti.")

    r = client.messages.create(model="claude-sonnet-5-5", max_tokens=4000,
                               messages=[{"role": "user", "content": prompt}])
    text = "".join(b.text for b in r.content if b.type == "text")

    title = text.split("\n")[0].lstrip("# ").strip()
    history.append({"date": datetime.date.today().isoformat(),
                    "mode": mode, "title": title, "content": text})
    save_history(history)
    return text

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "new"
    print(daily_idea(mode))