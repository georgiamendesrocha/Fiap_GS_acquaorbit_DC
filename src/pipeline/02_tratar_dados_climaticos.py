"""
Acqua Orbit DC - Etapa 02
Tratamento e validacao dos dados climaticos diarios NASA POWER.

Entrada esperada:
    data/nasa_power_2025_diario.csv

Saidas geradas:
    data/nasa_power_2025_diario_tratado.csv
    output/relatorio_tratamento_dados_climaticos.md

Uso:
    python src/pipeline/02_tratar_dados_climaticos.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC if (_SRC / "paths.py").exists() else _SRC.parent))
from paths import DATA, DOCUMENT, MODELS, OUTPUT, ROOT, SCRIPTS_DB, SRC, ASSETS  # noqa: E402

from pathlib import Path

import pandas as pd



ARQUIVO_ENTRADA = DATA / "nasa_power_2025_diario.csv"
ARQUIVO_REFERENCIA_CABECALHO = DATA / "clima_regioes_2025_tratado.csv"

ARQUIVO_DIARIO_TRATADO = DATA / "nasa_power_2025_diario_tratado.csv"
ARQUIVO_RELATORIO = OUTPUT / "relatorio_tratamento_dados_climaticos.md"


ORDEM_REGIOES = [
    "Barueri/Tamboré",
    "Rio de Janeiro - Barra/Jacarepaguá/Parque Olímpico",
    "Curitiba",
]

CABECALHOS_DIARIOS = {
    "T2M": "temp_media",
    "T2M_MAX": "temp_maxima",
    "T2M_MIN": "temp_minima",
    "PRECTOTCORR": "precipitacao_diaria_mm",
    "RH2M": "umidade_media",
    "WS2M": "vento_medio",
    "ALLSKY_SFC_SW_DWN": "radiacao_media",
}

COLUNAS_REFERENCIA_IGNORADAS = {
    "dias_validos",
    "data_inicio",
    "data_fim",
}

COLUNAS_REFERENCIA_AJUSTADAS = {
    "precipitacao_anual_mm": "precipitacao_diaria_mm",
}

COLUNAS_DIARIO_PADRAO = [
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

COLUNAS_CLIMATICAS_VALIDACAO = [
    "temp_media",
    "temp_maxima",
    "temp_minima",
    "precipitacao_diaria_mm",
    "umidade_media",
    "vento_medio",
    "radiacao_media",
]


def carregar_base() -> pd.DataFrame:
    if not ARQUIVO_ENTRADA.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {ARQUIVO_ENTRADA}\n"
            "Execute primeiro o script de extracao NASA POWER."
        )

    return pd.read_csv(ARQUIVO_ENTRADA)


def carregar_cabecalho_referencia() -> list[str]:
    if not ARQUIVO_REFERENCIA_CABECALHO.exists():
        return []

    return list(pd.read_csv(ARQUIVO_REFERENCIA_CABECALHO, nrows=0).columns)


def montar_colunas_diario(cabecalho_referencia: list[str]) -> list[str]:
    if not cabecalho_referencia:
        return ["data", *COLUNAS_DIARIO_PADRAO]

    colunas = ["data"]

    for coluna in cabecalho_referencia:
        if coluna in COLUNAS_REFERENCIA_IGNORADAS:
            continue

        colunas.append(COLUNAS_REFERENCIA_AJUSTADAS.get(coluna, coluna))

    return colunas


def tratar_base_diaria(
    df: pd.DataFrame,
    cabecalho_referencia: list[str],
) -> pd.DataFrame:
    df = df.copy()

    df["data"] = pd.to_datetime(
        df["data"].astype(str),
        format="%Y%m%d",
        errors="coerce",
    )

    if df["data"].isna().any():
        raise ValueError("Ha datas invalidas na base climatica diaria.")

    ordem = {regiao: indice for indice, regiao in enumerate(ORDEM_REGIOES)}
    df["ordem"] = df["regiao"].map(ordem)

    if df["ordem"].isna().any():
        regioes_invalidas = sorted(df.loc[df["ordem"].isna(), "regiao"].unique())
        raise ValueError(f"Ha regioes sem ordem definida: {regioes_invalidas}")

    df = df.sort_values(["ordem", "data"]).drop(columns=["ordem"])
    df["data"] = df["data"].dt.strftime("%Y-%m-%d")

    colunas_numericas = [
        "T2M",
        "T2M_MAX",
        "T2M_MIN",
        "PRECTOTCORR",
        "RH2M",
        "WS2M",
        "ALLSKY_SFC_SW_DWN",
        "latitude",
        "longitude",
    ]

    for coluna in colunas_numericas:
        if coluna in df.columns:
            df[coluna] = pd.to_numeric(df[coluna], errors="coerce").round(2)

    df = df.rename(columns=CABECALHOS_DIARIOS)
    df["periodo_referencia"] = "2025"
    df["fonte_climatica"] = "NASA POWER"
    df["fonte_climatica_url"] = "https://power.larc.nasa.gov/"
    df["origem_dados_climaticos"] = "real"

    colunas_diario = montar_colunas_diario(cabecalho_referencia)
    return df[colunas_diario]


def validar_base_diaria(df: pd.DataFrame) -> pd.DataFrame:
    validacao = (
        df.groupby(["regiao", "cidade", "estado"])
        .agg(
            data_inicio=("data", "min"),
            data_fim=("data", "max"),
            dias_validos=("data", "count"),
            faltantes_temp_media=("temp_media", lambda x: x.isna().sum()),
            faltantes_temp_maxima=("temp_maxima", lambda x: x.isna().sum()),
            faltantes_precipitacao_diaria_mm=(
                "precipitacao_diaria_mm",
                lambda x: x.isna().sum(),
            ),
            faltantes_umidade_media=("umidade_media", lambda x: x.isna().sum()),
        )
        .reset_index()
    )

    if not (validacao["dias_validos"] == 365).all():
        raise ValueError("Alguma regiao nao possui 365 registros diarios.")

    if df[COLUNAS_CLIMATICAS_VALIDACAO].isna().sum().sum() > 0:
        raise ValueError("Ha dados faltantes nas variaveis climaticas principais.")

    return validacao


def salvar_resultados(
    df_diario: pd.DataFrame,
    validacao: pd.DataFrame,
    cabecalho_referencia: list[str],
) -> None:
    DATA.mkdir(exist_ok=True)
    OUTPUT.mkdir(exist_ok=True)

    df_diario.to_csv(ARQUIVO_DIARIO_TRATADO, index=False, encoding="utf-8-sig")

    colunas_referencia = ", ".join(cabecalho_referencia) or "arquivo de referencia nao encontrado"
    colunas_diario = ", ".join(df_diario.columns)

    relatorio = f"""# Relatorio de Tratamento dos Dados Climaticos - Acqua Orbit DC

