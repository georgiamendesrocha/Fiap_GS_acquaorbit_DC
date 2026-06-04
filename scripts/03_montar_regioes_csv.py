"""
Acqua Orbit DC - Etapa 03
Montagem do CSV oficial da POC: data/regioes.csv.

Entrada principal:
    data/nasa_power_2025_diario_tratado.csv

Entrada alternativa:
    data/clima_regioes_2025_tratado.csv

Saidas geradas:
    data/regioes.csv
    output/relatorio_montagem_regioes_csv.md

Uso:
    python scripts/03_montar_regioes_csv.py
"""

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

ARQUIVO_CLIMA_DIARIO = DATA_DIR / "nasa_power_2025_diario_tratado.csv"
ARQUIVO_CLIMA_RESUMO = DATA_DIR / "clima_regioes_2025_tratado.csv"
ARQUIVO_SAIDA = DATA_DIR / "regioes.csv"
ARQUIVO_RELATORIO = OUTPUT_DIR / "relatorio_montagem_regioes_csv.md"

ORDEM_REGIOES = [
    "Barueri/Tamboré",
    "Rio de Janeiro - Barra/Jacarepaguá/Parque Olímpico",
    "Curitiba",
]

COLUNAS_DIARIO_OBRIGATORIAS = [
    "data",
    "regiao",
    "cidade",
    "estado",
    "latitude",
    "longitude",
    "temp_media",
    "temp_maxima",
    "temp_minima",
    "precipitacao_diaria_mm",
    "umidade_media",
    "vento_medio",
    "radiacao_media",
    "periodo_referencia",
    "fonte_climatica",
    "fonte_climatica_url",
    "origem_dados_climaticos",
]

COLUNAS_CLIMA_OBRIGATORIAS = [
    "regiao",
    "cidade",
    "estado",
    "latitude",
    "longitude",
    "temperatura_media_anual_c",
    "temperatura_maxima_anual_c",
    "precipitacao_total_anual_mm",
    "umidade_media_anual_pct",
    "periodo_referencia",
    "fonte_climatica",
    "fonte_climatica_url",
    "origem_dados_climaticos",
]

MAPA_COLUNAS_RESUMO_ATUAL = {
    "temp_media": "temperatura_media_anual_c",
    "temp_maxima": "temperatura_maxima_anual_c",
    "temp_minima": "temperatura_minima_anual_c",
    "precipitacao_anual_mm": "precipitacao_total_anual_mm",
    "umidade_media": "umidade_media_anual_pct",
    "vento_medio": "velocidade_vento_media_anual_m_s",
    "radiacao_media": "radiacao_solar_media_anual_kwh_m2_dia",
}

COLUNAS_NUMERICAS_DIARIO = [
    "latitude",
    "longitude",
    "temp_media",
    "temp_maxima",
    "temp_minima",
    "precipitacao_diaria_mm",
    "umidade_media",
    "vento_medio",
    "radiacao_media",
]

COLUNAS_NUMERICAS_RESUMO = [
    "latitude",
    "longitude",
    "temperatura_media_anual_c",
    "temperatura_maxima_anual_c",
    "temperatura_minima_anual_c",
    "precipitacao_total_anual_mm",
    "umidade_media_anual_pct",
    "velocidade_vento_media_anual_m_s",
    "radiacao_solar_media_anual_kwh_m2_dia",
]


