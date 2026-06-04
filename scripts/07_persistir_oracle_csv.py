"""
Acqua Orbit DC - Etapa 07
Persistencia opcional em Oracle com fallback automatico em CSV.

Entrada:
    data/resultados_regioes.csv

Saidas em fallback CSV:
    output/fallback_csv/ao_regioes.csv
    output/fallback_csv/ao_indicadores.csv
    output/fallback_csv/ao_resultados_poc.csv
    output/relatorio_persistencia_oracle_csv.md

Uso sem Oracle:
    python scripts/07_persistir_oracle_csv.py

Uso com Oracle:
    1. Execute database/01_criar_tabelas_oracle.sql no schema Oracle.
    2. Configure ORACLE_USER, ORACLE_PASSWORD e ORACLE_DSN no ambiente.
    3. Instale o pacote opcional: pip install oracledb
    4. Execute: python scripts/07_persistir_oracle_csv.py
"""

from pathlib import Path
import os
from typing import Any

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
FALLBACK_DIR = OUTPUT_DIR / "fallback_csv"

ARQUIVO_RESULTADOS = DATA_DIR / "resultados_regioes.csv"
ARQUIVO_RELATORIO = OUTPUT_DIR / "relatorio_persistencia_oracle_csv.md"

COLUNAS_REGIOES = [
    "regiao_id",
    "regiao",
    "eixo_regional",
    "cidade",
    "estado",
    "latitude",
    "longitude",
    "contexto_territorial",
    "bioma_contexto",
    "periodo_referencia",
    "fonte_climatica",
    "fonte_climatica_url",
    "origem_dados_climaticos",
]

COLUNAS_INDICADORES = [
    "regiao_id",
    "temperatura_media_anual_c",
    "temperatura_maxima_anual_c",
    "temperatura_minima_anual_c",
    "precipitacao_total_anual_mm",
    "umidade_media_anual_pct",
    "velocidade_vento_media_anual_m_s",
    "radiacao_solar_media_anual_kwh_m2_dia",
    "risco_hidrico_score_0_10",
    "risco_inundacao_score_0_10",
    "sensibilidade_territorial_score_0_10",
    "demanda_refrigeracao_score_0_10",
    "area_captacao_m2",
    "capacidade_reservatorio_l",
    "consumo_agua_tecnico_m3_dia",
    "eficiencia_captacao_pct",
    "potencial_pluvial_m3_ano",
    "conectividade_critica_score_0_10",
    "redundancia_fibra_score_0_10",
    "disponibilidade_energetica_score_0_10",
    "risco_rota_unica_score_0_10",
    "resiliencia_operacional_score_0_10",
    "origem_risco_hidrico",
    "origem_risco_inundacao",
    "origem_sensibilidade_territorial",
    "origem_reuso_pluvial",
    "origem_infraestrutura_digital",
    "origem_demanda_refrigeracao",
]

COLUNAS_RESULTADOS = [
    "regiao_id",
    "nivel_reservatorio_pct",
    "ph_agua",
    "turbidez_ntu",
    "condutividade_us_cm",
    "temperatura_agua_c",
    "classificacao_qualidade_agua",
    "indicador_geoespacial_score_0_10",
    "risco_ambiental_climatico_score_0_10",
    "ambiental_favoravel_score_0_10",
    "cobertura_reuso_pluvial_pct",
    "indice_potencial_reuso_pluvial_score_0_10",
    "indice_qualidade_agua_score_0_10",
    "indice_conectividade_critica_score_0_10",
    "indice_disponibilidade_energetica_score_0_10",
    "indice_refrigeracao_risco_termico_score_0_10",
    "indice_esg_resiliencia_score_0_10",
    "score_final_poc_0_10",
    "classificacao_final",
    "parecer_apoio_decisao",
    "origem_sensores_agua",
    "origem_indicadores_finais",
    "origem_classificacao_final",
]

