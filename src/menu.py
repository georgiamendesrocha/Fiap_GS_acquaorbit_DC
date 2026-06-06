"""
Acqua Orbit DC - Menu principal da POC.

Uso:
    python menu.py
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))

from paths import DATA, MODELS, OUTPUT, ROOT  # noqa: E402

sys.path.insert(0, str(SRC))
from config.carregar_env import carregar_dotenv  # noqa: E402

carregar_dotenv()

PYTHON = sys.executable
API_DIR = SRC / "api"
PIPELINE_DIR = SRC / "pipeline"
ML_DIR = SRC / "ml"
FRONTEND_DIR = SRC / "frontend"
DASHBOARD_STREAMLIT = FRONTEND_DIR / "dashboard_streamlit.py"


@dataclass(frozen=True)
class Etapa:
    numero: int
    titulo: str
    script: Path
    opcional: bool = False
    requer_internet: bool = False


ETAPAS: list[Etapa] = [
    Etapa(1, "Extrair dados climaticos da NASA POWER", API_DIR / "nasa_power.py", opcional=True, requer_internet=True),
    Etapa(2, "Tratar dados climaticos diarios", PIPELINE_DIR / "02_tratar_dados_climaticos.py"),
    Etapa(3, "Montar CSV oficial da POC (regioes.csv)", PIPELINE_DIR / "03_montar_regioes_csv.py"),
    Etapa(4, "Validar CSV oficial", PIPELINE_DIR / "04_validar_regioes_csv.py"),
    Etapa(5, "Calcular resultados finais e sensores simulados", PIPELINE_DIR / "05_calcular_resultados_poc.py"),
    Etapa(6, "Gerar dashboard HTML", FRONTEND_DIR / "gerar_dashboard_html.py"),
    Etapa(7, "Persistir no Oracle / fallback CSV", PIPELINE_DIR / "07_persistir_oracle_csv.py"),
    Etapa(8, "Consultar resultados no Oracle", PIPELINE_DIR / "08_consultar_resultados_oracle.py", opcional=True),
]

SCRIPT_TREINAR_MODELO = ML_DIR / "treinar_modelo.py"
SCRIPT_GERAR_PDF = PIPELINE_DIR / "09_gerar_pdf_documentacao.py"


def limpar_tela() -> None:
    print("\n" * 2)


def exibir_cabecalho() -> None:
    print("=" * 62)
    print("  ACQUA ORBIT DC - Menu Principal")
    print("  Global Solution 2026.1 | FIAP | Grupo 13")
    print("=" * 62)


def exibir_menu() -> None:
    exibir_cabecalho()
    print("\nEtapas do pipeline (ordem do README):\n")

    for etapa in ETAPAS:
        sufixo = []
        if etapa.opcional:
            sufixo.append("opcional")
        if etapa.requer_internet:
            sufixo.append("requer internet")
        extra = f" ({', '.join(sufixo)})" if sufixo else ""
        status = "OK" if etapa.script.exists() else "AUSENTE"
        print(f"  [{etapa.numero}] {etapa.titulo}{extra} [{status}]")

    status_treino = "OK" if SCRIPT_TREINAR_MODELO.exists() else "AUSENTE"
    status_pdf = "OK" if SCRIPT_GERAR_PDF.exists() else "AUSENTE"

    print("\nAcoes complementares (fora do pipeline):\n")
    print(f"  [9] Treinar e salvar modelo de IA (dashboard Streamlit) [{status_treino}]")
    print(f" [10] Gerar PDF da documentacao do projeto [{status_pdf}]")

    print("\nAcoes em lote:\n")
    print("  [P] Executar pipeline completo (etapas 2 a 7)")
    print("  [N] Executar pipeline completo com NASA (etapas 1 a 7)")
    print("  [T] Treinar e salvar modelo de IA")
    print("  [D] Abrir dashboard HTML no navegador (se existir)")
    print("  [S] Iniciar dashboard Streamlit interativo")
    print("\n  [0] Sair\n")


def executar_script(script: Path) -> bool:
    if not script.exists():
        print(f"\nErro: script nao encontrado: {script}")
        return False

    print(f"\n>> Executando: {script.relative_to(ROOT)}")
    print("-" * 62)

    resultado = subprocess.run([PYTHON, str(script)], cwd=str(ROOT), check=False)

    print("-" * 62)
    if resultado.returncode == 0:
        print("Etapa concluida com sucesso.\n")
        return True

    print(f"Etapa finalizada com erro (codigo {resultado.returncode}).\n")
    return False


def executar_pipeline(incluir_nasa: bool = False) -> None:
    inicio = 1 if incluir_nasa else 2
    fim = 7
    etapas = [e for e in ETAPAS if inicio <= e.numero <= fim]

    print(f"\nIniciando pipeline: etapas {inicio} a {fim}")
    for etapa in etapas:
        if not executar_script(etapa.script):
            resposta = input("Deseja continuar mesmo com erro? (s/N): ").strip().lower()
            if resposta != "s":
                print("Pipeline interrompido pelo usuario.")
                return

    print("Pipeline completo finalizado.")
    print(f"Dashboard: {OUTPUT / 'dashboard_poc.html'}")
    print(f"Resultados: {DATA / 'resultados_regioes.csv'}")
    print("Proximo passo sugerido: opcao 9 ou T (treinar modelo IA) e opcao S (Streamlit)\n")


def treinar_modelo_ia() -> None:
    executar_script(SCRIPT_TREINAR_MODELO)


def abrir_dashboard() -> None:
    dashboard = OUTPUT / "dashboard_poc.html"
    if not dashboard.exists():
        print("\nDashboard ainda nao foi gerado. Execute a etapa 6 primeiro.\n")
        return

    print(f"\nAbrindo: {dashboard}")
    if sys.platform == "win32":
        subprocess.run(["cmd", "/c", "start", "", str(dashboard)], check=False)
    elif sys.platform == "darwin":
        subprocess.run(["open", str(dashboard)], check=False)
    else:
        subprocess.run(["xdg-open", str(dashboard)], check=False)


def iniciar_dashboard_streamlit() -> None:
    if not DASHBOARD_STREAMLIT.exists():
        print(f"\nErro: arquivo nao encontrado: {DASHBOARD_STREAMLIT}\n")
        return

    if not (DATA / "resultados_regioes.csv").exists():
        print("\nResultados ainda nao gerados. Execute a etapa 5 antes do dashboard Streamlit.\n")
        return
    print("\nIniciando dashboard Streamlit...")
    print("URL: http://localhost:8501")
    print("Pressione Ctrl+C para encerrar o servidor e voltar ao menu.\n")
    print("-" * 62)

    try:
        subprocess.run(
            [
                PYTHON, "-m", "streamlit", "run", str(DASHBOARD_STREAMLIT),
                "--server.headless", "true",
                "--browser.gatherUsageStats", "false",
            ],
            cwd=str(ROOT),
            check=False,
        )
    except KeyboardInterrupt:
        print("\nDashboard Streamlit encerrado.\n")


def processar_opcao(opcao: str) -> bool:
    opcao = opcao.strip().upper()

    if opcao == "0":
        return False
    if opcao == "P":
        executar_pipeline(incluir_nasa=False)
        return True
    if opcao == "N":
        executar_pipeline(incluir_nasa=True)
        return True
    if opcao == "D":
        abrir_dashboard()
        return True
    if opcao == "S":
        iniciar_dashboard_streamlit()
        return True
    if opcao in ("T", "9"):
        treinar_modelo_ia()
        return True
    if opcao == "10":
        executar_script(SCRIPT_GERAR_PDF)
        return True
    if opcao.isdigit():
        numero = int(opcao)
        etapa = next((e for e in ETAPAS if e.numero == numero), None)
        if etapa is None:
            print("\nOpcao invalida. Tente novamente.\n")
            return True
        executar_script(etapa.script)
        return True

    print("\nOpcao invalida. Tente novamente.\n")
    return True


def main() -> None:
    continuar = True
    while continuar:
        limpar_tela()
        exibir_menu()
        opcao = input("Escolha uma opcao: ")
        continuar = processar_opcao(opcao)


if __name__ == "__main__":
    main()
