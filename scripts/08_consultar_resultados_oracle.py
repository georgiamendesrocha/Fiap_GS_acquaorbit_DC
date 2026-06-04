"""
Acqua Orbit DC - Consulta simples dos resultados persistidos no Oracle.

Pre-requisito:
    ORACLE_USER, ORACLE_PASSWORD e ORACLE_DSN carregados no terminal.

Uso:
    python scripts/08_consultar_resultados_oracle.py
"""

import os


SQL_RANKING = """
SELECT
    r.CIDADE,
    r.ESTADO,
    p.SCORE_FINAL,
    p.CLASS_FINAL
FROM AO_REGIOES r
JOIN AO_RESULTADOS_POC p
    ON p.REGIAO_ID = r.REGIAO_ID
ORDER BY p.SCORE_FINAL DESC
"""


def validar_variaveis() -> None:
    ausentes = [
        variavel
        for variavel in ["ORACLE_USER", "ORACLE_PASSWORD", "ORACLE_DSN"]
        if not os.getenv(variavel)
    ]

    if ausentes:
        raise RuntimeError(
            "Variaveis Oracle ausentes: "
            f"{', '.join(ausentes)}. Carregue o .env antes de executar."
        )


def main() -> None:
    validar_variaveis()

    try:
        import oracledb  # type: ignore
    except ImportError as erro:
        raise RuntimeError(
            "Pacote 'oracledb' nao instalado. Execute: pip install oracledb"
        ) from erro

    with oracledb.connect(
        user=os.environ["ORACLE_USER"],
        password=os.environ["ORACLE_PASSWORD"],
        dsn=os.environ["ORACLE_DSN"],
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(SQL_RANKING)
            linhas = cursor.fetchall()

    print("Ranking Oracle - Acqua Orbit DC")
    print("--------------------------------")

    for cidade, estado, score, classificacao in linhas:
        print(f"{cidade} / {estado} | score {score} | {classificacao}")


if __name__ == "__main__":
    main()
