# Agent de service client — LangGraph

Assistant de service client d'une boutique en ligne tunisienne :
RAG (ChromaDB + Gemini) · outils SQL (SQLite) · validation humaine (Human In The Loop).

## Fichiers

| Fichier | Rôle |
|---|---|
| `politique_boutique.pdf` | Règles de la boutique : source de connaissance du RAG |
| `indexer.py` | Charge le PDF, le découpe, calcule les embeddings et les stocke dans ChromaDB |
| `outils_base.py` | Crée la base SQLite et définit les outils SQL |
| `agent_boutique_state.py` | Outil RAG, état du graphe, nœuds et graphe LangGraph |
| `app_streamlit_state.py` | Interface web (point d'entrée) |
| `studio.py`, `langgraph.json` | Point d'entrée pour LangGraph Studio |

## Démarrage

```bash
uv sync
cp .env.example .env          # puis renseigner GOOGLE_API_KEY
uv run indexer.py             # une fois : indexe la politique dans ChromaDB
uv run agent_boutique_state.py  # optionnel : génère graphe_agent.png
uv run streamlit run app_streamlit_state.py
```

Puis ouvrir http://localhost:8501.

## LangGraph Studio / LangSmith

Renseigner les variables `LANGSMITH_*` dans `.env`, puis :

```bash
uv run langgraph dev --no-reload --allow-blocking
```

## Scénarios de test

| Question | Résultat attendu |
|---|---|
| Quels sont les délais de livraison ? | 2 à 4 jours ouvrables, gratuit dès 200 DT |
| Où en est la commande 1002 ? | Expédiée (écran 24 pouces) |
| Annule ma commande 1001 | Pause de validation ; si oui, commande annulée |
| J'ai reçu la 1003 mais la souris ne marche pas, je peux la retourner ? Si oui, fais la demande. | Pause, puis retour enregistré |
| Je veux retourner la 1004, le casque ne me plaît plus. | Refus expliqué (> 14 jours) |