# Valores definidos para POC academica. Nao representam laudo tecnico real.
PARAMETROS_REGIONAIS = {
    "Barueri/Tamboré": {
        "regiao_id": "SP_BARUERI_TAMBORE",
        "eixo_regional": "Barueri/Tamboré",
        "contexto_territorial": "Regiao metropolitana com forte presenca de infraestrutura tecnologica e pressao urbana moderada.",
        "bioma_contexto": "Mata Atlantica / Urbano",
        "risco_hidrico_score_0_10": 4.0,
        "risco_inundacao_score_0_10": 3.0,
        "sensibilidade_territorial_score_0_10": 4.0,
        "area_captacao_m2": 5000,
        "capacidade_reservatorio_l": 250000,
        "consumo_agua_tecnico_m3_dia": 120,
        "eficiencia_captacao_pct": 80,
        "conectividade_critica_score_0_10": 9.0,
        "redundancia_fibra_score_0_10": 9.0,
        "disponibilidade_energetica_score_0_10": 8.0,
        "risco_rota_unica_score_0_10": 2.0,
        "resiliencia_operacional_score_0_10": 8.5,
    },
    "Rio de Janeiro - Barra/Jacarepaguá/Parque Olímpico": {
        "regiao_id": "RJ_BARRA_JACAREPAGUA_PARQUE_OLIMPICO",
        "eixo_regional": "Barra/Jacarepaguá/Parque Olímpico",
        "contexto_territorial": "Eixo urbano metropolitano com boa infraestrutura, maior atencao a calor, chuvas intensas e risco de inundacao.",
        "bioma_contexto": "Mata Atlantica / Costeiro Urbano",
        "risco_hidrico_score_0_10": 5.0,
        "risco_inundacao_score_0_10": 7.0,
        "sensibilidade_territorial_score_0_10": 6.0,
        "area_captacao_m2": 5000,
        "capacidade_reservatorio_l": 250000,
        "consumo_agua_tecnico_m3_dia": 130,
        "eficiencia_captacao_pct": 80,
        "conectividade_critica_score_0_10": 8.0,
        "redundancia_fibra_score_0_10": 8.0,
        "disponibilidade_energetica_score_0_10": 7.0,
        "risco_rota_unica_score_0_10": 3.0,
        "resiliencia_operacional_score_0_10": 7.0,
    },
    "Curitiba": {
        "regiao_id": "PR_CURITIBA",
        "eixo_regional": "Curitiba",
        "contexto_territorial": "Regiao metropolitana com clima mais ameno, boa condicao urbana e menor pressao termica relativa.",
        "bioma_contexto": "Mata Atlantica / Urbano Sul",
        "risco_hidrico_score_0_10": 3.0,
        "risco_inundacao_score_0_10": 4.0,
        "sensibilidade_territorial_score_0_10": 3.5,
        "area_captacao_m2": 5000,
        "capacidade_reservatorio_l": 250000,
        "consumo_agua_tecnico_m3_dia": 110,
        "eficiencia_captacao_pct": 80,
        "conectividade_critica_score_0_10": 7.0,
        "redundancia_fibra_score_0_10": 7.0,
        "disponibilidade_energetica_score_0_10": 7.5,
        "risco_rota_unica_score_0_10": 4.0,
        "resiliencia_operacional_score_0_10": 7.0,
    },
}


def validar_colunas(df: pd.DataFrame, obrigatorias: list[str], origem: Path) -> None:
    ausentes = [coluna for coluna in obrigatorias if coluna not in df.columns]
    if ausentes:
        raise ValueError(f"Colunas obrigatorias ausentes em {origem}: {ausentes}")


def ordenar_regioes(df: pd.DataFrame) -> pd.DataFrame:
    ordem = {regiao: indice for indice, regiao in enumerate(ORDEM_REGIOES)}
    df = df.copy()
    df["ordem"] = df["regiao"].map(ordem)

    if df["ordem"].isna().any():
        regioes_invalidas = sorted(df.loc[df["ordem"].isna(), "regiao"].unique())
        raise ValueError(f"Regioes sem ordem definida: {regioes_invalidas}")

    return df.sort_values("ordem").drop(columns=["ordem"])


def converter_numericas(df: pd.DataFrame, colunas: list[str], origem: Path) -> pd.DataFrame:
    df = df.copy()

    for coluna in colunas:
        if coluna in df.columns:
            df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    colunas_presentes = [coluna for coluna in colunas if coluna in df.columns]
    if df[colunas_presentes].isna().sum().sum() > 0:
        raise ValueError(f"Ha valores numericos invalidos em {origem}.")

    return df


def gerar_resumo_climatico_anual(df_diario: pd.DataFrame) -> pd.DataFrame:
    validar_colunas(df_diario, COLUNAS_DIARIO_OBRIGATORIAS, ARQUIVO_CLIMA_DIARIO)

    df = converter_numericas(df_diario, COLUNAS_NUMERICAS_DIARIO, ARQUIVO_CLIMA_DIARIO)
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    if df["data"].isna().any():
        raise ValueError("Ha datas invalidas na base climatica diaria tratada.")

    validacao = (
        df.groupby(["regiao", "cidade", "estado"])
        .agg(
            dias_validos=("data", "count"),
            data_inicio=("data", "min"),
            data_fim=("data", "max"),
        )
        .reset_index()
    )

    if not (validacao["dias_validos"] == 365).all():
        raise ValueError("Alguma regiao nao possui 365 registros diarios.")

    resumo = (
        df.groupby(
            [
                "regiao",
                "cidade",
                "estado",
                "latitude",
                "longitude",
                "periodo_referencia",
                "fonte_climatica",
                "fonte_climatica_url",
                "origem_dados_climaticos",
            ]
        )
        .agg(
            temperatura_media_anual_c=("temp_media", "mean"),
            temperatura_maxima_anual_c=("temp_maxima", "max"),
            temperatura_minima_anual_c=("temp_minima", "min"),
            precipitacao_total_anual_mm=("precipitacao_diaria_mm", "sum"),
            umidade_media_anual_pct=("umidade_media", "mean"),
            velocidade_vento_media_anual_m_s=("vento_medio", "mean"),
            radiacao_solar_media_anual_kwh_m2_dia=("radiacao_media", "mean"),
        )
        .reset_index()
    )

    for coluna in COLUNAS_NUMERICAS_RESUMO:
        if coluna in resumo.columns:
            resumo[coluna] = resumo[coluna].round(2)

    return ordenar_regioes(resumo)


