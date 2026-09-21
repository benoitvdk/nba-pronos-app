# NBA Playoffs Pronos App

App de pronostics sur les résultats des playoffs NBA (façon Mon Petit
Pronostic), en Python, 100% gratuit à héberger. Voir `Spec App Pronostics
Playoffs NBA.md` pour la spec complète.

## Stack

- Backend : Flask, déployé sur Render (free tier)
- Base de données : Neon (Postgres gratuit)
- ORM : Flask-SQLAlchemy

## Démarrage local

```bash
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# éditer .env : renseigner DATABASE_URL (Neon) et SECRET_KEY

python -m scripts.init_db   # crée les tables + seed scoring_config
python -m scripts.add_player "Prénom Nom"   # crée un joueur + son lien de connexion
python wsgi.py              # lance le serveur de dev sur http://127.0.0.1:5000
```

Pour lancer les tests (logique de scoring, indépendante de la base) :

```bash
pip install -r requirements-dev.txt
pytest
```

Pour recalculer les points une fois des résultats de matchs en base :

```bash
python -m scripts.run_scoring --engine classic      # ou --engine odds_based
python -m scripts.score_bracket --category nba_champion --winner "Boston Celtics"
```

## Ingestion automatique (résultats + cotes)

L'ingestion (`scripts/ingest.py`) ne fait que mettre à jour des matchs pour des
séries qui existent déjà : **il faut d'abord créer chaque `Series` à la main**
(season, round, team_a, team_b - et si tu veux le moteur basé sur les cotes,
`winner_odds`/`score_odds`) via le SQL Editor de Neon, par exemple :

```sql
INSERT INTO series (season, round, team_a, team_b)
VALUES (2025, 'finals', 'New York Knicks', 'San Antonio Spurs');
```

Les noms d'équipe doivent être écrits pareil que dans balldontlie/theoddsapi
(nom complet, ex. "Boston Celtics", pas "BOS"). `season` suit la convention
balldontlie : année de **début** de saison (ex. 2025 pour la finale NBA 2026,
jouée en juin 2026 à la fin de la saison 2025-26) - toujours la renseigner,
c'est ce qui évite toute confusion si les deux mêmes équipes se recroisent
une autre année.

Si ta base a été créée avant ces ajouts, lance d'abord dans le SQL Editor de
Neon `sql/002_add_external_id_to_games.sql` puis `sql/003_add_season_to_series.sql`
(une base neuve via `init_db.py` a déjà les deux colonnes).

Il faut aussi une clé API gratuite balldontlie.io (Sign Up sur balldontlie.io,
palier Free, 5 req/min) à ajouter dans `.env` (`BALLDONTLIE_API_KEY`).

```bash
python -m scripts.ingest --season 2025   # test : finale 2026 (Knicks-Spurs, déjà jouée)
python -m scripts.ingest --season 2026   # vrais playoffs 2027, une fois commencés
```

Un workflow GitHub Actions (`.github/workflows/ingest.yml`) est prêt pour
lancer ça automatiquement toutes les heures, gratuitement, sur un repo public -
il faut juste ajouter `DATABASE_URL`, `BALLDONTLIE_API_KEY` et `ODDS_API_KEY`
dans les secrets du repo GitHub (Settings > Secrets and variables > Actions),
et mettre à jour `--season` dedans le moment venu.

