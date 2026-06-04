"""
Acqua Orbit DC - Etapa 06
Geracao de dashboard HTML simples para apresentacao da POC.

Entrada:
    data/resultados_regioes.csv

Saidas geradas:
    output/dashboard_poc.html
    output/relatorio_visualizacoes_poc.md

Uso:
    python scripts/06_gerar_visualizacoes.py
"""

from html import escape
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

ARQUIVO_RESULTADOS = DATA_DIR / "resultados_regioes.csv"
ARQUIVO_DASHBOARD = OUTPUT_DIR / "dashboard_poc.html"
ARQUIVO_RELATORIO = OUTPUT_DIR / "relatorio_visualizacoes_poc.md"

CORES_REGIOES = {
    "SP_BARUERI_TAMBORE": "#0f8b8d",
    "PR_CURITIBA": "#6a8d22",
    "RJ_BARRA_JACAREPAGUA_PARQUE_OLIMPICO": "#d95d39",
}

COLUNAS_OBRIGATORIAS = [
    "regiao_id",
    "regiao",
    "cidade",
    "estado",
    "latitude",
    "longitude",
    "classificacao_final",
    "classificacao_qualidade_agua",
    "score_final_poc_0_10",
    "risco_ambiental_climatico_score_0_10",
    "indice_esg_resiliencia_score_0_10",
    "indice_potencial_reuso_pluvial_score_0_10",
    "indice_conectividade_critica_score_0_10",
    "indice_disponibilidade_energetica_score_0_10",
    "indicador_geoespacial_score_0_10",
    "nivel_reservatorio_pct",
    "ph_agua",
    "turbidez_ntu",
    "parecer_apoio_decisao",
]

COLUNAS_NUMERICAS = [
    "latitude",
    "longitude",
    "score_final_poc_0_10",
    "risco_ambiental_climatico_score_0_10",
    "indice_esg_resiliencia_score_0_10",
    "indice_potencial_reuso_pluvial_score_0_10",
    "indice_conectividade_critica_score_0_10",
    "indice_disponibilidade_energetica_score_0_10",
    "indicador_geoespacial_score_0_10",
    "nivel_reservatorio_pct",
    "ph_agua",
    "turbidez_ntu",
]


def carregar_resultados() -> pd.DataFrame:
    if not ARQUIVO_RESULTADOS.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {ARQUIVO_RESULTADOS}\n"
            "Execute antes o script 05_calcular_resultados_poc.py."
        )

    df = pd.read_csv(ARQUIVO_RESULTADOS)
    ausentes = [coluna for coluna in COLUNAS_OBRIGATORIAS if coluna not in df.columns]
    if ausentes:
        raise ValueError(f"Colunas obrigatorias ausentes em resultados_regioes.csv: {ausentes}")

    for coluna in COLUNAS_NUMERICAS:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    if df[COLUNAS_NUMERICAS].isna().sum().sum() > 0:
        raise ValueError("Ha valores numericos invalidos em resultados_regioes.csv.")

    return df.sort_values("score_final_poc_0_10", ascending=False).reset_index(drop=True)


def fmt(valor: float, casas: int = 2) -> str:
    return f"{valor:.{casas}f}"


def cor_regiao(row: pd.Series) -> str:
    return CORES_REGIOES.get(str(row["regiao_id"]), "#305f72")


def classe_status(classificacao: str) -> str:
    if classificacao == "favorável":
        return "status-good"
    if classificacao == "atenção":
        return "status-warn"
    if classificacao == "alto risco":
        return "status-risk"
    return "status-critical"