def normalizar_resumo_climatico(df_resumo: pd.DataFrame) -> pd.DataFrame:
    renomear = {
        origem: destino
        for origem, destino in MAPA_COLUNAS_RESUMO_ATUAL.items()
        if origem in df_resumo.columns and destino not in df_resumo.columns
    }

    df = df_resumo.rename(columns=renomear).copy()

    if "fonte_climatica_url" not in df.columns:
        df["fonte_climatica_url"] = "https://power.larc.nasa.gov/"

    validar_colunas(df, COLUNAS_CLIMA_OBRIGATORIAS, ARQUIVO_CLIMA_RESUMO)
    df = converter_numericas(df, COLUNAS_NUMERICAS_RESUMO, ARQUIVO_CLIMA_RESUMO)

    return ordenar_regioes(df)


def carregar_clima() -> pd.DataFrame:
    if ARQUIVO_CLIMA_DIARIO.exists():
        df_diario = pd.read_csv(ARQUIVO_CLIMA_DIARIO)
        return gerar_resumo_climatico_anual(df_diario)

    if ARQUIVO_CLIMA_RESUMO.exists():
        df_resumo = pd.read_csv(ARQUIVO_CLIMA_RESUMO)
        return normalizar_resumo_climatico(df_resumo)

    raise FileNotFoundError(
        f"Arquivos climaticos nao encontrados:\n"
        f"- {ARQUIVO_CLIMA_DIARIO}\n"
        f"- {ARQUIVO_CLIMA_RESUMO}\n"
        "Execute antes o script 02_tratar_dados_climaticos.py."
    )


def calcular_demanda_refrigeracao(temp_media: float, temp_maxima: float) -> float:
    """
    Score simplificado de cautela para refrigeracao.
    Escala: 0 a 10. Nao representa dimensionamento termico real.
    """
    score = 0

    if temp_media >= 27:
        score += 4
    elif temp_media >= 24:
        score += 3
    elif temp_media >= 21:
        score += 2
    else:
        score += 1

    if temp_maxima >= 38:
        score += 5
    elif temp_maxima >= 35:
        score += 4
    elif temp_maxima >= 32:
        score += 3
    elif temp_maxima >= 29:
        score += 2
    else:
        score += 1

    return min(float(score), 10.0)


def calcular_potencial_pluvial(
    precipitacao_mm: float,
    area_m2: float,
    eficiencia_pct: float,
) -> float:
    eficiencia = eficiencia_pct / 100
    volume_m3_ano = (precipitacao_mm / 1000) * area_m2 * eficiencia
    return round(volume_m3_ano, 2)


