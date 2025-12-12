"""Configuration pytest pour les tests du skill."""

import sys
from pathlib import Path

# Ajouter le répertoire racine au path pour les imports
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))