## Etapa executada

Tratamento e validacao dos dados climaticos diarios extraidos da NASA POWER para o periodo de 2025.

## Arquivos gerados

- `data/nasa_power_2025_diario_tratado.csv`
- `output/relatorio_tratamento_dados_climaticos.md`

## Cabecalho

O cabecalho do diario tratado foi padronizado com nomes interpretaveis, usando `data/clima_regioes_2025_tratado.csv` como referencia de nomenclatura.

Colunas de referencia:
`{colunas_referencia}`

Colunas do diario tratado:
`{colunas_diario}`

## Validacao

- Total de registros tratados: {len(df_diario)}
- Total de regioes validadas: {len(validacao)}
- Dias esperados por regiao: 365
- Data inicial: {df_diario["data"].min()}
- Data final: {df_diario["data"].max()}
- Dados faltantes nas variaveis climaticas principais: 0
- Fonte climatica: NASA POWER
- Periodo de referencia: 2025
- Origem dos dados climaticos: real

## Resultado

Dados climaticos diarios tratados, validados e prontos para uso na POC.
"""
    ARQUIVO_RELATORIO.write_text(relatorio, encoding="utf-8")


def main() -> None:
    print("Acqua Orbit DC - Tratamento dos dados climaticos diarios")

    cabecalho_referencia = carregar_cabecalho_referencia()
    df_original = carregar_base()
    print(f"Base carregada: {len(df_original)} registros")

    df_diario = tratar_base_diaria(df_original, cabecalho_referencia)
    print("Base diaria tratada com cabecalho interpretavel")

    validacao = validar_base_diaria(df_diario)
    print("Validacao concluida")

    salvar_resultados(df_diario, validacao, cabecalho_referencia)
    print("Arquivos salvos com sucesso")

    print("\nSaidas:")
    print(f"- {ARQUIVO_DIARIO_TRATADO}")
    print(f"- {ARQUIVO_RELATORIO}")


if __name__ == "__main__":
    main()
