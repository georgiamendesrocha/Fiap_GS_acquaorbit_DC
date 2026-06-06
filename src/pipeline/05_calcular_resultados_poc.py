"""
Acqua Orbit DC - Etapa 05
Calculo dos indicadores finais, sensores simulados e classificacao da POC.

Entrada:
    data/regioes.csv

Saidas geradas:
    data/resultados_regioes.csv
    output/relatorio_resultados_poc.md

Uso:
    python src/pipeline/05_calcular_resultados_poc.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC if (_SRC / "paths.py").exists() else _SRC.parent))
from paths import DATA, DOCUMENT, MODELS, OUTPUT, ROOT, SCRIPTS_DB, SRC, ASSETS  # noqa: E402

from pathlib import Path

import pandas as pd



ARQUIVO_REGIOES = DATA / "regioes.csv"
ARQUIVO_RESULTADOS = DATA / "resultados_regioes.csv"
ARQUIVO_RELATORIO = OUTPUT / "relatorio_resultados_poc.md"

COLUNAS_OBRIGATORIAS = [
    "regiao_id",
    "regiao",
    "cidade",
    "estado",
    "latitude",
    "longitude",
    "temperatura_media_anual_c",
    "temperatura_maxima_anual_c",
    "precipitacao_total_anual_mm",
    "umidade_media_anual_pct",
    "risco_hidrico_score_0_10",
    "risco_inundacao_score_0_10",
    "sensibilidade_territorial_score_0_10",
    "demanda_refrigeracao_score_0_10",
    "area_captacao_m2",
    "capacidade_reservatorio_l",
    "consumo_agua_tecnico_m3_dia",
    "potencial_pluvial_m3_ano",
    "conectividade_critica_score_0_10",
    "redundancia_fibra_score_0_10",
    "disponibilidade_energetica_score_0_10",
    "risco_rota_unica_score_0_10",
    "resiliencia_operacional_score_0_10",
]

COLUNAS_NUMERICAS = [
    "latitude",
    "longitude",
    "temperatura_media_anual_c",
    "temperatura_maxima_anual_c",
    "precipitacao_total_anual_mm",
    "umidade_media_anual_pct",
    "risco_hidrico_score_0_10",
    "risco_inundacao_score_0_10",
    "sensibilidade_territorial_score_0_10",
    "demanda_refrigeracao_score_0_10",
    "area_captacao_m2",
    "capacidade_reservatorio_l",
    "consumo_agua_tecnico_m3_dia",
    "potencial_pluvial_m3_ano",
    "conectividade_critica_score_0_10",
    "redundancia_fibra_score_0_10",
    "disponibilidade_energetica_score_0_10",
    "risco_rota_unica_score_0_10",
    "resiliencia_operacional_score_0_10",
]

CLASSIFICACOES_VALIDAS = {
    "favorável",
    "atenção",
    "alto risco",
    "crítica",
}


def carregar_regioes() -> pd.DataFrame:
    if not ARQUIVO_REGIOES.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {ARQUIVO_REGIOES}\n"
            "Execute antes os scripts 03_montar_regioes_csv.py e 04_validar_regioes_csv.py."
        )

    df = pd.read_csv(ARQUIVO_REGIOES)
    validar_colunas(df)

    for coluna in COLUNAS_NUMERICAS:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    if df[COLUNAS_NUMERICAS].isna().sum().sum() > 0:
        raise ValueError("Ha valores numericos invalidos em data/regioes.csv.")

    return df


def validar_colunas(df: pd.DataFrame) -> None:
    ausentes = [coluna for coluna in COLUNAS_OBRIGATORIAS if coluna not in df.columns]
    if ausentes:
        raise ValueError(f"Colunas obrigatorias ausentes em data/regioes.csv: {ausentes}")


def limitar(valor: float, minimo: float = 0.0, maximo: float = 10.0) -> float:
    return min(max(valor, minimo), maximo)


def simular_sensores_agua(linha: pd.Series) -> dict[str, float | str]:
    consumo_mensal_m3 = float(linha["consumo_agua_tecnico_m3_dia"]) * 30
    potencial_mensal_m3 = float(linha["potencial_pluvial_m3_ano"]) / 12
    nivel_reservatorio_pct = limitar((potencial_mensal_m3 / consumo_mensal_m3) * 100, 25, 95)

    precipitacao = float(linha["precipitacao_total_anual_mm"])
    risco_inundacao = float(linha["risco_inundacao_score_0_10"])
    risco_hidrico = float(linha["risco_hidrico_score_0_10"])
    sensibilidade = float(linha["sensibilidade_territorial_score_0_10"])
    umidade = float(linha["umidade_media_anual_pct"])
    temp_media = float(linha["temperatura_media_anual_c"])

    ph_agua = limitar(7.1 + ((precipitacao - 950) / 1000) - (risco_inundacao * 0.03), 6.2, 8.4)
    turbidez_ntu = limitar(2.0 + (risco_inundacao * 0.7) + ((umidade - 70) * 0.05), 1.0, 15.0)
    condutividade_us_cm = limitar(180 + (risco_hidrico * 22) + (sensibilidade * 8), 120, 900)
    temperatura_agua_c = limitar(temp_media - 1.5, 10, 35)

    if 6.5 <= ph_agua <= 8.5 and turbidez_ntu <= 5 and condutividade_us_cm <= 500:
        classificacao = "adequada"
    elif 6.0 <= ph_agua <= 9.0 and turbidez_ntu <= 10 and condutividade_us_cm <= 800:
        classificacao = "necessita tratamento"
    else:
        classificacao = "deve ser descartada"

    return {
        "nivel_reservatorio_pct": round(nivel_reservatorio_pct, 2),
        "ph_agua": round(ph_agua, 2),
        "turbidez_ntu": round(turbidez_ntu, 2),
        "condutividade_us_cm": round(condutividade_us_cm, 2),
        "temperatura_agua_c": round(temperatura_agua_c, 2),
        "classificacao_qualidade_agua": classificacao,
    }


def calcular_qualidade_agua_score(sensores: dict[str, float | str]) -> float:
    ph = float(sensores["ph_agua"])
    turbidez = float(sensores["turbidez_ntu"])
    condutividade = float(sensores["condutividade_us_cm"])
    temperatura = float(sensores["temperatura_agua_c"])

    score = 10
    score -= abs(ph - 7.2) * 1.2
    score -= turbidez * 0.35
    score -= max(0, condutividade - 350) / 100
    score -= max(0, temperatura - 25) * 0.5

    return round(limitar(score), 2)


def calcular_indicadores(linha: pd.Series, sensores: dict[str, float | str]) -> dict[str, float | str]:
    risco_hidrico = float(linha["risco_hidrico_score_0_10"])
    risco_inundacao = float(linha["risco_inundacao_score_0_10"])
    sensibilidade = float(linha["sensibilidade_territorial_score_0_10"])
    demanda_refrigeracao = float(linha["demanda_refrigeracao_score_0_10"])
    precipitacao = float(linha["precipitacao_total_anual_mm"])
    potencial_pluvial = float(linha["potencial_pluvial_m3_ano"])
    consumo_diario = float(linha["consumo_agua_tecnico_m3_dia"])

    pressao_chuva_score = limitar((precipitacao / 1200) * 10)
    risco_ambiental = (
        risco_hidrico * 0.25
        + risco_inundacao * 0.25
        + sensibilidade * 0.20
        + demanda_refrigeracao * 0.20
        + pressao_chuva_score * 0.10
    )
    risco_ambiental = round(limitar(risco_ambiental), 2)

    indicador_geoespacial = round(
        limitar(10 - ((risco_inundacao + sensibilidade + pressao_chuva_score) / 3)),
        2,
    )

    cobertura_reuso_pluvial_pct = (potencial_pluvial / (consumo_diario * 365)) * 100
    potencial_reuso_score = round(limitar(cobertura_reuso_pluvial_pct), 2)

    conectividade_score = round(
        limitar(
            (float(linha["conectividade_critica_score_0_10"]) * 0.40)
            + (float(linha["redundancia_fibra_score_0_10"]) * 0.35)
            + ((10 - float(linha["risco_rota_unica_score_0_10"])) * 0.25)
        ),
        2,
    )

    energia_score = round(
        limitar(
            (float(linha["disponibilidade_energetica_score_0_10"]) * 0.70)
            + (float(linha["resiliencia_operacional_score_0_10"]) * 0.30)
        ),
        2,
    )

    qualidade_agua_score = calcular_qualidade_agua_score(sensores)
    ambiental_favoravel_score = round(limitar(10 - risco_ambiental), 2)
    transparencia_score = 9.0

    esg_resiliencia_score = round(
        limitar(
            ambiental_favoravel_score * 0.30
            + potencial_reuso_score * 0.20
            + qualidade_agua_score * 0.15
            + ((conectividade_score + energia_score) / 2) * 0.25
            + transparencia_score * 0.10
        ),
        2,
    )

    score_final = round(
        limitar(
            indicador_geoespacial * 0.15
            + ambiental_favoravel_score * 0.25
            + potencial_reuso_score * 0.15
            + qualidade_agua_score * 0.10
            + conectividade_score * 0.15
            + energia_score * 0.10
            + float(linha["resiliencia_operacional_score_0_10"]) * 0.10
        ),
        2,
    )

    return {
        "indicador_geoespacial_score_0_10": indicador_geoespacial,
        "risco_ambiental_climatico_score_0_10": risco_ambiental,
        "ambiental_favoravel_score_0_10": ambiental_favoravel_score,
        "cobertura_reuso_pluvial_pct": round(cobertura_reuso_pluvial_pct, 2),
        "indice_potencial_reuso_pluvial_score_0_10": potencial_reuso_score,
        "indice_qualidade_agua_score_0_10": qualidade_agua_score,
        "indice_conectividade_critica_score_0_10": conectividade_score,
        "indice_disponibilidade_energetica_score_0_10": energia_score,
        "indice_refrigeracao_risco_termico_score_0_10": round(demanda_refrigeracao, 2),
        "indice_esg_resiliencia_score_0_10": esg_resiliencia_score,
        "score_final_poc_0_10": score_final,
    }


def classificar_regiao(score_final: float) -> str:
    if score_final >= 7.0:
        return "favorável"
    if score_final >= 5.5:
        return "atenção"
    if score_final >= 4.0:
        return "alto risco"
    return "crítica"


def gerar_parecer(classificacao: str) -> str:
    if classificacao == "favorável":
        return "Boa combinacao entre clima, reuso pluvial, infraestrutura critica e resiliencia para a POC."
    if classificacao == "atenção":
        return "Regiao utilizavel na POC, mas exige cautela em riscos ambientais, operacionais ou de qualidade simulada da agua."
    if classificacao == "alto risco":
        return "Regiao com fatores relevantes de cautela; exigiria mitigacoes antes de uma decisao real."
    return "Regiao critica no modelo academico; nao recomendada sem revisao profunda dos riscos."


def calcular_resultados(df_regioes: pd.DataFrame) -> pd.DataFrame:
    linhas = []

    for _, linha in df_regioes.iterrows():
        sensores = simular_sensores_agua(linha)
        indicadores = calcular_indicadores(linha, sensores)
        classificacao = classificar_regiao(float(indicadores["score_final_poc_0_10"]))

        registro = {
            **linha.to_dict(),
            **sensores,
            **indicadores,
            "classificacao_final": classificacao,
            "parecer_apoio_decisao": gerar_parecer(classificacao),
            "origem_sensores_agua": "simulado",
            "origem_indicadores_finais": "calculado",
            "origem_classificacao_final": "calculado",
        }

        linhas.append(registro)

    df = pd.DataFrame(linhas)
    validar_resultados(df)

    return df.sort_values("score_final_poc_0_10", ascending=False)


def validar_resultados(df: pd.DataFrame) -> None:
    colunas_score = [coluna for coluna in df.columns if coluna.endswith("_score_0_10")]

    for coluna in colunas_score:
        invalidos = df[(df[coluna] < 0) | (df[coluna] > 10)]
        if not invalidos.empty:
            raise ValueError(f"Score fora da escala 0-10 na coluna: {coluna}")

    classificacoes = set(df["classificacao_final"].dropna().astype(str))
    invalidas = classificacoes - CLASSIFICACOES_VALIDAS
    if invalidas:
        raise ValueError(f"Classificacoes finais invalidas: {sorted(invalidas)}")


def salvar_relatorio(df: pd.DataFrame) -> None:
    OUTPUT.mkdir(exist_ok=True)

    ranking = []
    for posicao, row in enumerate(df.itertuples(), start=1):
        ranking.append(
            f"{posicao}. {row.regiao} - score {row.score_final_poc_0_10} - {row.classificacao_final}"
        )

    qualidade_agua = []
    for row in df.itertuples():
        qualidade_agua.append(
            f"- {row.regiao}: {row.classificacao_qualidade_agua} "
            f"(pH {row.ph_agua}, turbidez {row.turbidez_ntu} NTU, nivel {row.nivel_reservatorio_pct}%)"
        )

    relatorio = f"""# Relatorio de Resultados da POC - Acqua Orbit DC

