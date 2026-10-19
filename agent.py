import json, datetime, anthropic, os
import goals

client = anthropic.Anthropic()
MODEL = "claude-sonnet-5-5"
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
HISTORY_FILE = "chat_history.json"
MAX_MESSAGES = 40

def load_history():
    # Relit les messages enregistrés (liste vide si le fichier n'existe pas)
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(saved):
    # Ne garde que les 40 derniers messages, puis écrit le fichier
    del saved[:-MAX_MESSAGES]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(saved, f, ensure_ascii=False, indent=2)

TOOLS = [
    {"name": "list_goals",
     "description": "Liste les objectifs de l'utilisateur avec leur numéro, "
                    "leur date et leur heure prévues.",
     "input_schema": {"type": "object", "properties": {
         "status": {"type": "string", "enum": ["pending", "done", "all"]}}}},
    {"name": "add_goal",
     "description": "Ajoute un objectif ou une tâche. Dates au format AAAA-MM-JJ, "
                    "heures au format HH:MM.",
     "input_schema": {"type": "object", "properties": {
         "text": {"type": "string"},
         "period": {"type": "string", "enum": ["jour", "semaine"]},
         "due_date": {"type": "string"},
         "due_time": {"type": "string"}},
         "required": ["text"]}},
    {"name": "complete_goal",
     "description": "Marque un objectif comme accompli, à partir de son numéro.",
     "input_schema": {"type": "object", "properties": {
         "goal_id": {"type": "integer"}},
         "required": ["goal_id"]}},
]

def run_tool(name, args):
    if name == "list_goals":
        status = args.get("status", "pending")
        items = goals.load_goals()
        if status == "pending":
            items = [g for g in items if not g["done"]]
        elif status == "done":
            items = [g for g in items if g["done"]]
        return json.dumps(items, ensure_ascii=False) if items else "Aucun objectif."
    if name == "add_goal":
        new_id = goals.add_goal(args["text"], args.get("period", "jour"),
                                args.get("due_date"), args.get("due_time"))
        return f"Objectif ajouté avec le numéro {new_id}."
    if name == "complete_goal":
        ok = goals.complete_goal(args["goal_id"])
        return "Objectif marqué comme fait." if ok else "Numéro introuvable."
    return "Outil inconnu."

def system_prompt():
    now = datetime.datetime.now()
    return (
        "Tu es l'assistant personnel de Protais, étudiant en data science et IA. "
        f"Nous sommes {JOURS[now.weekday()]} {now.date().isoformat()} (AAAA-MM-JJ) "
        f"et il est {now.strftime('%H:%M')}. "
        "Utilise cette date et cette heure pour comprendre « demain », « vendredi », "
        "« dans deux heures », etc. Ne propose jamais un créneau déjà passé. "
        "Réponds toujours en français, de façon concise. "
        "Gère ses objectifs avec tes outils. "
        "S'il ne donne pas d'heure, consulte d'abord ses objectifs du jour concerné, "
        "propose un créneau libre et demande confirmation avant d'enregistrer. "
        "Ne marque un objectif comme fait que s'il le dit clairement."
    )

def chat(saved, user_message):
    messages = saved + [{"role": "user", "content": user_message}]
    while True:
        r = client.messages.create(model=MODEL, max_tokens=4000,
                                   system=system_prompt(), tools=TOOLS,
                                   messages=messages)
        messages.append({"role": "assistant", "content": r.content})
        if r.stop_reason != "tool_use":
            answer = "".join(b.text for b in r.content if b.type == "text")
            break
        results = [{"type": "tool_result", "tool_use_id": b.id,
                    "content": run_tool(b.name, b.input)}
                   for b in r.content if b.type == "tool_use"]
        messages.append({"role": "user", "content": results})

    saved.append({"role": "user", "content": user_message})
    saved.append({"role": "assistant", "content": answer or "(Action effectuée.)"})
    save_history(saved)
    return answer

if __name__ == "__main__":
    saved = load_history()
    print(f"Assistant prêt ({len(saved) // 2} échanges en mémoire). Tapez 'quit' pour sortir.")
    while True:
        msg = input("Vous : ")
        if msg.strip().lower() in ("quit", "exit"):
            break
        print("Agent :", chat(saved, msg))