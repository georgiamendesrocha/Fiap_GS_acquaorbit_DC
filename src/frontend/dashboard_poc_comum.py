"""
Componentes compartilhados entre dashboard HTML e Streamlit.
Espelha a entrega da Georgia Mendes Rocha (etapa 06).
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC if (_SRC / "paths.py").exists() else _SRC.parent))

from gerar_dashboard_html import (  # noqa: E402
    ARQUIVO_RESULTADOS,
    CORES_REGIOES,
    carregar_resultados,
    classe_status,
)

GRAFICOS_POC = [
    ("score_final_poc_0_10", "Score final da POC", "Quanto maior, melhor a condicao comparativa", False),
    (
        "indice_esg_resiliencia_score_0_10",
        "Indice ESG e resiliencia",
        "Combinacao de ambiente, reuso, agua e infraestrutura",
        False,
    ),
    (
        "risco_ambiental_climatico_score_0_10",
        "Risco ambiental e climatico",
        "Quanto maior, maior a cautela ambiental",
        False,
    ),
    (
        "indice_conectividade_critica_score_0_10",
        "Conectividade critica",
        "Robustez parametrizada da infraestrutura digital",
        False,
    ),
    (
        "indice_disponibilidade_energetica_score_0_10",
        "Disponibilidade energetica",
        "Condicao parametrizada de energia e resiliencia",
        False,
    ),
    (
        "cobertura_reuso_pluvial_pct",
        "Cobertura estimada de reuso pluvial",
        "Potencial anual frente ao consumo tecnico simulado",
        True,
    ),
]

STATUS_CORES = {
    "status-good": "#6a8d22",
    "status-warn": "#c98a12",
    "status-risk": "#b23a48",
    "status-critical": "#7f1d1d",
}
