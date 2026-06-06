"""
Dashboard Streamlit interativo original.

Ranking por IA, indicadores, clima NASA POWER, sensores simulados e mapa.
Requer modelo treinado em src/models/.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC if (_SRC / "paths.py").exists() else _SRC.parent))
from paths import DATA, MODELS  # noqa: E402

import pandas as pd
import streamlit as st

from ml.modelo_score_regiao import (  # noqa: E402
    ARQUIVO_MODELO,
    carregar_modelo,
    predizer_dataframe,
)

ARQUIVO_RESULTADOS = DATA / "resultados_regioes.csv"
ARQUIVO_CLIMA = DATA / "nasa_power_2025_diario_tratado.csv"

CORES_REGIOES = {
    "SP_BARUERI_TAMBORE": "#0f8b8d",
    "PR_CURITIBA": "#6a8d22",
    "RJ_BARRA_JACAREPAGUA_PARQUE_OLIMPICO": "#d95d39",
}

MEDALHAS = ["🥇", "🥈", "🥉"]

INDICADORES_SCORE = [
    ("Score IA", "score_ia_0_10"),
    ("Score regras POC", "score_final_poc_0_10"),
    ("Risco ambiental/climatico", "risco_ambiental_climatico_score_0_10"),
    ("ESG e resiliencia", "indice_esg_resiliencia_score_0_10"),
    ("Potencial reuso pluvial", "indice_potencial_reuso_pluvial_score_0_10"),
    ("Conectividade critica", "indice_conectividade_critica_score_0_10"),
    ("Disponibilidade energetica", "indice_disponibilidade_energetica_score_0_10"),
    ("Qualidade da agua", "indice_qualidade_agua_score_0_10"),
]

VARIAVEIS_CLIMA = [
    "temperatura_media_anual_c",
    "precipitacao_total_anual_mm",
    "umidade_media_anual_pct",
    "velocidade_vento_media_anual_m_s",
    "radiacao_solar_media_anual_kwh_m2_dia",
]


@st.cache_data
def carregar_resultados() -> pd.DataFrame:
    if not ARQUIVO_RESULTADOS.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {ARQUIVO_RESULTADOS}. "
            "Execute a etapa 5 do pipeline antes de abrir o dashboard."
        )
    return pd.read_csv(ARQUIVO_RESULTADOS)


@st.cache_data
def carregar_clima_diario() -> pd.DataFrame | None:
    if not ARQUIVO_CLIMA.exists():
        return None
    return pd.read_csv(ARQUIVO_CLIMA)


@st.cache_resource
def carregar_modelo_ia():
    return carregar_modelo()


@st.cache_data
def aplicar_modelo_ia(_versao_modelo: float) -> pd.DataFrame:
    df = carregar_resultados()
    return predizer_dataframe(df)


def renderizar_cabecalho(metadata: dict) -> None:
    st.title("Acqua Orbit DC")
    st.caption(
        "Global Solution 2026.1 | Ranking gerado por modelo de IA treinado "
        "com dados climaticos NASA POWER e indicadores ESG."
    )
    st.info(
        f"**Modelo ativo:** {metadata['algoritmo']} | "
        f"**Arquivo:** `{ARQUIVO_MODELO.name}` | "
        f"**MAE (regioes reais):** {metadata['mae_regioes_reais']} | "
        f"**Treinado em:** {metadata['treinado_em']}"
    )


def renderizar_sidebar(metadata: dict) -> str | None:
    st.sidebar.header("Painel")
    st.sidebar.markdown("**Motor de decisao**")
    st.sidebar.success("Modelo de IA carregado")
    st.sidebar.caption(metadata["observacao"])

    df_ranking = aplicar_modelo_ia(ARQUIVO_MODELO.stat().st_mtime)
    destaque = st.sidebar.selectbox(
        "Destacar regiao no ranking",
        ["Nenhuma"] + df_ranking["regiao"].tolist(),
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Fonte climatica**")
    st.sidebar.markdown("[NASA POWER](https://power.larc.nasa.gov/)")
    st.sidebar.markdown("**Periodo:** 2025")
    st.sidebar.markdown("**Sensores:** simulados (POC)")

    if st.sidebar.button("Atualizar dados e modelo"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()

    return None if destaque == "Nenhuma" else destaque


def renderizar_kpis(df: pd.DataFrame) -> None:
    lider = df.iloc[0]
    cols = st.columns(5)
    cols[0].metric("Regioes", len(df))
    cols[1].metric("1o lugar", lider["cidade"])
    cols[2].metric("Score IA", f"{lider['score_ia_0_10']:.2f}")
    cols[3].metric("Classificacao IA", lider["classificacao_ia"])
    cols[4].metric(
        "Delta vs regras",
        f"{lider['score_ia_0_10'] - lider['score_final_poc_0_10']:+.2f}",
    )


def renderizar_podio(df: pd.DataFrame) -> None:
    st.markdown("### Podio IA")
    cols = st.columns(3)
    for idx in range(min(3, len(df))):
        linha = df.iloc[idx]
        cor = CORES_REGIOES.get(str(linha["regiao_id"]), "#305f72")
        with cols[idx]:
            st.markdown(
                f"""
                <div style="
                    border:2px solid {cor};
                    border-radius:14px;
                    padding:16px;
                    text-align:center;
                    background:#f8fbfc;
                ">
                    <div style="font-size:2rem">{MEDALHAS[idx]}</div>
                    <div style="font-weight:700;color:{cor};font-size:1.05rem">
                        {linha['regiao']}
                    </div>
                    <div style="font-size:1.8rem;font-weight:700;margin:8px 0">
                        {linha['score_ia_0_10']:.2f}
                    </div>
                    <div style="color:#555">{linha['classificacao_ia']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def renderizar_ranking(df: pd.DataFrame, destaque: str | None) -> None:
    st.subheader("Ranking final — Modelo de IA")

    df_rank = df.copy()
    df_rank.insert(0, "Posicao", range(1, len(df_rank) + 1))

    for _, linha in df_rank.iterrows():
        cor_barra = CORES_REGIOES.get(str(linha["regiao_id"]), "#0f8b8d")
        destaque_css = (
            "border:2px solid #0f8b8d;background:#eef9fa;"
            if destaque and linha["regiao"] == destaque
            else "border:1px solid #e5e7eb;background:#ffffff;"
        )
        progresso = float(linha["score_ia_0_10"]) / 10.0
        st.markdown(
            f"""
            <div style="{destaque_css} border-radius:12px; padding:12px 14px; margin-bottom:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-weight:700; font-size:1.1rem;">
                            #{int(linha['Posicao'])} {linha['regiao']}
                        </span>
                        <span style="color:#666; margin-left:8px;">({linha['estado']})</span>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-weight:700; color:{cor_barra}; font-size:1.2rem;">
                            {linha['score_ia_0_10']:.2f}
                        </div>
                        <div style="color:#666; font-size:0.85rem;">{linha['classificacao_ia']}</div>
                    </div>
                </div>
                <div style="margin-top:8px; background:#edf2f7; border-radius:999px; height:10px;">
                    <div style="
                        width:{progresso * 100:.1f}%;
                        background:{cor_barra};
                        height:10px;
                        border-radius:999px;
                    "></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    tabela = df_rank[
        [
            "Posicao",
            "regiao",
            "estado",
            "score_ia_0_10",
            "classificacao_ia",
            "score_final_poc_0_10",
            "classificacao_final",
            "indice_esg_resiliencia_score_0_10",
            "risco_ambiental_climatico_score_0_10",
        ]
    ].copy()
    tabela.columns = [
        "#",
        "Regiao",
        "UF",
        "Score IA",
        "Class. IA",
        "Score regras",
        "Class. regras",
        "ESG",
        "Risco ambiental",
    ]
    st.dataframe(tabela, width="stretch", hide_index=True)

    comparativo = df_rank.set_index("regiao")[["score_ia_0_10", "score_final_poc_0_10"]]
    comparativo.columns = ["Score IA", "Score regras POC"]
    st.markdown("#### Comparativo IA x regras deterministicas")
    st.bar_chart(comparativo, height=280)


def renderizar_indicadores(df: pd.DataFrame, destaque: str | None) -> None:
    st.subheader("Comparativo de indicadores")

    dados = []
    for rotulo, coluna in INDICADORES_SCORE:
        for _, linha in df.iterrows():
            dados.append(
                {
                    "Indicador": rotulo,
                    "Regiao": linha["regiao"],
                    "Valor": float(linha[coluna]),
                }
            )
    pivot = pd.DataFrame(dados).pivot(index="Indicador", columns="Regiao", values="Valor")
    st.bar_chart(pivot, height=360)

    regiao_sel = destaque or st.selectbox(
        "Detalhar regiao",
        df["regiao"].tolist(),
        key="detalhe_regiao",
    )
    linha = df[df["regiao"] == regiao_sel].iloc[0]
    cols = st.columns(4)
    for idx, (rotulo, coluna) in enumerate(INDICADORES_SCORE):
        cols[idx % 4].metric(rotulo, f"{linha[coluna]:.2f}")


def renderizar_clima(df: pd.DataFrame, clima_diario: pd.DataFrame | None) -> None:
    st.subheader("Dados climaticos e ambientais")
    cols = st.columns(3)
    for idx, coluna in enumerate(VARIAVEIS_CLIMA):
        nome = coluna.replace("_", " ").replace(" anual", "").title()
        grafico = df.set_index("regiao")[[coluna]].rename(columns={coluna: nome})
        with cols[idx % 3]:
            st.markdown(f"**{nome}**")
            st.bar_chart(grafico, height=200)

    if clima_diario is not None and "regiao" in clima_diario.columns:
        st.markdown("#### Serie diaria NASA POWER")
        regiao_clima = st.selectbox("Regiao", clima_diario["regiao"].unique())
        serie = clima_diario[clima_diario["regiao"] == regiao_clima].copy()
        if "data" in serie.columns:
            serie["data"] = pd.to_datetime(serie["data"], errors="coerce")
            serie = serie.sort_values("data")
            col_temp = next((c for c in ("temp_media", "temperatura_media_c") if c in serie.columns), None)
            col_chuva = next(
                (c for c in ("precipitacao_diaria_mm", "precipitacao_mm") if c in serie.columns),
                None,
            )
            c1, c2 = st.columns(2)
            if col_temp:
                c1.line_chart(
                    serie.set_index("data")[[col_temp]].rename(columns={col_temp: "Temp (C)"}),
                    height=240,
                )
            if col_chuva:
                c2.line_chart(
                    serie.set_index("data")[[col_chuva]].rename(columns={col_chuva: "Chuva (mm)"}),
                    height=240,
                )
    else:
        st.info("Base diaria NASA POWER nao encontrada.")


def renderizar_sensores(df: pd.DataFrame) -> None:
    st.subheader("Sensores de agua simulados")
    sensores = df[
        [
            "regiao",
            "nivel_reservatorio_pct",
            "ph_agua",
            "turbidez_ntu",
            "condutividade_us_cm",
            "temperatura_agua_c",
            "classificacao_qualidade_agua",
            "potencial_pluvial_m3_ano",
        ]
    ].copy()
    st.dataframe(sensores, width="stretch", hide_index=True)


def renderizar_mapa(df: pd.DataFrame) -> None:
    st.subheader("Mapa das regioes")
    mapa = df[["latitude", "longitude", "score_ia_0_10"]].copy()
    mapa.columns = ["lat", "lon", "Score IA"]
    st.map(mapa, latitude="lat", longitude="lon", size="Score IA", color="#0f8b8d")


def renderizar_dashboard_interativo() -> None:
    """Painel interativo com ranking IA e abas de analise."""
    if not ARQUIVO_MODELO.exists():
        st.error(
            "Modelo de IA nao encontrado. Execute antes:\n\n"
            "`python src/ml/treinar_modelo.py` ou a opcao 9 do menu."
        )
        st.stop()

    try:
        _, metadata = carregar_modelo_ia()
        df = aplicar_modelo_ia(ARQUIVO_MODELO.stat().st_mtime)
    except FileNotFoundError as erro:
        st.error(str(erro))
        st.stop()

    renderizar_cabecalho(metadata)
    destaque = renderizar_sidebar(metadata)
    clima_diario = carregar_clima_diario()

    renderizar_kpis(df)

    aba_ranking, aba_indicadores, aba_clima, aba_sensores, aba_mapa, aba_modelo = st.tabs(
        ["Ranking IA", "Indicadores", "Clima", "Sensores", "Mapa", "Modelo IA"]
    )

    with aba_ranking:
        renderizar_podio(df)
        renderizar_ranking(df, destaque)
    with aba_indicadores:
        renderizar_indicadores(df, destaque)
    with aba_clima:
        renderizar_clima(df, clima_diario)
    with aba_sensores:
        renderizar_sensores(df)
    with aba_mapa:
        renderizar_mapa(df)
    with aba_modelo:
        st.subheader("Detalhes do modelo treinado")
        st.json(metadata)
        st.markdown("**Features utilizadas pelo modelo:**")
        st.code("\n".join(metadata["features"]), language="text")

    st.markdown("---")
    st.caption("POC academica FIAP — ranking exibido com base no modelo salvo em src/models/.")