MAPA_REGIOES = {
    "REGIAO_ID": "regiao_id",
    "REGIAO": "regiao",
    "EIXO_REGIONAL": "eixo_regional",
    "CIDADE": "cidade",
    "ESTADO": "estado",
    "LATITUDE": "latitude",
    "LONGITUDE": "longitude",
    "CONTEXTO_TERRITORIAL": "contexto_territorial",
    "BIOMA_CONTEXTO": "bioma_contexto",
    "PERIODO_REFERENCIA": "periodo_referencia",
    "FONTE_CLIMATICA": "fonte_climatica",
    "FONTE_CLIMATICA_URL": "fonte_climatica_url",
    "ORIGEM_DADOS_CLIMATICOS": "origem_dados_climaticos",
}

MAPA_INDICADORES = {
    "REGIAO_ID": "regiao_id",
    "TEMP_MEDIA_ANUAL_C": "temperatura_media_anual_c",
    "TEMP_MAXIMA_ANUAL_C": "temperatura_maxima_anual_c",
    "TEMP_MINIMA_ANUAL_C": "temperatura_minima_anual_c",
    "PRECIP_TOTAL_ANUAL_MM": "precipitacao_total_anual_mm",
    "UMIDADE_MEDIA_ANUAL_PCT": "umidade_media_anual_pct",
    "VENTO_MEDIO_ANUAL_M_S": "velocidade_vento_media_anual_m_s",
    "RADIACAO_SOLAR_MEDIA": "radiacao_solar_media_anual_kwh_m2_dia",
    "RISCO_HIDRICO_SCORE": "risco_hidrico_score_0_10",
    "RISCO_INUNDACAO_SCORE": "risco_inundacao_score_0_10",
    "SENSIBILIDADE_SCORE": "sensibilidade_territorial_score_0_10",
    "DEMANDA_REFRIG_SCORE": "demanda_refrigeracao_score_0_10",
    "AREA_CAPTACAO_M2": "area_captacao_m2",
    "CAPACIDADE_RESERVATORIO_L": "capacidade_reservatorio_l",
    "CONSUMO_AGUA_M3_DIA": "consumo_agua_tecnico_m3_dia",
    "EFICIENCIA_CAPTACAO_PCT": "eficiencia_captacao_pct",
    "POTENCIAL_PLUVIAL_M3_ANO": "potencial_pluvial_m3_ano",
    "CONECTIVIDADE_SCORE": "conectividade_critica_score_0_10",
    "REDUNDANCIA_SCORE": "redundancia_fibra_score_0_10",
    "ENERGIA_SCORE": "disponibilidade_energetica_score_0_10",
    "RISCO_ROTA_UNICA_SCORE": "risco_rota_unica_score_0_10",
    "RESILIENCIA_SCORE": "resiliencia_operacional_score_0_10",
    "ORIGEM_RISCO_HIDRICO": "origem_risco_hidrico",
    "ORIGEM_RISCO_INUNDACAO": "origem_risco_inundacao",
    "ORIGEM_SENSIBILIDADE": "origem_sensibilidade_territorial",
    "ORIGEM_REUSO_PLUVIAL": "origem_reuso_pluvial",
    "ORIGEM_INFRA_DIGITAL": "origem_infraestrutura_digital",
    "ORIGEM_DEMANDA_REFRIG": "origem_demanda_refrigeracao",
}

