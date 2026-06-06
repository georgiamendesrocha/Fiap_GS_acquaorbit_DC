"""Camada de banco de dados Oracle da POC."""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC if (_SRC / "paths.py").exists() else _SRC.parent))
from paths import DATA, DOCUMENT, MODELS, OUTPUT, ROOT, SCRIPTS_DB, SRC, ASSETS  # noqa: E402

from db.db import (
    conectar,
    consultar_ranking,
    criar_tabelas,
    garantir_estrutura,
    inicializar_credenciais,
    oracle_disponivel,
)

__all__ = [
    "conectar",
    "consultar_ranking",
    "criar_tabelas",
    "garantir_estrutura",
    "inicializar_credenciais",
    "oracle_disponivel",
]
