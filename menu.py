"""
Atalho na raiz — menu interativo do projeto.

Uso:
    python menu.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MENU = ROOT / "src" / "menu.py"

_spec = importlib.util.spec_from_file_location("acqua_menu", MENU)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"Menu não encontrado: {MENU}")

_mod = importlib.util.module_from_spec(_spec)
sys.modules["acqua_menu"] = _mod
_spec.loader.exec_module(_mod)

if __name__ == "__main__":
    _mod.main()