def montar_regioes(df_clima: pd.DataFrame) -> pd.DataFrame:
    linhas = []

    for _, linha in df_clima.iterrows():
        regiao = linha["regiao"]

        if regiao not in PARAMETROS_REGIONAIS:
            raise ValueError(f"Regiao sem parametrizacao definida: {regiao}")

        p = PARAMETROS_REGIONAIS[regiao].copy()

        demanda_refrigeracao = calcular_demanda_refrigeracao(
            temp_media=float(linha["temperatura_media_anual_c"]),
            temp_maxima=float(linha["temperatura_maxima_anual_c"]),
        )

        potencial_pluvial_m3_ano = calcular_potencial_pluvial(
            precipitacao_mm=float(linha["precipitacao_total_anual_mm"]),
            area_m2=float(p["area_captacao_m2"]),
            eficiencia_pct=float(p["eficiencia_captacao_pct"]),
        )

        registro = {
            "regiao_id": p["regiao_id"],
            "regiao": linha["regiao"],
            "eixo_regional": p["eixo_regional"],
            "cidade": linha["cidade"],
            "estado": linha["estado"],
            "latitude": linha["latitude"],
            "longitude": linha["longitude"],
            "contexto_territorial": p["contexto_territorial"],
            "bioma_contexto": p["bioma_contexto"],
            "periodo_referencia": linha["periodo_referencia"],
            "fonte_climatica": linha["fonte_climatica"],
            "fonte_climatica_url": linha["fonte_climatica_url"],
            "temperatura_media_anual_c": linha["temperatura_media_anual_c"],
            "temperatura_maxima_anual_c": linha["temperatura_maxima_anual_c"],
            "temperatura_minima_anual_c": linha.get("temperatura_minima_anual_c"),
            "precipitacao_total_anual_mm": linha["precipitacao_total_anual_mm"],
            "umidade_media_anual_pct": linha["umidade_media_anual_pct"],
            "velocidade_vento_media_anual_m_s": linha.get("velocidade_vento_media_anual_m_s"),
            "radiacao_solar_media_anual_kwh_m2_dia": linha.get("radiacao_solar_media_anual_kwh_m2_dia"),
            "risco_hidrico_score_0_10": p["risco_hidrico_score_0_10"],
            "risco_inundacao_score_0_10": p["risco_inundacao_score_0_10"],
            "sensibilidade_territorial_score_0_10": p["sensibilidade_territorial_score_0_10"],
            "demanda_refrigeracao_score_0_10": demanda_refrigeracao,
            "area_captacao_m2": p["area_captacao_m2"],
            "capacidade_reservatorio_l": p["capacidade_reservatorio_l"],
            "consumo_agua_tecnico_m3_dia": p["consumo_agua_tecnico_m3_dia"],
            "eficiencia_captacao_pct": p["eficiencia_captacao_pct"],
            "potencial_pluvial_m3_ano": potencial_pluvial_m3_ano,
            "conectividade_critica_score_0_10": p["conectividade_critica_score_0_10"],
            "redundancia_fibra_score_0_10": p["redundancia_fibra_score_0_10"],
            "disponibilidade_energetica_score_0_10": p["disponibilidade_energetica_score_0_10"],
            "risco_rota_unica_score_0_10": p["risco_rota_unica_score_0_10"],
            "resiliencia_operacional_score_0_10": p["resiliencia_operacional_score_0_10"],
            "origem_dados_climaticos": linha["origem_dados_climaticos"],
            "origem_risco_hidrico": "parametrizado",
            "origem_risco_inundacao": "parametrizado",
            "origem_sensibilidade_territorial": "parametrizado",
            "origem_reuso_pluvial": "calculado e simulado",
            "origem_infraestrutura_digital": "parametrizado",
            "origem_demanda_refrigeracao": "calculado",
        }

        linhas.append(registro)

    return pd.DataFrame(linhas)


def salvar_relatorio(df: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    relatorio = f"""# Relatorio de Montagem do regioes.csv - Acqua Orbit DC

## Etapa executada

Integracao dos dados climaticos tratados com indicadores parametrizados, simulados e calculados da POC.

## Entrada climatica

- Preferencial: `data/nasa_power_2025_diario_tratado.csv`
- Alternativa: `data/clima_regioes_2025_tratado.csv`

## Arquivo gerado

- `data/regioes.csv`

## Regioes incluidas

{chr(10).join([f"- {row.regiao} ({row.cidade}/{row.estado})" for row in df.itertuples()])}

## Origem dos dados

- Dados climaticos: NASA POWER, origem real.
- Riscos ambientais: parametrizados para fins academicos.
- Reuso pluvial: calculado a partir da precipitacao e de area/capacidade simuladas.
- Infraestrutura critica digital: parametrizada para representar conectividade, energia, redundancia e resiliencia.
- Demanda de refrigeracao: calculada a partir da temperatura media e maxima.

## Observacao

O arquivo `regioes.csv` e a base oficial de entrada da POC. Ele nao representa laudo tecnico real, auditoria de data center, estudo profissional de telecomunicacoes ou analise energetica profissional.
"""
    ARQUIVO_RELATORIO.write_text(relatorio, encoding="utf-8")


def main() -> None:
    print("Acqua Orbit DC - Montagem do regioes.csv")

    DATA_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    df_clima = carregar_clima()
    print(f"Resumo climatico preparado: {len(df_clima)} regioes")

    df_regioes = montar_regioes(df_clima)
    print("Indicadores complementares integrados")

    df_regioes.to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8-sig")
    salvar_relatorio(df_regioes)

    print("Arquivo regioes.csv gerado com sucesso")
    print(f"- {ARQUIVO_SAIDA}")
    print(f"- {ARQUIVO_RELATORIO}")


if __name__ == "__main__":
    main()
