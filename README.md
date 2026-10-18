\# Briefing quotidien : un agent IA personnel pour un étudiant en filière data science et intelligence artificielle



Agent écrit en Python qui prépare chaque jour un briefing personnalisé

(actualité, idée de business, vidéo à regarder) à l'aide de l'API Claude.



\## Fonctionnalités



\- \*\*Actualité\*\* : récupère des flux RSS (France, monde, Cameroun, technologie)

&#x20; et les résume en français.

\- \*\*Idée de business\*\* : propose une idée de business passif en ligne,

&#x20; avec mémoire des idées précédentes, et l'approfondit un jour par semaine.

\- \*\*Vidéo du jour\*\* : choisit une vidéo récente de chaînes YouTube

&#x20; sur la data science et l'IA, sans jamais reproposer la même.

\- \*\*Assemblage\*\* : génère un briefing daté, enregistré dans `briefings/`.



\## Architecture



| Fichier | Rôle |

|---|---|

| `news.py` | Flux RSS + synthèse de l'actualité |

| `ideas.py` | Idées de business avec historique JSON |

| `videos.py` | Suggestion de vidéo avec historique JSON |

| `main.py` | Orchestration, tolérance aux pannes, sauvegarde |



Chaque module est indépendant : si l'un échoue, les autres continuent.



\## Installation



```

pip install -r requirements.txt

```



Définir la clé d'API Anthropic dans une variable d'environnement

(PowerShell) :



```

$env:ANTHROPIC\_API\_KEY="votre-clé"

```



\## Utilisation



```

python main.py

```



\## Feuille de route



\- \[ ] Envoi du briefing par e-mail

\- \[ ] Planification quotidienne automatique

\- \[ ] Résumé des e-mails Gmail

\- \[ ] Suivi des objectifs de la journée

\- \[ ] Interface web (Streamlit)



\## Sécurité



Aucune clé n'est stockée dans le code : elles sont lues depuis des

variables d'environnement. Les historiques et briefings personnels

sont exclus du dépôt par `.gitignore`.

