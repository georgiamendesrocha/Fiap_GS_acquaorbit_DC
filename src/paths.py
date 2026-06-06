"""
Caminhos centralizados do projeto Acqua Orbit DC.

Raiz do repositório (template FIAP):
    .github, assets, config, document, scripts, src, menu.py, README.md

Dentro de src/ ficam código, dados, modelos e saídas geradas.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
DATA = SRC / "data"
MODELS = SRC / "models"
OUTPUT = SRC / "output"
DOCUMENT = ROOT / "document"
SCRIPTS_DB = ROOT / "scripts" / "database"
ASSETS = ROOT / "assets"