def grafico_barras(df: pd.DataFrame, coluna: str, titulo: str, subtitulo: str) -> str:
    largura = 760
    altura_linha = 72
    margem_esq = 250
    margem_dir = 70
    margem_topo = 34
    altura = margem_topo + (len(df) * altura_linha) + 26
    largura_barra = largura - margem_esq - margem_dir

    linhas_svg = [
        f'<svg viewBox="0 0 {largura} {altura}" role="img" aria-label="{escape(titulo)}">',
        f'<text x="0" y="18" class="svg-title">{escape(titulo)}</text>',
        f'<text x="0" y="36" class="svg-subtitle">{escape(subtitulo)}</text>',
    ]

    for indice, row in df.iterrows():
        valor = float(row[coluna])
        largura_valor = max(4, (valor / 10) * largura_barra)
        y = margem_topo + 22 + (indice * altura_linha)
        label = f"{row['cidade']}/{row['estado']}"
        linhas_svg.extend(
            [
                f'<text x="0" y="{y + 18}" class="svg-label">{escape(label)}</text>',
                f'<rect x="{margem_esq}" y="{y}" width="{largura_barra}" height="26" rx="5" class="bar-track"/>',
                f'<rect x="{margem_esq}" y="{y}" width="{largura_valor:.2f}" height="26" rx="5" fill="{cor_regiao(row)}"/>',
                f'<text x="{margem_esq + largura_barra + 12}" y="{y + 18}" class="svg-value">{fmt(valor)}</text>',
            ]
        )

    linhas_svg.append("</svg>")
    return "\n".join(linhas_svg)


def grafico_barras_percentual(df: pd.DataFrame, coluna: str, titulo: str, subtitulo: str) -> str:
    largura = 760
    altura_linha = 72
    margem_esq = 250
    margem_dir = 92
    margem_topo = 34
    altura = margem_topo + (len(df) * altura_linha) + 26
    largura_barra = largura - margem_esq - margem_dir

    linhas_svg = [
        f'<svg viewBox="0 0 {largura} {altura}" role="img" aria-label="{escape(titulo)}">',
        f'<text x="0" y="18" class="svg-title">{escape(titulo)}</text>',
        f'<text x="0" y="36" class="svg-subtitle">{escape(subtitulo)}</text>',
    ]

    maximo = max(float(df[coluna].max()), 1)
    for indice, row in df.iterrows():
        valor = float(row[coluna])
        largura_valor = max(4, (valor / maximo) * largura_barra)
        y = margem_topo + 22 + (indice * altura_linha)
        label = f"{row['cidade']}/{row['estado']}"
        linhas_svg.extend(
            [
                f'<text x="0" y="{y + 18}" class="svg-label">{escape(label)}</text>',
                f'<rect x="{margem_esq}" y="{y}" width="{largura_barra}" height="26" rx="5" class="bar-track"/>',
                f'<rect x="{margem_esq}" y="{y}" width="{largura_valor:.2f}" height="26" rx="5" fill="{cor_regiao(row)}"/>',
                f'<text x="{margem_esq + largura_barra + 12}" y="{y + 18}" class="svg-value">{fmt(valor, 1)}%</text>',
            ]
        )

    linhas_svg.append("</svg>")
    return "\n".join(linhas_svg)


