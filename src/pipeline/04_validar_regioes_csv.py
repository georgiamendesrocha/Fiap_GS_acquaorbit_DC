"""
Ácqua Orbit DC — Etapa 04
Validação do CSV oficial da POC: data/regioes.csv

Entrada:
    data/regioes.csv

Saída:
    output/relatorio_validacao_regioes_csv.md

Uso:
    python src/pipeline/04_validar_regioes_csv.py
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
ARQUIVO_RELATORIO = OUTPUT / "relatorio_validacao_regioes_csv.md"

REGIOES_ESPERADAS = {
    "Barueri/Tamboré",
    "Rio de Janeiro - Barra/Jacarepaguá/Parque Olímpico",
    "Curitiba",
}

ORIGENS_VALIDAS = {
    "real",
    "calculado",
    "simulado",
    "inspirado",
    "parametrizado",
    "calculado e simulado",
}

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
    "origem_dados_climaticos",
    "origem_risco_hidrico",
    "origem_risco_inundacao",
    "origem_sensibilidade_territorial",
    "origem_reuso_pluvial",
    "origem_infraestrutura_digital",
    "origem_demanda_refrigeracao",
]


def carregar_regioes() -> pd.DataFrame:
    if not ARQUIVO_REGIOES.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO_REGIOES}\n"
            "Execute antes o script 03_montar_regioes_csv.py."
        )
    return pd.read_csv(ARQUIVO_REGIOES)


def validar_colunas(df: pd.DataFrame) -> list[str]:
    erros = []
    ausentes = [col for col in COLUNAS_OBRIGATORIAS if col not in df.columns]
    if ausentes:
        erros.append(f"Colunas obrigatórias ausentes: {ausentes}")
    return erros


def validar_regioes(df: pd.DataFrame) -> list[str]:
    erros = []

    regioes_encontradas = set(df["regiao"].dropna().unique())

    if regioes_encontradas != REGIOES_ESPERADAS:
        erros.append(
            f"Regiões incorretas. Esperadas: {sorted(REGIOES_ESPERADAS)}. "
            f"Encontradas: {sorted(regioes_encontradas)}"
        )

    if len(df) != 3:
        erros.append(f"O CSV deve ter 3 linhas. Encontrado: {len(df)}")

    return erros


def validar_nulos(df: pd.DataFrame) -> list[str]:
    erros = []
    nulos = df[COLUNAS_OBRIGATORIAS].isna().sum()
    nulos = nulos[nulos > 0]

    if not nulos.empty:
        erros.append(f"Campos obrigatórios com valores nulos: {nulos.to_dict()}")

    return erros


def validar_scores(df: pd.DataFrame) -> list[str]:
    erros = []

    colunas_score = [col for col in df.columns if col.endswith("_score_0_10")]

    for coluna in colunas_score:
        valores_invalidos = df[(df[coluna] < 0) | (df[coluna] > 10)]
        if not valores_invalidos.empty:
            erros.append(f"Score fora da escala 0-10 na coluna: {coluna}")

    return erros


def validar_origens(df: pd.DataFrame) -> list[str]:
    erros = []
    colunas_origem = [col for col in df.columns if col.startswith("origem_")]

    for coluna in colunas_origem:
        valores = set(df[coluna].dropna().astype(str).unique())
        invalidos = valores - ORIGENS_VALIDAS
        if invalidos:
            erros.append(f"Valores inválidos em {coluna}: {sorted(invalidos)}")

    return erros


def gerar_relatorio(df: pd.DataFrame, erros: list[str]) -> None:
    OUTPUT.mkdir(exist_ok=True)

    status = "APROVADO" if not erros else "REPROVADO"

    linhas_regioes = []
    for row in df.itertuples():
        linhas_regioes.append(
            f"- {row.regiao} ({row.cidade}/{row.estado}) | "
            f"Lat {row.latitude} | Lon {row.longitude}"
        )

    if erros:
        bloco_erros = "\n".join([f"- {erro}" for erro in erros])
    else:
        bloco_erros = "- Nenhum erro crítico encontrado."

    relatorio = f"""# Relatório de Validação do regioes.csv — Ácqua Orbit DC

## Status

{status}

## Regiões validadas

{chr(10).join(linhas_regioes)}

## Verificações executadas

- Quantidade de regiões.
- Presença das três regiões oficiais.
- Presença das colunas obrigatórias.
- Ausência de nulos em campos obrigatórios.
- Escala dos scores entre 0 e 10.
- Valores permitidos para origem dos dados.

## Erros encontrados

{bloco_erros}
"""
    ARQUIVO_RELATORIO.write_text(relatorio, encoding="utf-8")


def main() -> None:
    print("Ácqua Orbit DC — Validação do regioes.csv")

    df = carregar_regioes()

    erros = []
    erros.extend(validar_colunas(df))

    if not erros:
        erros.extend(validar_regioes(df))
        erros.extend(validar_nulos(df))
        erros.extend(validar_scores(df))
        erros.extend(validar_origens(df))

    gerar_relatorio(df, erros)

    if erros:
        print("Validação reprovada.")
        for erro in erros:
            print(f"- {erro}")
        raise SystemExit(1)

    print("Validação aprovada.")
    print(f"Relatório: {ARQUIVO_RELATORIO}")


if __name__ == "__main__":
    main()