## Etapa executada

Calculo dos indicadores finais, simulacao de sensores de agua e classificacao final das regioes.

## Arquivos gerados

- `data/resultados_regioes.csv`
- `output/relatorio_resultados_poc.md`

## Ranking final

{chr(10).join(ranking)}

## Qualidade simulada da agua

{chr(10).join(qualidade_agua)}

## Indicadores calculados

- Indicador geoespacial simplificado.
- Indice de risco ambiental e climatico.
- Indice de potencial de reuso pluvial.
- Indice de qualidade simulada da agua.
- Indice de conectividade critica.
- Indice de disponibilidade energetica.
- Indice de refrigeracao e risco termico.
- Indice ESG e de resiliencia.
- Classificacao final da regiao.

## Observacao

Os resultados sao uma simulacao academica de apoio a decisao. A POC nao substitui laudo ambiental, auditoria ESG, estudo profissional de data center, telecomunicacoes ou energia.
"""
    ARQUIVO_RELATORIO.write_text(relatorio, encoding="utf-8")


def main() -> None:
    print("Acqua Orbit DC - Calculo dos resultados finais da POC")

    DATA.mkdir(exist_ok=True)
    OUTPUT.mkdir(exist_ok=True)

    df_regioes = carregar_regioes()
    print(f"Base regioes carregada: {len(df_regioes)} regioes")

    df_resultados = calcular_resultados(df_regioes)
    print("Indicadores finais calculados")

    df_resultados.to_csv(ARQUIVO_RESULTADOS, index=False, encoding="utf-8-sig")
    salvar_relatorio(df_resultados)

    print("Etapa 05 concluida com sucesso")
    print(f"- {ARQUIVO_RESULTADOS}")
    print(f"- {ARQUIVO_RELATORIO}")


if __name__ == "__main__":
    main()
