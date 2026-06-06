"""
Acqua Orbit DC - Etapa 10
Treina e salva o modelo de IA para predicao do score final das regioes.

Entrada:
    data/resultados_regioes.csv

Saidas:
    models/score_regiao_model.joblib
    models/score_regiao_metadata.json

Uso:
    python ml/treinar_modelo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC if (_SRC / "paths.py").exists() else _SRC.parent))
from paths import DATA, DOCUMENT, MODELS, OUTPUT, ROOT, SCRIPTS_DB, SRC, ASSETS  # noqa: E402

from pathlib import Path
import sys


from ml.modelo_score_regiao import ARQUIVO_METADADOS, treinar_e_salvar  # noqa: E402


def main() -> None:
    print("Acqua Orbit DC - Treinamento do modelo de IA")
    print("-" * 48)
    caminho = treinar_e_salvar()
    print(f"Modelo salvo em: {caminho}")
    print(f"Metadados: {ARQUIVO_METADADOS}")
    print("Treinamento concluido com sucesso.")


if __name__ == "__main__":
    main()
