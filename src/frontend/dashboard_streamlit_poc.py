"""
Dashboard Streamlit — versao POC (conteudo do HTML da etapa 06).

Replica o dashboard estatico gerado por gerar_dashboard_html.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC if (_SRC / "paths.py").exists() else _SRC.parent))
from paths import OUTPUT, ROOT  # noqa: E402

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from dashboard_poc_comum import (  # noqa: E402
    GRAFICOS_POC,
    STATUS_CORES,
    carregar_resultados,
    classe_status,
)
from gerar_dashboard_html import ARQUIVO_DASHBOARD  # noqa: E402

CSS_POC = """
<style>
    .poc-header {
        background: #102a43;
        color: #ffffff;
        padding: 28px 24px 22px;
        border-radius: 8px;
        margin-bottom: 18px;
    }
    .poc-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 800;
    }
    .poc-header p {
        margin: 10px 0 0;
        color: #d9e7f2;
        max-width: 860px;
    }
    .region-card {
        border: 1px solid #d8e0e6;
        border-radius: 8px;
        padding: 18px;
        background: #ffffff;
        min-height: 220px;
    }
    .rank-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        border-radius: 50%;
        color: #ffffff;
        background: #305f72;
        font-weight: 700;
    }
    .status-badge {
        display: inline-block;
        border-radius: 999px;
        padding: 4px 12px;
        color: #fff;
        font-size: 0.82rem;
        font-weight: 700;
    }
    .score-big {
        font-size: 2rem;
        font-weight: 800;
        line-height: 1;
        margin: 10px 0 4px;
    }
    .footnote {
        color: #5c6873;
        font-size: 0.9rem;
        margin-top: 24px;
    }
