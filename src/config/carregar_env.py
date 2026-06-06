"""
Carrega variaveis de ambiente a partir de arquivos .env do projeto.
"""

from __future__ import annotations

import os
from pathlib import Path

from paths import ROOT

CANDIDATOS_ENV = (
    ROOT / ".env",
    ROOT / ".ENV",
    ROOT.parent / ".env",
    ROOT.parent / ".ENV",
    ROOT / "config" / ".env",
    ROOT / "config" / ".ENV",
)


def _parsear_arquivo(caminho: Path) -> int:
    carregadas = 0
    conteudo = caminho.read_text(encoding="utf-8")

    for linha in conteudo.splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue

        chave, valor = linha.split("=", 1)
        chave = chave.strip()
        valor = valor.strip().strip('"').strip("'")

        if not chave:
            continue

        if chave not in os.environ or not os.environ.get(chave):
            os.environ[chave] = valor
            carregadas += 1

    return carregadas


def carregar_dotenv() -> Path | None:
    for caminho in CANDIDATOS_ENV:
        if caminho.exists():
            _parsear_arquivo(caminho)
            return caminho
    return None


def oracle_configurado() -> bool:
    return all(os.getenv(var) for var in ("ORACLE_USER", "ORACLE_PASSWORD", "ORACLE_DSN"))


def garantir_oracle_env() -> Path:
    caminho = carregar_dotenv()
    if not oracle_configurado():
        procurados = "\n".join(f"  - {p}" for p in CANDIDATOS_ENV)
        raise RuntimeError(
            "Variaveis Oracle ausentes: ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN.\n"
            f"Arquivos .env procurados:\n{procurados}\n"
            "Crie um .env na raiz do projeto ou na pasta pai com as credenciais Oracle."
        )
    return caminho or Path(".env")
