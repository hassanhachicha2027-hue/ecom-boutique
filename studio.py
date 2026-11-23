"""Point d'entrée pour LangGraph Studio : uv run langgraph dev --no-reload --allow-blocking"""
from agent_boutique_state import construire_graphe
from outils_base import creer_base

creer_base()
agent = construire_graphe()  # sans checkpointer : le serveur gère lui-même la persistance