def mapa_svg(df: pd.DataFrame) -> str:
    largura = 760
    altura = 360
    margem = 54
    lat_min = float(df["latitude"].min())
    lat_max = float(df["latitude"].max())
    lon_min = float(df["longitude"].min())
    lon_max = float(df["longitude"].max())
    lat_span = lat_max - lat_min or 1
    lon_span = lon_max - lon_min or 1

    linhas_svg = [
        f'<svg viewBox="0 0 {largura} {altura}" role="img" aria-label="Mapa simplificado por coordenadas">',
        '<text x="0" y="18" class="svg-title">Mapa simplificado por coordenadas</text>',
        '<text x="0" y="36" class="svg-subtitle">Posicionamento relativo das regioes oficiais da POC</text>',
        f'<rect x="{margem}" y="{margem}" width="{largura - margem * 2}" height="{altura - margem * 2}" rx="8" class="map-area"/>',
    ]

    for passo in range(1, 4):
        x = margem + ((largura - margem * 2) / 4) * passo
        y = margem + ((altura - margem * 2) / 4) * passo
        linhas_svg.append(f'<line x1="{x}" y1="{margem}" x2="{x}" y2="{altura - margem}" class="grid-line"/>')
        linhas_svg.append(f'<line x1="{margem}" y1="{y}" x2="{largura - margem}" y2="{y}" class="grid-line"/>')

    for _, row in df.iterrows():
        x = margem + ((float(row["longitude"]) - lon_min) / lon_span) * (largura - margem * 2)
        y = altura - margem - ((float(row["latitude"]) - lat_min) / lat_span) * (altura - margem * 2)
        label = f"{row['cidade']}/{row['estado']}"
        linhas_svg.extend(
            [
                f'<circle cx="{x:.2f}" cy="{y:.2f}" r="10" fill="{cor_regiao(row)}"/>',
                f'<circle cx="{x:.2f}" cy="{y:.2f}" r="18" fill="{cor_regiao(row)}" opacity="0.15"/>',
                f'<text x="{x + 16:.2f}" y="{y - 10:.2f}" class="map-label">{escape(label)}</text>',
                f'<text x="{x + 16:.2f}" y="{y + 8:.2f}" class="map-value">score {fmt(float(row["score_final_poc_0_10"]))}</text>',
            ]
        )

    linhas_svg.extend(
        [
            f'<text x="{margem}" y="{altura - 16}" class="axis-label">Longitude {fmt(lon_min)} a {fmt(lon_max)}</text>',
            f'<text x="{largura - 236}" y="{altura - 16}" class="axis-label">Latitude {fmt(lat_min)} a {fmt(lat_max)}</text>',
            "</svg>",
        ]
    )
    return "\n".join(linhas_svg)


def cards_ranking(df: pd.DataFrame) -> str:
    cards = []

    for posicao, row in enumerate(df.itertuples(), start=1):
        classificacao = str(row.classificacao_final)
        cards.append(
            f"""
            <article class="region-card">
                <div class="rank-line">
                    <span class="rank-number">{posicao}</span>
                    <span class="status {classe_status(classificacao)}">{escape(classificacao)}</span>
                </div>
                <h3>{escape(row.regiao)}</h3>
                <p class="muted">{escape(row.cidade)}/{escape(row.estado)}</p>
                <div class="score" style="--accent:{CORES_REGIOES.get(str(row.regiao_id), '#305f72')}">
                    <span>{fmt(float(row.score_final_poc_0_10))}</span>
                    <small>score final</small>
                </div>
                <p>{escape(row.parecer_apoio_decisao)}</p>
            </article>
            """
        )

    return "\n".join(cards)


def tabela_sensores(df: pd.DataFrame) -> str:
    linhas = []

    for row in df.itertuples():
        linhas.append(
            f"""
            <tr>
                <td>{escape(row.cidade)}/{escape(row.estado)}</td>
                <td>{escape(row.classificacao_qualidade_agua)}</td>
                <td>{fmt(float(row.nivel_reservatorio_pct), 1)}%</td>
                <td>{fmt(float(row.ph_agua))}</td>
                <td>{fmt(float(row.turbidez_ntu))}</td>
                <td>{fmt(float(row.indice_qualidade_agua_score_0_10))}</td>
            </tr>
            """
        )

    return "\n".join(linhas)