MAPA_RESULTADOS = {
    "REGIAO_ID": "regiao_id",
    "NIVEL_RESERVATORIO_PCT": "nivel_reservatorio_pct",
    "PH_AGUA": "ph_agua",
    "TURBIDEZ_NTU": "turbidez_ntu",
    "CONDUTIVIDADE_US_CM": "condutividade_us_cm",
    "TEMP_AGUA_C": "temperatura_agua_c",
    "CLASS_QUALIDADE_AGUA": "classificacao_qualidade_agua",
    "IND_GEO_SCORE": "indicador_geoespacial_score_0_10",
    "RISCO_AMB_CLIM_SCORE": "risco_ambiental_climatico_score_0_10",
    "AMBIENTAL_FAVORAVEL_SCORE": "ambiental_favoravel_score_0_10",
    "COBERTURA_REUSO_PCT": "cobertura_reuso_pluvial_pct",
    "POTENCIAL_REUSO_SCORE": "indice_potencial_reuso_pluvial_score_0_10",
    "QUALIDADE_AGUA_SCORE": "indice_qualidade_agua_score_0_10",
    "IND_CONECTIVIDADE_SCORE": "indice_conectividade_critica_score_0_10",
    "IND_DISP_ENERGETICA_SCORE": "indice_disponibilidade_energetica_score_0_10",
    "IND_REFRIG_RISCO_TERMICO": "indice_refrigeracao_risco_termico_score_0_10",
    "ESG_RESILIENCIA_SCORE": "indice_esg_resiliencia_score_0_10",
    "SCORE_FINAL": "score_final_poc_0_10",
    "CLASS_FINAL": "classificacao_final",
    "PARECER_APOIO": "parecer_apoio_decisao",
    "ORIGEM_SENSORES_AGUA": "origem_sensores_agua",
    "ORIGEM_INDICADORES_FINAIS": "origem_indicadores_finais",
    "ORIGEM_CLASSIFICACAO_FINAL": "origem_classificacao_final",
}


def carregar_resultados() -> pd.DataFrame:
    if not ARQUIVO_RESULTADOS.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {ARQUIVO_RESULTADOS}\n"
            "Execute antes o script 05_calcular_resultados_poc.py."
        )

    df = pd.read_csv(ARQUIVO_RESULTADOS)
    colunas_obrigatorias = COLUNAS_REGIOES + COLUNAS_INDICADORES + COLUNAS_RESULTADOS
    ausentes = [coluna for coluna in colunas_obrigatorias if coluna not in df.columns]

    if ausentes:
        raise ValueError(f"Colunas obrigatorias ausentes em resultados_regioes.csv: {ausentes}")

    return df


def oracle_configurado() -> bool:
    return all(
        os.getenv(variavel)
        for variavel in ["ORACLE_USER", "ORACLE_PASSWORD", "ORACLE_DSN"]
    )


def valor_limpo(valor: Any) -> Any:
    if pd.isna(valor):
        return None
    if hasattr(valor, "item"):
        try:
            return valor.item()
        except (AttributeError, ValueError):
            return valor
    return valor


def binds(row: pd.Series, mapa: dict[str, str]) -> dict[str, Any]:
    return {
        destino: valor_limpo(row[origem])
        for destino, origem in mapa.items()
    }


def salvar_fallback_csv(df: pd.DataFrame, motivo: str) -> str:
    FALLBACK_DIR.mkdir(parents=True, exist_ok=True)

    df[COLUNAS_REGIOES].to_csv(
        FALLBACK_DIR / "ao_regioes.csv",
        index=False,
        encoding="utf-8-sig",
    )
    df[COLUNAS_INDICADORES].to_csv(
        FALLBACK_DIR / "ao_indicadores.csv",
        index=False,
        encoding="utf-8-sig",
    )
    df[COLUNAS_RESULTADOS].to_csv(
        FALLBACK_DIR / "ao_resultados_poc.csv",
        index=False,
        encoding="utf-8-sig",
    )

    salvar_relatorio(
        modo="CSV fallback",
        registros=len(df),
        detalhe=motivo,
    )

    return "CSV fallback"


def executar_merge(cursor: Any, sql: str, parametros: dict[str, Any]) -> None:
    cursor.execute(sql, parametros)


def gerar_merge(tabela: str, mapa: dict[str, str], pk: str = "REGIAO_ID") -> str:
    colunas = list(mapa.keys())
    colunas_update = [coluna for coluna in colunas if coluna != pk]

    update_set = ",\n            ".join(
        f"t.{coluna} = :{coluna}"
        for coluna in colunas_update
    )
    insert_cols = ", ".join(colunas)
    insert_vals = ", ".join(f":{coluna}" for coluna in colunas)

    return f"""
        MERGE INTO {tabela} t
        USING (SELECT :{pk} AS {pk} FROM dual) s
        ON (t.{pk} = s.{pk})
        WHEN MATCHED THEN UPDATE SET
            {update_set}
        WHEN NOT MATCHED THEN INSERT ({insert_cols})
        VALUES ({insert_vals})
    """


