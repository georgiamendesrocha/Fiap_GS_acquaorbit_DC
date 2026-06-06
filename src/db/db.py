"""
Camada centralizada de acesso ao Oracle com oracledb.

Responsavel por:
- carregar credenciais do .env
- abrir conexoes
- garantir estrutura das tabelas da POC
- executar consultas reutilizaveis
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC if (_SRC / "paths.py").exists() else _SRC.parent))
from paths import DATA, DOCUMENT, MODELS, OUTPUT, ROOT, SCRIPTS_DB, SRC, ASSETS  # noqa: E402

import os
from pathlib import Path
from typing import Any

from config.carregar_env import carregar_dotenv, garantir_oracle_env, oracle_configurado

SQL_CRIAR_TABELAS = SCRIPTS_DB / "01_criar_tabelas_oracle.sql"

TABELAS_POC = ("AO_REGIOES", "AO_INDICADORES", "AO_RESULTADOS_POC")

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


def _importar_oracledb():
    try:
        import oracledb  # type: ignore
    except ImportError as erro:
        raise RuntimeError(
            "Pacote 'oracledb' nao instalado. Execute: pip install oracledb"
        ) from erro
    return oracledb


def inicializar_credenciais() -> Path:
    caminho = garantir_oracle_env()
    return caminho


def conectar():
    inicializar_credenciais()
    oracledb = _importar_oracledb()
    return oracledb.connect(
        user=os.environ["ORACLE_USER"],
        password=os.environ["ORACLE_PASSWORD"],
        dsn=os.environ["ORACLE_DSN"],
    )


def _normalizar_statement(texto: str) -> str:
    texto = texto.strip()
    if texto.upper().startswith("CREATE TABLE") and texto.endswith(";"):
        texto = texto[:-1].rstrip()
    return texto


def _finalizar_buffer(buffer: list[str], statements: list[str]) -> None:
    if not buffer:
        return
    texto = _normalizar_statement("\n".join(buffer))
    if texto:
        statements.append(texto)
    buffer.clear()


def _dividir_sql(conteudo: str) -> list[str]:
    statements: list[str] = []
    buffer: list[str] = []

    for linha in conteudo.splitlines():
        texto_linha = linha.strip()
        if texto_linha.startswith("--"):
            continue
        if texto_linha == "/":
            _finalizar_buffer(buffer, statements)
            continue
        if texto_linha.upper().startswith("CREATE TABLE") and buffer:
            _finalizar_buffer(buffer, statements)
        buffer.append(linha)

    _finalizar_buffer(buffer, statements)
    return statements


def tabela_existe(connection, nome_tabela: str) -> bool:
    sql = """
        SELECT COUNT(*)
        FROM USER_TABLES
        WHERE TABLE_NAME = :nome
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, {"nome": nome_tabela.upper()})
        quantidade = cursor.fetchone()[0]
    return int(quantidade) > 0


def estrutura_pronta(connection) -> bool:
    return all(tabela_existe(connection, tabela) for tabela in TABELAS_POC)


def criar_tabelas() -> None:
    if not SQL_CRIAR_TABELAS.exists():
        raise FileNotFoundError(f"Script SQL nao encontrado: {SQL_CRIAR_TABELAS}")

    statements = _dividir_sql(SQL_CRIAR_TABELAS.read_text(encoding="utf-8"))
    with conectar() as connection:
        with connection.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)
        connection.commit()


def garantir_estrutura() -> str:
    with conectar() as connection:
        if estrutura_pronta(connection):
            return "Estrutura Oracle ja existente."

    criar_tabelas()
    return "Estrutura Oracle criada a partir de scripts/database/01_criar_tabelas_oracle.sql"


def executar_sql(sql: str, parametros: dict[str, Any] | None = None) -> list[tuple]:
    with conectar() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or {})
            return cursor.fetchall()


def consultar_ranking() -> list[tuple]:
    return executar_sql(SQL_RANKING)


def oracle_disponivel() -> bool:
    carregar_dotenv()
    return oracle_configurado()
