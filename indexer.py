"""Indexation des règles de la boutique dans ChromaDB (à lancer une fois avant l'agent).

    uv run indexer.py
"""
import os

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()  # charge GOOGLE_API_KEY depuis le fichier .env

DOSSIER = os.path.dirname(os.path.abspath(__file__))
FICHIER_PDF = os.getenv("FICHIER_PDF", "politique_boutique.pdf")
EMBEDDINGS = os.getenv("EMBEDDINGS", "gemini-embedding-001")
CHROMA_DIR = os.getenv("CHROMA_DIR", os.path.join(DOSSIER, "chroma_db"))
COLLECTION = os.getenv("COLLECTION", "politique_boutique")


def connecter_chroma():
    """Se connecte à la base vectorielle Chroma (sans indexer : utilisée aussi par l'agent)."""
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDINGS)
    return Chroma(
        collection_name=COLLECTION,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )


def indexer_politique(db):
    """Charge le PDF, le découpe et (ré)indexe tous les chunks dans la collection Chroma."""
    # 1. CHARGEMENT DU PDF (chemin relatif à ce fichier : marche quel que soit le dossier courant)
    chemin = FICHIER_PDF if os.path.isabs(FICHIER_PDF) else os.path.join(DOSSIER, FICHIER_PDF)
    docs = PyPDFLoader(chemin).load()
    print("Pages chargées :", len(docs))

    # 2. DÉCOUPAGE (CHUNKING)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    print("Chunks :", len(chunks))

    # 3 + 4. EMBEDDINGS GEMINI + STOCKAGE CHROMADB
    db.reset_collection()  # vide la collection : relancer le script ne crée pas de doublons
    db.add_documents(chunks)
    print(f"Index ChromaDB créé : {len(chunks)} chunks dans '{COLLECTION}' ({CHROMA_DIR})")
    return len(chunks)


def index_vide(db) -> bool:
    """Vrai si la collection ne contient aucun chunk (ex. premier démarrage sur Streamlit Cloud)."""
    return len(db.get(limit=1)["ids"]) == 0


# Ce bloc ne s'exécute qu'avec « uv run indexer.py », pas quand l'agent importe connecter_chroma
if __name__ == "__main__":
    db = connecter_chroma()
    indexer_politique(db)

    # 5. TEST RAPIDE DU RETRIEVER
    question = "Puis-je retourner un produit après 20 jours ?"
    print(f"\nTest : {question}")
    for doc in db.similarity_search(question, k=2):
        print("  •", doc.page_content.replace("\n", " ")[:120], "...")

    # 5. TEST RAPIDE DU RETRIEVER
    question = "Puis-je retourner un produit après 20 jours ?"
    print(f"\nTest : {question}")
    for doc in db.similarity_search(question, k=2):
        print("  •", doc.page_content.replace("\n", " ")[:120], "...")
