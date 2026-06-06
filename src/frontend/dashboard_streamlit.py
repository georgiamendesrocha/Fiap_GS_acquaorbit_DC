"""
Acqua Orbit DC - Dashboard Streamlit.

Duas visualizacoes no mesmo app:
- Dashboard POC (HTML): conteudo da etapa 06 (Georgia)
- Analise interativa: ranking IA, indicadores, clima, sensores e mapa

Uso:
    streamlit run src/frontend/dashboard_streamlit.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC))
sys.path.insert(0, str(_SRC if (_SRC / "paths.py").exists() else _SRC.parent))

import streamlit as st

from dashboard_streamlit_interativo import renderizar_dashboard_interativo  # noqa: E402
from dashboard_streamlit_poc import (  # noqa: E402
    configurar_pagina,
    obter_resultados,
    renderizar_dashboard_poc_html,
)


def main() -> None:
    configurar_pagina()

    try:
        df = obter_resultados()
    except (FileNotFoundError, ValueError) as erro:
        st.error(str(erro))
        st.stop()

    modo = st.radio(
        "Visualizacao",
        ["Dashboard POC (HTML)", "Analise interativa (IA)"],
        horizontal=True,
        help="POC estatica da etapa 06 ou painel completo com modelo de IA.",
    )
    st.markdown("---")

    if modo == "Dashboard POC (HTML)":
        renderizar_dashboard_poc_html(df)
    else:
        renderizar_dashboard_interativo()


if __name__ == "__main__":
    main()
