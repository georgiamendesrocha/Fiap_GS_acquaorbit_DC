"""
Gera imagens estaticas (prints) das saidas do pipeline e do dashboard Streamlit
para inclusao no PDF de documentacao.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC if (_SRC / "paths.py").exists() else _SRC.parent))
from paths import DATA, DOCUMENT, MODELS, OUTPUT, ROOT, SCRIPTS_DB, SRC, ASSETS  # noqa: E402

import sys
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec


CAPTURAS_DIR = OUTPUT / "pdf_capturas"
ARQUIVO_RESULTADOS = DATA / "resultados_regioes.csv"
ARQUIVO_MODELO = MODELS / "score_regiao_model.joblib"

CORES = {
    "SP_BARUERI_TAMBORE": "#0f8b8d",
    "PR_CURITIBA": "#6a8d22",
    "RJ_BARRA_JACAREPAGUA_PARQUE_OLIMPICO": "#d95d39",
}

MEDALHAS = ["1", "2", "3"]


def _cor_regiao(regiao_id: str) -> str:
    return CORES.get(str(regiao_id), "#305f72")


def _nome_curto(regiao: str) -> str:
    return regiao.replace("Barra/Jacarepaguá/Parque Olímpico", "Barra/Jacarepaguá")[:28]


def _salvar(fig: plt.Figure, nome: str) -> Path:
    CAPTURAS_DIR.mkdir(parents=True, exist_ok=True)
    caminho = CAPTURAS_DIR / nome
    fig.savefig(caminho, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return caminho


def carregar_resultados() -> pd.DataFrame:
    if not ARQUIVO_RESULTADOS.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {ARQUIVO_RESULTADOS}. Execute a etapa 5 do pipeline."
        )
    return pd.read_csv(ARQUIVO_RESULTADOS)


def carregar_resultados_ia() -> pd.DataFrame:
    df = carregar_resultados()
    if ARQUIVO_MODELO.exists():
        from ml.modelo_score_regiao import predizer_dataframe

        return predizer_dataframe(df)
    df = df.copy()
    df["score_ia_0_10"] = df["score_final_poc_0_10"]
    df["classificacao_ia"] = df["classificacao_final"]
    return df.sort_values("score_ia_0_10", ascending=False).reset_index(drop=True)


def captura_pipeline_terminal(df: pd.DataFrame) -> Path:
    df_ord = df.sort_values("score_final_poc_0_10", ascending=False)
    linhas = [
        "Acqua Orbit DC - Resumo do Pipeline",
        "=" * 52,
        f"Execucao documentada em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "",
        "[02] Dados climaticos NASA POWER tratados",
        "[03] regioes.csv montado com 3 regioes oficiais",
        "[04] Validacao estrutural concluida",
        "[05] Sensores simulados e scores calculados",
        "[06] dashboard_poc.html gerado",
        "[07] Persistencia Oracle/CSV executada",
        "",
        "Ranking final da POC:",
    ]
    for pos, (_, row) in enumerate(df_ord.iterrows(), start=1):
        linhas.append(
            f"  {pos}. {row['cidade']}/{row['estado']} | "
            f"score {row['score_final_poc_0_10']:.2f} | {row['classificacao_final']}"
        )

    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_facecolor("#1e1e1e")
    fig.patch.set_facecolor("#1e1e1e")
    ax.axis("off")
    ax.text(
        0.03,
        0.97,
        "\n".join(linhas),
        va="top",
        ha="left",
        fontsize=11,
        family="monospace",
        color="#d7f9ff",
    )
    ax.set_title(
        "Print - Saida consolidada do pipeline",
        color="#0f8b8d",
        fontsize=14,
        fontweight="bold",
        pad=14,
    )
    return _salvar(fig, "pipeline_terminal_resumo.png")


def captura_pipeline_ranking(df: pd.DataFrame) -> Path:
    df_ord = df.sort_values("score_final_poc_0_10", ascending=True)
    cores = [_cor_regiao(r) for r in df_ord["regiao_id"]]
    nomes = [_nome_curto(r) for r in df_ord["regiao"]]

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.barh(nomes, df_ord["score_final_poc_0_10"], color=cores, height=0.55)
    ax.set_xlim(0, 10)
    ax.set_xlabel("Score final (regras POC)")
    ax.set_title("Print - Ranking final do pipeline (etapa 05)", fontweight="bold", color="#0f4c5c")
    ax.grid(axis="x", alpha=0.25)
    for i, valor in enumerate(df_ord["score_final_poc_0_10"]):
        ax.text(valor + 0.08, i, f"{valor:.2f}", va="center", fontsize=10, fontweight="bold")
    return _salvar(fig, "pipeline_ranking_final.png")


def captura_pipeline_sensores(df: pd.DataFrame) -> Path:
    nomes = [_nome_curto(r) for r in df["regiao"]]
    x = np.arange(len(nomes))
    largura = 0.35

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(x - largura / 2, df["ph_agua"], largura, label="pH", color="#6a8d22")
    ax.bar(x + largura / 2, df["turbidez_ntu"], largura, label="Turbidez (NTU)", color="#d95d39")
    ax.set_xticks(x)
    ax.set_xticklabels(nomes, rotation=10)
    ax.set_title("Print - Sensores de agua simulados (pipeline)", fontweight="bold", color="#0f4c5c")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    return _salvar(fig, "pipeline_sensores_agua.png")


def captura_pipeline_clima(df: pd.DataFrame) -> Path:
    nomes = [_nome_curto(r) for r in df["regiao"]]
    variaveis = [
        ("Temp. media (C)", "temperatura_media_anual_c"),
        ("Precipitacao (mm)", "precipitacao_total_anual_mm"),
        ("Umidade (%)", "umidade_media_anual_pct"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(11, 4.5))
    for ax, (titulo, coluna) in zip(axes, variaveis):
        ax.bar(nomes, df[coluna], color="#0f8b8d", alpha=0.85)
        ax.set_title(titulo, fontsize=10)
        ax.tick_params(axis="x", rotation=15)
        ax.grid(axis="y", alpha=0.2)
    fig.suptitle("Print - Clima NASA POWER por regiao (pipeline)", fontweight="bold", color="#0f4c5c")
    fig.tight_layout()
    return _salvar(fig, "pipeline_clima_regioes.png")


def captura_pipeline_indicadores(df: pd.DataFrame) -> Path:
    nomes = [_nome_curto(r) for r in df["regiao"]]
    indicadores = [
        ("ESG", "indice_esg_resiliencia_score_0_10"),
        ("Risco ambiental", "risco_ambiental_climatico_score_0_10"),
        ("Conectividade", "indice_conectividade_critica_score_0_10"),
        ("Energia", "indice_disponibilidade_energetica_score_0_10"),
    ]
    dados = {nome: [float(df.iloc[i][col]) for i in range(len(df))] for nome, col in indicadores}
    x = np.arange(len(nomes))
    largura = 0.18

    fig, ax = plt.subplots(figsize=(11, 5))
    for idx, nome_ind in enumerate(dados):
        offset = (idx - 1.5) * largura
        ax.bar(x + offset, dados[nome_ind], largura, label=nome_ind)
    ax.set_xticks(x)
    ax.set_xticklabels(nomes, rotation=10)
    ax.set_ylim(0, 10)
    ax.set_title("Print - Indicadores ESG e infraestrutura (pipeline)", fontweight="bold", color="#0f4c5c")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    return _salvar(fig, "pipeline_indicadores_esg.png")


def captura_streamlit_ranking_ia(df: pd.DataFrame) -> Path:
    fig = plt.figure(figsize=(11, 7))
    gs = GridSpec(2, 1, height_ratios=[1, 1.4], hspace=0.35)
    ax_podio = fig.add_subplot(gs[0])
    ax_rank = fig.add_subplot(gs[1])

    ax_podio.set_xlim(0, 3)
    ax_podio.set_ylim(0, 1)
    ax_podio.axis("off")
    ax_podio.set_title("Dashboard Streamlit - Podio IA", fontweight="bold", color="#0f4c5c", pad=10)

    posicoes = [0.5, 1.5, 2.5]
    alturas = [0.55, 0.75, 0.45]
    for idx in range(min(3, len(df))):
        row = df.iloc[idx]
        cor = _cor_regiao(row["regiao_id"])
        rect = mpatches.FancyBboxPatch(
            (posicoes[idx] - 0.38,
             0.08 if idx != 1 else 0.18),
            0.76,
            alturas[idx],
            boxstyle="round,pad=0.02",
            linewidth=2,
            edgecolor=cor,
            facecolor="#f4fbfc",
        )
        ax_podio.add_patch(rect)
        ax_podio.text(
            posicoes[idx],
            0.08 + alturas[idx] - 0.12,
            f"#{idx + 1}  {row['cidade']}",
            ha="center",
            fontsize=10,
            fontweight="bold",
            color=cor,
        )
        ax_podio.text(
            posicoes[idx],
            0.08 + alturas[idx] / 2,
            f"{row['score_ia_0_10']:.2f}",
            ha="center",
            fontsize=18,
            fontweight="bold",
            color=cor,
        )
        ax_podio.text(
            posicoes[idx],
            0.08 + 0.08,
            str(row["classificacao_ia"]),
            ha="center",
            fontsize=9,
            color="#555",
        )

    df_ord = df.sort_values("score_ia_0_10", ascending=True)
    nomes = [_nome_curto(r) for r in df_ord["regiao"]]
    cores = [_cor_regiao(r) for r in df_ord["regiao_id"]]
    ax_rank.barh(nomes, df_ord["score_ia_0_10"], color=cores, height=0.55)
    ax_rank.set_xlim(0, 10)
    ax_rank.set_title("Ranking por modelo de IA treinado", fontsize=11)
    ax_rank.grid(axis="x", alpha=0.25)
    for i, valor in enumerate(df_ord["score_ia_0_10"]):
        ax_rank.text(valor + 0.08, i, f"{valor:.2f}", va="center", fontweight="bold")

    fig.suptitle("Print - Dashboard Streamlit (aba Ranking IA)", fontweight="bold", color="#0f4c5c")
    return _salvar(fig, "streamlit_ranking_ia.png")


def captura_streamlit_comparativo(df: pd.DataFrame) -> Path:
    nomes = [_nome_curto(r) for r in df["regiao"]]
    x = np.arange(len(nomes))
    largura = 0.35

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(x - largura / 2, df["score_ia_0_10"], largura, label="Score IA", color="#0f8b8d")
    ax.bar(x + largura / 2, df["score_final_poc_0_10"], largura, label="Score regras POC", color="#94a3b8")
    ax.set_xticks(x)
    ax.set_xticklabels(nomes, rotation=10)
    ax.set_ylim(0, 10)
    ax.set_title(
        "Print - Dashboard Streamlit (comparativo IA x regras)",
        fontweight="bold",
        color="#0f4c5c",
    )
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    return _salvar(fig, "streamlit_comparativo_ia.png")


def captura_streamlit_indicadores(df: pd.DataFrame) -> Path:
    indicadores = [
        "indice_esg_resiliencia_score_0_10",
        "risco_ambiental_climatico_score_0_10",
        "indice_conectividade_critica_score_0_10",
        "indice_disponibilidade_energetica_score_0_10",
        "indice_qualidade_agua_score_0_10",
    ]
    rotulos = ["ESG", "Risco ambiental", "Conectividade", "Energia", "Qualidade agua"]
    matriz = df[indicadores].values
    nomes = [_nome_curto(r) for r in df["regiao"]]

    fig, ax = plt.subplots(figsize=(11, 5.5))
    im = ax.imshow(matriz, cmap="YlGnBu", aspect="auto", vmin=0, vmax=10)
    ax.set_xticks(range(len(rotulos)))
    ax.set_xticklabels(rotulos, rotation=20, ha="right")
    ax.set_yticks(range(len(nomes)))
    ax.set_yticklabels(nomes)
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            ax.text(j, i, f"{matriz[i, j]:.1f}", ha="center", va="center", color="#123", fontsize=9)
    fig.colorbar(im, ax=ax, shrink=0.85, label="Score 0-10")
    ax.set_title("Print - Dashboard Streamlit (aba Indicadores)", fontweight="bold", color="#0f4c5c")
    return _salvar(fig, "streamlit_indicadores.png")


def captura_streamlit_mapa(df: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(11, 5.5))
    scatter = ax.scatter(
        df["longitude"],
        df["latitude"],
        s=df["score_ia_0_10"] * 90,
        c=[_cor_regiao(r) for r in df["regiao_id"]],
        alpha=0.85,
        edgecolors="#123",
        linewidths=1.2,
    )
    for _, row in df.iterrows():
        ax.annotate(
            _nome_curto(row["regiao"]),
            (row["longitude"], row["latitude"]),
            textcoords="offset points",
            xytext=(6, 6),
            fontsize=9,
        )
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Print - Dashboard Streamlit (aba Mapa)", fontweight="bold", color="#0f4c5c")
    ax.grid(alpha=0.25)
    return _salvar(fig, "streamlit_mapa_regioes.png")


def captura_streamlit_sensores(df: pd.DataFrame) -> Path:
    nomes = [_nome_curto(r) for r in df["regiao"]]
    fig, axes = plt.subplots(1, 3, figsize=(11, 4.5))
    campos = [
        ("Nivel reservatorio (%)", "nivel_reservatorio_pct", "#0f8b8d"),
        ("Condutividade (uS/cm)", "condutividade_us_cm", "#6a8d22"),
        ("Temp. agua (C)", "temperatura_agua_c", "#d95d39"),
    ]
    for ax, (titulo, coluna, cor) in zip(axes, campos):
        ax.bar(nomes, df[coluna], color=cor, alpha=0.9)
        ax.set_title(titulo, fontsize=10)
        ax.tick_params(axis="x", rotation=15)
        ax.grid(axis="y", alpha=0.2)
    fig.suptitle("Print - Dashboard Streamlit (aba Sensores)", fontweight="bold", color="#0f4c5c")
    fig.tight_layout()
    return _salvar(fig, "streamlit_sensores.png")


def captura_dashboard_html_poc(df: pd.DataFrame) -> Path:
    """Evidencia visual do dashboard HTML estatico (etapa 06)."""
    df_ord = df.sort_values("score_final_poc_0_10", ascending=False)
    fig = plt.figure(figsize=(11, 6.5))
    gs = GridSpec(2, 3, height_ratios=[1, 1.1], hspace=0.45, wspace=0.35)
    ax_cards = fig.add_subplot(gs[0, :])
    ax_cards.set_xlim(0, 3)
    ax_cards.set_ylim(0, 1)
    ax_cards.axis("off")
    ax_cards.set_title(
        "Print - Dashboard HTML POC (etapa 06)",
        fontweight="bold",
        color="#102a43",
        pad=12,
    )

    for idx in range(min(3, len(df_ord))):
        row = df_ord.iloc[idx]
        cor = _cor_regiao(row["regiao_id"])
        x = idx + 0.5
        rect = mpatches.FancyBboxPatch(
            (x - 0.42, 0.08),
            0.84,
            0.78,
            boxstyle="round,pad=0.02",
            linewidth=2,
            edgecolor=cor,
            facecolor="#f8fbfc",
        )
        ax_cards.add_patch(rect)
        ax_cards.text(x, 0.72, f"#{idx + 1}", ha="center", fontsize=14, fontweight="bold", color=cor)
        ax_cards.text(
            x,
            0.58,
            _nome_curto(row["regiao"]),
            ha="center",
            fontsize=9,
            fontweight="bold",
            color="#102a43",
        )
        ax_cards.text(
            x,
            0.42,
            f"{row['score_final_poc_0_10']:.2f}",
            ha="center",
            fontsize=16,
            fontweight="bold",
            color=cor,
        )
        ax_cards.text(
            x,
            0.22,
            str(row["classificacao_final"]),
            ha="center",
            fontsize=8,
            color="#555",
        )

    indicadores = [
        ("Score final", "score_final_poc_0_10"),
        ("ESG", "indice_esg_resiliencia_score_0_10"),
        ("Risco ambiental", "risco_ambiental_climatico_score_0_10"),
    ]
    for j, (titulo, coluna) in enumerate(indicadores):
        ax = fig.add_subplot(gs[1, j])
        nomes = [_nome_curto(r) for r in df_ord["regiao"]]
        cores = [_cor_regiao(r) for r in df_ord["regiao_id"]]
        ax.barh(nomes, df_ord[coluna], color=cores, height=0.55)
        ax.set_xlim(0, 10)
        ax.set_title(titulo, fontsize=9)
        ax.invert_yaxis()
        ax.grid(axis="x", alpha=0.2)

    fig.subplots_adjust(top=0.9, bottom=0.08, left=0.06, right=0.98)
    return _salvar(fig, "dashboard_html_poc.png")


def gerar_capturas_pdf() -> list[tuple[str, Path]]:
    """Quatro capturas essenciais para o PDF (sem repetir o mesmo ranking em varios graficos)."""
    df = carregar_resultados()
    df_ia = carregar_resultados_ia()

    return [
        ("Ranking final da POC - regras etapa 05", captura_pipeline_ranking(df)),
        ("Dashboard HTML - etapa 06", captura_dashboard_html_poc(df)),
        ("Streamlit - podio e ranking IA", captura_streamlit_ranking_ia(df_ia)),
        ("Streamlit - comparativo IA x regras POC", captura_streamlit_comparativo(df_ia)),
    ]


def gerar_todas_capturas() -> dict[str, list[tuple[str, Path]]]:
    """Compatibilidade: gera conjunto completo para debug ou uso externo."""
    df = carregar_resultados()
    df_ia = carregar_resultados_ia()

    return {
        "pipeline": [
            ("Resumo do pipeline", captura_pipeline_terminal(df)),
            ("Ranking final", captura_pipeline_ranking(df)),
            ("Sensores simulados", captura_pipeline_sensores(df)),
            ("Clima NASA POWER", captura_pipeline_clima(df)),
            ("Indicadores ESG", captura_pipeline_indicadores(df)),
        ],
        "dashboard_html": [
            ("Dashboard HTML POC", captura_dashboard_html_poc(df)),
        ],
        "streamlit": [
            ("Ranking IA", captura_streamlit_ranking_ia(df_ia)),
            ("Comparativo IA", captura_streamlit_comparativo(df_ia)),
            ("Indicadores", captura_streamlit_indicadores(df_ia)),
            ("Mapa", captura_streamlit_mapa(df_ia)),
            ("Sensores", captura_streamlit_sensores(df_ia)),
        ],
    }
