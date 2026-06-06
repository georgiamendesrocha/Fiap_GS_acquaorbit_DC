"""
Acqua Orbit DC - Consulta simples dos resultados persistidos no Oracle.

Pre-requisito:
    Arquivo .env com ORACLE_USER, ORACLE_PASSWORD e ORACLE_DSN.

Uso:
    python src/pipeline/08_consultar_resultados_oracle.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC if (_SRC / "paths.py").exists() else _SRC.parent))
from paths import DATA, DOCUMENT, MODELS, OUTPUT, ROOT, SCRIPTS_DB, SRC, ASSETS  # noqa: E402

import os
import sys
from pathlib import Path


from db.db import consultar_ranking, garantir_estrutura, inicializar_credenciais  # noqa: E402


def main() -> None:
    caminho_env = inicializar_credenciais()
    print(f"Credenciais Oracle carregadas de: {caminho_env}")
    print(f"Usuario Oracle: {os.environ['ORACLE_USER']}")
    print(garantir_estrutura())

    linhas = consultar_ranking()

    print("Ranking Oracle - Acqua Orbit DC")
    print("--------------------------------")

    if not linhas:
        print("Nenhum registro encontrado. Execute a opcao 7 para persistir os dados.")
        return

    for cidade, estado, score, classificacao in linhas:
        print(f"{cidade} / {estado} | score {score} | {classificacao}")


if __name__ == "__main__":
    main()