</style>
"""


def configurar_pagina() -> None:
    st.set_page_config(
        page_title="Acqua Orbit DC - Dashboard POC",
        page_icon="🛰️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(CSS_POC, unsafe_allow_html=True)


@st.cache_data
def obter_resultados() -> pd.DataFrame:
    return carregar_resultados()


def _cor_regiao(regiao_id: str) -> str:
    from dashboard_poc_comum import CORES_REGIOES

    return CORES_REGIOES.get(str(regiao_id), "#305f72")


def renderizar_cabecalho_poc() -> None:
    st.markdown(
        """
        <div class="poc-header">
            <h1>Acqua Orbit DC</h1>
            <p>Dashboard da POC com classificacao ESG, risco ambiental, reuso pluvial,
            sensores simulados e infraestrutura critica digital para regioes candidatas a data centers.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def renderizar_resumo(df: pd.DataFrame) -> None:
    melhor = df.iloc[0]
    favoraveis = int((df["classificacao_final"] == "favorável").sum())
    atencao = int((df["classificacao_final"] == "atenção").sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Regioes oficiais avaliadas", len(df))
    c2.metric("Melhor classificacao", f"{melhor['cidade']}/{melhor['estado']}")
    c3.metric("Classificacao favoravel", favoraveis)
    c4.metric("Regioes em atencao", atencao)


def renderizar_card_regiao(posicao: int, row: pd.Series) -> None:
    status_cls = classe_status(str(row["classificacao_final"]))
    status_cor = STATUS_CORES.get(status_cls, "#305f72")
    accent = _cor_regiao(row["regiao_id"])

    st.markdown(
        f"""
        <div class="region-card">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span class="rank-number">{posicao}</span>
                <span class="status-badge" style="background:{status_cor}">
                    {row['classificacao_final']}
                </span>
            </div>
            <h3 style="margin:12px 0 4px;color:{accent}">{row['regiao']}</h3>
            <p style="color:#5c6873;margin:0 0 8px">{row['cidade']}/{row['estado']}</p>
            <div class="score-big" style="color:{accent}">{row['score_final_poc_0_10']:.2f}</div>
            <small style="color:#5c6873">score final</small>
            <p style="margin-top:12px;font-size:0.95rem">{row['parecer_apoio_decisao']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def renderizar_ranking_cards(df: pd.DataFrame) -> None:
    st.markdown("## Ranking Final")
    cols = st.columns(3)
    for idx in range(min(3, len(df))):
        with cols[idx]:
            renderizar_card_regiao(idx + 1, df.iloc[idx])


def grafico_barras_horizontal(
    df: pd.DataFrame,
    coluna: str,
    titulo: str,
    subtitulo: str,
    percentual: bool = False,
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7.2, 2.6))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    labels = [f"{r['cidade']}/{r['estado']}" for _, r in df.iterrows()]
    valores = df[coluna].astype(float).tolist()
    cores = [_cor_regiao(r["regiao_id"]) for _, r in df.iterrows()]
    ymax = max(valores) if percentual else 10.0
    if percentual:
        ymax = max(max(valores), 1)

    y_pos = list(range(len(labels)))
    ax.barh(y_pos, [ymax] * len(labels), color="#e8eef2", height=0.55, zorder=1)
    ax.barh(y_pos, valores, color=cores, height=0.55, zorder=2)

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(labels, fontsize=10, fontweight="bold")
    ax.set_xlim(0, ymax * 1.12)
    ax.invert_yaxis()
    ax.set_title(titulo, loc="left", fontsize=13, fontweight="bold", pad=14)
    ax.text(0, 1.02, subtitulo, transform=ax.transAxes, fontsize=9, color="#5c6873")
    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
    ax.tick_params(axis="x", colors="#5c6873")
    ax.set_xticks([])

    for i, valor in enumerate(valores):
        texto = f"{valor:.1f}%" if percentual else f"{valor:.2f}"
        ax.text(valor + ymax * 0.02, i, texto, va="center", fontsize=10, fontweight="bold")

    fig.tight_layout()
    return fig


def renderizar_graficos(df: pd.DataFrame) -> None:
    for i in range(0, len(GRAFICOS_POC), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j >= len(GRAFICOS_POC):
                break
            coluna, titulo, subtitulo, percentual = GRAFICOS_POC[i + j]
            fig = grafico_barras_horizontal(df, coluna, titulo, subtitulo, percentual)
            with col:
                st.pyplot(fig, clear_figure=True)
            plt.close(fig)


def renderizar_mapa(df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    fig.patch.set_facecolor("#ffffff")

    lat_min, lat_max = df["latitude"].min(), df["latitude"].max()
    lon_min, lon_max = df["longitude"].min(), df["longitude"].max()
    lat_pad = (lat_max - lat_min) * 0.15 or 0.5
    lon_pad = (lon_max - lon_min) * 0.15 or 0.5

    ax.set_facecolor("#eef4f7")
    ax.set_xlim(lon_min - lon_pad, lon_max + lon_pad)
    ax.set_ylim(lat_min - lat_pad, lat_max + lat_pad)

    for passo in range(1, 4):
        ax.axvline(
            lon_min + ((lon_max - lon_min) / 4) * passo,
            color="#d3dde4",
            linewidth=0.8,
        )
        ax.axhline(
            lat_min + ((lat_max - lat_min) / 4) * passo,
            color="#d3dde4",
            linewidth=0.8,
        )

    for _, row in df.iterrows():
        cor = _cor_regiao(row["regiao_id"])
        ax.scatter(row["longitude"], row["latitude"], s=180, color=cor, alpha=0.2, zorder=2)
        ax.scatter(row["longitude"], row["latitude"], s=70, color=cor, zorder=3)
        ax.annotate(
            f"{row['cidade']}/{row['estado']}\nscore {row['score_final_poc_0_10']:.2f}",
            (row["longitude"], row["latitude"]),
            textcoords="offset points",
            xytext=(12, 6),
            fontsize=9,
            fontweight="bold",
        )

    ax.set_title(
        "Mapa simplificado por coordenadas",
        loc="left",
        fontsize=13,
        fontweight="bold",
        pad=12,
    )
    ax.text(
        0,
        1.02,
        "Posicionamento relativo das regioes oficiais da POC",
        transform=ax.transAxes,
        fontsize=9,
        color="#5c6873",
    )
    ax.set_xlabel(f"Longitude {lon_min:.2f} a {lon_max:.2f}", fontsize=9, color="#5c6873")
    ax.set_ylabel(f"Latitude {lat_min:.2f} a {lat_max:.2f}", fontsize=9, color="#5c6873")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


def renderizar_sensores(df: pd.DataFrame) -> None:
    st.markdown("#### Sensores simulados de agua")
    tabela = df[
        [
            "cidade",
            "estado",
            "classificacao_qualidade_agua",
            "nivel_reservatorio_pct",
            "ph_agua",
            "turbidez_ntu",
            "indice_qualidade_agua_score_0_10",
        ]
    ].copy()
    tabela.columns = [
        "Cidade",
        "UF",
        "Qualidade",
        "Nivel (%)",
        "pH",
        "Turbidez",
        "Score",
    ]
    tabela["Regiao"] = tabela["Cidade"] + "/" + tabela["UF"]
    tabela = tabela[
        ["Regiao", "Qualidade", "Nivel (%)", "pH", "Turbidez", "Score"]
    ]
    st.dataframe(tabela, width="stretch", hide_index=True)


def renderizar_mapa_e_sensores(df: pd.DataFrame) -> None:
    col_mapa, col_sensores = st.columns(2)
    with col_mapa:
        fig = renderizar_mapa(df)
        st.pyplot(fig, clear_figure=True)
        plt.close(fig)
    with col_sensores:
        renderizar_sensores(df)


def renderizar_rodape() -> None:
    st.markdown(
        """
        <p class="footnote">
        POC academica. Os resultados sao apoio simulado a decisao e nao substituem laudos tecnicos,
        auditorias ESG ou estudos profissionais de data center, energia, telecomunicacoes e meio ambiente.
        </p>
        """,
        unsafe_allow_html=True,
    )


def renderizar_dashboard_poc_html(df: pd.DataFrame) -> None:
    """Versao equivalente ao dashboard HTML da etapa 06."""
    renderizar_cabecalho_poc()
    renderizar_resumo(df)
    renderizar_ranking_cards(df)
    renderizar_graficos(df)
    renderizar_mapa_e_sensores(df)
    renderizar_rodape()

    if ARQUIVO_DASHBOARD.exists():
        st.markdown("---")
        st.markdown(f"**Versao HTML estatica:** `{ARQUIVO_DASHBOARD.relative_to(ROOT)}`")
        with open(ARQUIVO_DASHBOARD, encoding="utf-8") as html:
            st.download_button(
                "Baixar dashboard HTML",
                html.read(),
                file_name="dashboard_poc.html",
                mime="text/html",
            )