Limite connue : theoddsapi.com ne donne les cotes que pour les matchs à venir/en
direct (pas d'historique sur le palier gratuit), donc la partie cotes ne sera
réellement testable qu'une fois les playoffs 2026 commencés.

`/health` répond `{"status": "ok"}` une fois le serveur lancé. Le lien affiché par
`add_player` (ex. `http://127.0.0.1:5000/login/<code>`) connecte directement, sans
mot de passe.

## Déploiement sur Render

Déploiement via Blueprint (`render.yaml` à la racine) : sur render.com, *New +*
→ *Blueprint* → connecter le repo GitHub → Render détecte `render.yaml` et
propose le service `nba-playoffs-pronos`. `SECRET_KEY` est généré
automatiquement ; `DATABASE_URL`, `ODDS_API_KEY` et `BALLDONTLIE_API_KEY`
sont à renseigner manuellement dans le dashboard Render (mêmes valeurs que
dans `.env` local).

Le plan gratuit Render met le service en veille après 15 minutes d'inactivité
(premier chargement suivant : 30 à 60 secondes de réveil). Pour que le cron
d'ingestion GitHub Actions fonctionne, ajouter les mêmes 3 secrets
(`DATABASE_URL`, `BALLDONTLIE_API_KEY`, `ODDS_API_KEY`) dans les secrets
Actions du repo GitHub (pas les variables).

## Utilisation (frontend)

Une fois connecté via son lien, chaque joueur arrive sur `/` (tableau de bord) :

- pour chaque série : pronostic vainqueur de série + score exact (équipe +
  score combinés, ex. "Celtics gagnent 4-2"), et pour chaque match à venir un
  pronostic vainqueur du match. Tout redevient modifiable jusqu'au coup
  d'envoi (match) ou jusqu'au premier match joué de la série (vainqueur/score
  de série), puis se fige.
- `/classement` : classement de tous les joueurs (pronostics + bracket
  confondus), y compris ceux à 0 point.
- `/bracket/` : pronostics "avant playoffs" (champion NBA, MVP des finales,
  champion Est/Ouest) - texte libre, verrouillé dès qu'un premier match de
  playoffs a été joué.

L'app est une PWA installable (manifest + service worker, icônes générées) :
sur mobile ou desktop, le navigateur propose "Installer l'application" /
"Ajouter à l'écran d'accueil". Une page hors-ligne s'affiche si le joueur
perd sa connexion. Le service worker est servi depuis `/sw.js` (et non
`/static/sw.js`) exprès, pour que son scope couvre toute l'app et pas
seulement `/static/`.

## Structure

```
app/
  __init__.py      application factory Flask
  config.py        config lue depuis les variables d'environnement
  extensions.py     instance SQLAlchemy partagée
  models.py        tables : players, series, games, predictions,
                    scoring_config, bracket_predictions
  auth.py          connexion par lien/code d'accès (pas de mot de passe)
  home.py          tableau de bord : pronostics ouverts + déjà soumis
  predictions.py   soumission des pronostics (match, vainqueur/score série)
  leaderboard.py   classement de tous les joueurs
  bracket.py       pronostics "avant playoffs" (champion, MVP, etc.)
  time_utils.py    normalisation des datetimes (SQLite vs Postgres)
  templates/       login.html, home.html, base.html, leaderboard.html,
                    bracket.html
  static/          manifest.json, sw.js, offline.html, icons/ (PWA)
  scoring.py       logique pure des 2 moteurs de scoring (testable seule)
  scoring_service.py  branche scoring.py aux données réelles (DB)
  ingestion.py     transforme les réponses API en Game à jour (testable seul)
  clients/         clients HTTP balldontlie.py et odds_api.py
scripts/
  init_db.py       crée les tables + seed scoring_config
  add_player.py    ajoute un joueur et génère son lien de connexion
  run_scoring.py   recalcule les points des pronostics match/série
  score_bracket.py note une catégorie du bracket une fois le résultat connu
  ingest.py        récupère résultats + cotes et met à jour la base
sql/
  schema.sql, seed_scoring_config.sql, 002_add_external_id_to_games.sql,
  003_add_season_to_series.sql
tests/
  test_scoring.py    tests unitaires des 2 moteurs de scoring
  test_ingestion.py  tests de l'ingestion (API mockées, pas d'appel réseau)
  test_web.py        tests des routes web (pronostics, classement, bracket)
.github/workflows/
  ingest.yml       cron GitHub Actions (gratuit) pour l'ingestion automatique
render.yaml        Blueprint Render (service web + variables d'environnement)
wsgi.py            point d'entrée pour gunicorn / Render
```

## État d'avancement

- [x] Modèle de données
- [x] Authentification simple par lien/code joueur
- [x] Moteurs de scoring (classique + basé sur les cotes)
- [x] Script d'ingestion automatique (résultats + cotes)
- [x] Frontend PWA (pronostics, classement, bracket, installable hors-ligne)
- [x] Déploiement sur Render
- [ ] Nettoyage des séries de test avant la vraie saison 2026-27