def persistir_oracle(df: pd.DataFrame) -> str:
    try:
        import oracledb  # type: ignore
    except ImportError:
        return salvar_fallback_csv(
            df,
            "Pacote opcional 'oracledb' nao instalado.",
        )

    merge_regioes = gerar_merge("AO_REGIOES", MAPA_REGIOES)
    merge_indicadores = gerar_merge("AO_INDICADORES", MAPA_INDICADORES)
    merge_resultados = gerar_merge("AO_RESULTADOS_POC", MAPA_RESULTADOS)

    try:
        with oracledb.connect(
            user=os.environ["ORACLE_USER"],
            password=os.environ["ORACLE_PASSWORD"],
            dsn=os.environ["ORACLE_DSN"],
        ) as connection:
            with connection.cursor() as cursor:
                for _, row in df.iterrows():
                    executar_merge(cursor, merge_regioes, binds(row, MAPA_REGIOES))
                    executar_merge(cursor, merge_indicadores, binds(row, MAPA_INDICADORES))
                    executar_merge(cursor, merge_resultados, binds(row, MAPA_RESULTADOS))

            connection.commit()

    except Exception as erro:
        return salvar_fallback_csv(
            df,
            f"Oracle indisponivel ou nao configurado corretamente: {erro}",
        )

    salvar_relatorio(
        modo="Oracle",
        registros=len(df),
        detalhe="Dados persistidos nas tabelas AO_REGIOES, AO_INDICADORES e AO_RESULTADOS_POC.",
    )
    return "Oracle"


def salvar_relatorio(modo: str, registros: int, detalhe: str) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    relatorio = f"""# Relatorio de Persistencia Oracle/CSV - Acqua Orbit DC

## Etapa executada

Persistencia dos resultados finais da POC em Oracle opcional, com fallback automatico em CSV.

## Modo utilizado

{modo}

## Registros processados

{registros}

## Detalhe

{detalhe}

## Estrutura logica

- `AO_REGIOES`: dados cadastrais e geograficos das regioes.
- `AO_INDICADORES`: indicadores climaticos, ambientais e de infraestrutura.
- `AO_RESULTADOS_POC`: sensores simulados, indices finais e classificacao.

## Apoio Oracle

- `database/01_criar_tabelas_oracle.sql`: cria ou recria as tabelas Oracle.
- `database/02_consultas_oracle.sql`: consultas para validacao e demonstracao.
- `database/03_modelagem_dados.md`: documentacao da modelagem e tipagem.

## Fallback CSV

Quando Oracle nao esta configurado ou indisponivel, os dados sao salvos em:

- `output/fallback_csv/ao_regioes.csv`
- `output/fallback_csv/ao_indicadores.csv`
- `output/fallback_csv/ao_resultados_poc.csv`
"""
    ARQUIVO_RELATORIO.write_text(relatorio, encoding="utf-8")


def main() -> None:
    print("Acqua Orbit DC - Persistencia Oracle opcional / CSV fallback")

    df = carregar_resultados()
    print(f"Resultados carregados: {len(df)} regioes")

    if oracle_configurado():
        modo = persistir_oracle(df)
    else:
        modo = salvar_fallback_csv(
            df,
            "Variaveis ORACLE_USER, ORACLE_PASSWORD e ORACLE_DSN nao configuradas.",
        )

    print(f"Persistencia concluida em modo: {modo}")
    print(f"- {ARQUIVO_RELATORIO}")

    if modo == "CSV fallback":
        print(f"- {FALLBACK_DIR / 'ao_regioes.csv'}")
        print(f"- {FALLBACK_DIR / 'ao_indicadores.csv'}")
        print(f"- {FALLBACK_DIR / 'ao_resultados_poc.csv'}")


if __name__ == "__main__":
    main()