def gerar_html(df: pd.DataFrame) -> str:
    melhor = df.iloc[0]
    total_regioes = len(df)
    favoraveis = int((df["classificacao_final"] == "favorável").sum())
    atencao = int((df["classificacao_final"] == "atenção").sum())

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Acqua Orbit DC - Dashboard POC</title>
    <style>
        :root {{
            --ink: #172026;
            --muted: #5c6873;
            --line: #d8e0e6;
            --paper: #f7f9fb;
            --panel: #ffffff;
            --blue: #305f72;
            --teal: #0f8b8d;
            --green: #6a8d22;
            --amber: #c98a12;
            --red: #b23a48;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            color: var(--ink);
            background: var(--paper);
            font-family: Arial, Helvetica, sans-serif;
            line-height: 1.5;
        }}

        header {{
            background: #102a43;
            color: #ffffff;
            padding: 34px 24px 28px;
        }}

        .wrap {{
            width: min(1160px, calc(100% - 32px));
            margin: 0 auto;
        }}

        h1 {{
            margin: 0;
            font-size: 34px;
            font-weight: 800;
            letter-spacing: 0;
        }}

        h2 {{
            margin: 0 0 16px;
            font-size: 22px;
            letter-spacing: 0;
        }}

        h3 {{
            margin: 12px 0 4px;
            font-size: 18px;
            letter-spacing: 0;
        }}

        p {{
            margin: 0 0 12px;
        }}

        .subhead {{
            max-width: 860px;
            margin-top: 10px;
            color: #d9e7f2;
        }}

        main {{
            padding: 24px 0 42px;
        }}

        section {{
            margin-top: 22px;
        }}

        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
        }}

        .metric {{
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 16px;
            min-height: 112px;
        }}

        .metric strong {{
            display: block;
            font-size: 28px;
            line-height: 1.1;
        }}

        .metric span {{
            color: var(--muted);
            font-size: 14px;
        }}

        .region-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
        }}

        .region-card,
        .panel {{
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 18px;
        }}

        .rank-line {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }}

        .rank-number {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 34px;
            height: 34px;
            border-radius: 50%;
            color: #ffffff;
            background: var(--blue);
            font-weight: 700;
        }}

        .status {{
            display: inline-flex;
            min-height: 28px;
            align-items: center;
            border-radius: 999px;
            padding: 3px 10px;
            color: #ffffff;
            font-size: 13px;
            font-weight: 700;
        }}

        .status-good {{ background: var(--green); }}
        .status-warn {{ background: var(--amber); }}
        .status-risk {{ background: #b56a00; }}
        .status-critical {{ background: var(--red); }}

        .muted {{
            color: var(--muted);
        }}

        .score {{
            margin: 14px 0;
            padding: 10px 0 10px 14px;
            border-left: 5px solid var(--accent);
        }}

        .score span {{
            display: block;
            font-size: 30px;
            font-weight: 800;
            line-height: 1;
        }}

        .score small {{
            color: var(--muted);
            font-size: 13px;
        }}

        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 14px;
        }}

        svg {{
            width: 100%;
            height: auto;
            display: block;
        }}

        .svg-title {{
            font-size: 17px;
            font-weight: 800;
            fill: var(--ink);
        }}

        .svg-subtitle,
        .axis-label {{
            font-size: 12px;
            fill: var(--muted);
        }}

        .svg-label {{
            font-size: 13px;
            font-weight: 700;
            fill: var(--ink);
        }}

        .svg-value {{
            font-size: 13px;
            font-weight: 800;
            fill: var(--ink);
        }}

        .bar-track {{
            fill: #e8eef2;
        }}

        .map-area {{
            fill: #eef4f7;
            stroke: var(--line);
        }}

        .grid-line {{
            stroke: #d3dde4;
            stroke-width: 1;
        }}

        .map-label {{
            font-size: 13px;
            font-weight: 800;
            fill: var(--ink);
        }}

        .map-value {{
            font-size: 12px;
            fill: var(--muted);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}

        th,
        td {{
            border-bottom: 1px solid var(--line);
            padding: 10px 8px;
            text-align: left;
            vertical-align: top;
        }}

        th {{
            color: var(--muted);
            font-size: 12px;
            text-transform: uppercase;
        }}

        .footnote {{
            margin-top: 24px;
            color: var(--muted);
            font-size: 13px;
        }}

        @media (max-width: 900px) {{
            .summary-grid,
            .region-grid,
            .chart-grid {{
                grid-template-columns: 1fr;
            }}

            h1 {{
                font-size: 28px;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="wrap">
            <h1>Acqua Orbit DC</h1>
            <p class="subhead">Dashboard da POC com classificacao ESG, risco ambiental, reuso pluvial, sensores simulados e infraestrutura critica digital para regioes candidatas a data centers.</p>
        </div>
    </header>

    <main class="wrap">
        <section class="summary-grid" aria-label="Resumo executivo">
            <div class="metric">
                <strong>{total_regioes}</strong>
                <span>regioes oficiais avaliadas</span>
            </div>
            <div class="metric">
                <strong>{escape(str(melhor["cidade"]))}/{escape(str(melhor["estado"]))}</strong>
                <span>melhor classificacao da POC</span>
            </div>
            <div class="metric">
                <strong>{favoraveis}</strong>
                <span>regiao em classificacao favoravel</span>
            </div>
            <div class="metric">
                <strong>{atencao}</strong>
                <span>regioes em atencao</span>
            </div>
        </section>

        <section>
            <h2>Ranking Final</h2>
            <div class="region-grid">
                {cards_ranking(df)}
            </div>
        </section>

        <section class="chart-grid">
            <div class="panel">
                {grafico_barras(df, "score_final_poc_0_10", "Score final da POC", "Quanto maior, melhor a condicao comparativa")}
            </div>
            <div class="panel">
                {grafico_barras(df, "indice_esg_resiliencia_score_0_10", "Indice ESG e resiliencia", "Combinacao de ambiente, reuso, agua e infraestrutura")}
            </div>
            <div class="panel">
                {grafico_barras(df, "risco_ambiental_climatico_score_0_10", "Risco ambiental e climatico", "Quanto maior, maior a cautela ambiental")}
            </div>
            <div class="panel">
                {grafico_barras(df, "indice_conectividade_critica_score_0_10", "Conectividade critica", "Robustez parametrizada da infraestrutura digital")}
            </div>
            <div class="panel">
                {grafico_barras(df, "indice_disponibilidade_energetica_score_0_10", "Disponibilidade energetica", "Condicao parametrizada de energia e resiliencia")}
            </div>
            <div class="panel">
                {grafico_barras_percentual(df, "cobertura_reuso_pluvial_pct", "Cobertura estimada de reuso pluvial", "Potencial anual frente ao consumo tecnico simulado")}
            </div>
        </section>

        <section class="chart-grid">
            <div class="panel">
                {mapa_svg(df)}
            </div>
            <div class="panel">
                <h2>Sensores simulados de agua</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Regiao</th>
                            <th>Qualidade</th>
                            <th>Nivel</th>
                            <th>pH</th>
                            <th>Turbidez</th>
                            <th>Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tabela_sensores(df)}
                    </tbody>
                </table>
            </div>
        </section>

        <p class="footnote">POC academica. Os resultados sao apoio simulado a decisao e nao substituem laudos tecnicos, auditorias ESG ou estudos profissionais de data center, energia, telecomunicacoes e meio ambiente.</p>
    </main>
</body>
</html>
"""


def salvar_relatorio(df: pd.DataFrame) -> None:
    ranking = []
    for posicao, row in enumerate(df.itertuples(), start=1):
        ranking.append(
            f"{posicao}. {row.regiao} - score {row.score_final_poc_0_10} - {row.classificacao_final}"
        )

    relatorio = f"""# Relatorio de Visualizacoes da POC - Acqua Orbit DC

## Etapa executada

Geracao de dashboard HTML simples a partir de `data/resultados_regioes.csv`.

## Arquivo gerado

- `output/dashboard_poc.html`

## Visualizacoes incluidas

- Ranking final das regioes.
- Grafico de score final.
- Grafico de indice ESG e resiliencia.
- Grafico de risco ambiental e climatico.
- Grafico de conectividade critica.
- Grafico de disponibilidade energetica.
- Grafico de cobertura estimada de reuso pluvial.
- Mapa simplificado por latitude e longitude.
- Tabela de sensores simulados de agua.

## Ranking exibido

{chr(10).join(ranking)}
"""
    ARQUIVO_RELATORIO.write_text(relatorio, encoding="utf-8")


def main() -> None:
    print("Acqua Orbit DC - Geracao de visualizacoes da POC")

    OUTPUT_DIR.mkdir(exist_ok=True)
    df = carregar_resultados()
    print(f"Resultados carregados: {len(df)} regioes")

    html = gerar_html(df)
    ARQUIVO_DASHBOARD.write_text(html, encoding="utf-8")
    salvar_relatorio(df)

    print("Etapa 06 concluida com sucesso")
    print(f"- {ARQUIVO_DASHBOARD}")
    print(f"- {ARQUIVO_RELATORIO}")


if __name__ == "__main__":
    main()
