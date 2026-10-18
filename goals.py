import json, os, datetime

GOALS_FILE = "goals.json"

def load_goals():
    # Lit la liste des objectifs (liste vide si le fichier n'existe pas encore)
    if os.path.exists(GOALS_FILE):
        with open(GOALS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_goals(goals):
    with open(GOALS_FILE, "w", encoding="utf-8") as f:
        json.dump(goals, f, ensure_ascii=False, indent=2)

def add_goal(text, period="jour"):
    # period vaut "jour" ou "semaine"
    goals = load_goals()
    new_id = max([g["id"] for g in goals], default=0) + 1
    goals.append({"id": new_id, "text": text, "period": period,
                  "created": datetime.date.today().isoformat(),
                  "done": False, "done_date": None})
    save_goals(goals)
    return new_id

def complete_goal(goal_id):
    goals = load_goals()
    for g in goals:
        if g["id"] == goal_id:
            g["done"] = True
            g["done_date"] = datetime.date.today().isoformat()
            save_goals(goals)
            return True
    return False

def pending_goals():
    return [g for g in load_goals() if not g["done"]]