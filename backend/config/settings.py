from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

DATABASE_PATH = BASE_DIR / "data" / "sqlite" / "research.db"
GRAPH_PATH = BASE_DIR / "data" / "graph" / "research_graph.gexf"

OPENALEX_EMAIL = os.getenv("OPENALEX_EMAIL", "")