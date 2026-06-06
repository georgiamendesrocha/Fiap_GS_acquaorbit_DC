"""
Acqua Orbit DC - Etapa 09
Gera PDF de entrega da Global Solution.

Estrutura (sem repeticao de conteudo):
  1. Capa com logo FIAP
  2. Indice
  3. Documento academico (ai_project_document_fiap.md)
  4. Resultados da ultima execucao (CSV)
  5. Evidencias visuais (4 capturas essenciais)
  6. Modelo de IA (resumo, se existir)
  7. Anexo - trechos de codigo
  8. Links para entrega

Saida: src/output/acqua_orbit_dc_documentacao.pdf

Uso:
    python src/pipeline/09_gerar_pdf_documentacao.py
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC if (_SRC / "paths.py").exists() else _SRC.parent))
from paths import DATA, DOCUMENT, MODELS, OUTPUT, ROOT, SCRIPTS_DB, SRC, ASSETS  # noqa: E402

sys.path.insert(0, str(_SRC))
from pdf_gerar_capturas import gerar_capturas_pdf  # noqa: E402

from fpdf import FPDF

LINK_REPOSITORIO = "https://github.com/georgiamendesrocha/Fiap_GS_acquaorbit_DC"
ARQUIVO_PDF = OUTPUT / "acqua_orbit_dc_documentacao.pdf"
ARQUIVO_RESULTADOS = DATA / "resultados_regioes.csv"
ARQUIVO_MODELO_META = MODELS / "score_regiao_metadata.json"
ARQUIVO_DOCUMENTO_GS = DOCUMENT / "ai_project_document_fiap.md"
LOGO_FIAP = ASSETS / "logo-fiap.png"

INTEGRANTES = [
    "Edemir Sufiatti - RM571375",
    "Carlos Magnus Costa Amaral - RM573978",
    "Georgia Mendes Rocha - RM573281",
    "Marina Leme Soares - RM570461",
    "Jocasta de Kacia Bortolacci - RM564730",
]

TRECHOS_CODIGO: list[tuple[str, Path, list[str]]] = [
    (
        "Simulacao de sensores e classificacao final",
        SRC / "pipeline" / "05_calcular_resultados_poc.py",
        ["simular_sensores_agua", "classificar_regiao"],
    ),
    (
        "Consulta a API NASA POWER",
        SRC / "api" / "nasa_power.py",
        ["consultar_nasa_power"],
    ),
]

FONT_DIR = ASSETS / "fonts"
FAMILIA_FONTE = "Projeto"

_EMOJI_RE = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE,
)

_CORRIGIR_PATHS = [
    ("`data/", "`src/data/"),
    ("`output/", "`src/output/"),
    ("`models/", "`src/models/"),
    ("scripts\\06_gerar_visualizacoes.py", "src\\frontend\\gerar_dashboard_html.py"),
    ("scripts/06_gerar_visualizacoes.py", "src/frontend/gerar_dashboard_html.py"),
    ("scripts\\10_treinar_modelo_ia.py", "src\\ml\\treinar_modelo.py"),
    ("scripts/10_treinar_modelo_ia.py", "src/ml/treinar_modelo.py"),
    ("data/resultados_regioes.csv", "src/data/resultados_regioes.csv"),
    ("data/regioes.csv", "src/data/regioes.csv"),
    ("data/nasa_power_2025_diario_tratado.csv", "src/data/nasa_power_2025_diario_tratado.csv"),
    ("output/dashboard_poc.html", "src/output/dashboard_poc.html"),
    ("output/fallback_csv", "src/output/fallback_csv"),
]


def _sem_emojis(texto: str) -> str:
    return _EMOJI_RE.sub("", texto)


def _limpar_html_markdown(texto: str) -> str:
    texto = _sem_emojis(texto)
    texto = re.sub(r"<img[^>]*>", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"<p[^>]*>", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"</p>", "\n", texto, flags=re.IGNORECASE)
    texto = re.sub(r"<br\s*/?>", "\n", texto, flags=re.IGNORECASE)
    texto = re.sub(r"<a [^>]+>", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"</a>", "", texto, flags=re.IGNORECASE)
    return texto


def _atualizar_paths(texto: str) -> str:
    for antigo, novo in _CORRIGIR_PATHS:
        texto = texto.replace(antigo, novo)
    return texto


def _preparar_documento_gs(conteudo: str) -> str:
    texto = _limpar_html_markdown(conteudo)
    texto = _atualizar_paths(texto)
    marcador = "## 1. Introducao"
    if marcador in texto:
        texto = texto[texto.index(marcador) :]
    return texto


def resolver_fontes() -> dict[str, Path]:
    candidatos = [
        {
            "": FONT_DIR / "DejaVuSans.ttf",
            "B": FONT_DIR / "DejaVuSans-Bold.ttf",
            "I": FONT_DIR / "DejaVuSans-Oblique.ttf",
            "BI": FONT_DIR / "DejaVuSans-BoldOblique.ttf",
        },
        {
            "": Path("C:/Windows/Fonts/arial.ttf"),
            "B": Path("C:/Windows/Fonts/arialbd.ttf"),
            "I": Path("C:/Windows/Fonts/ariali.ttf"),
            "BI": Path("C:/Windows/Fonts/arialbi.ttf"),
        },
        {
            "": Path("C:/Windows/Fonts/segoeui.ttf"),
            "B": Path("C:/Windows/Fonts/segoeuib.ttf"),
            "I": Path("C:/Windows/Fonts/segoeuii.ttf"),
            "BI": Path("C:/Windows/Fonts/segoeuiz.ttf"),
        },
    ]
    for grupo in candidatos:
        if all(caminho.exists() for caminho in grupo.values()):
            return grupo
    raise FileNotFoundError(
        "Nenhuma fonte Unicode encontrada. Esperado DejaVu em assets/fonts "
        "ou fontes Arial/Segoe UI no Windows."
    )


def extrair_funcoes(caminho: Path, nomes: list[str]) -> str:
    if not caminho.exists():
        return ""
    linhas = caminho.read_text(encoding="utf-8").splitlines()
    blocos: list[str] = []
    for nome in nomes:
        inicio = next((i for i, ln in enumerate(linhas) if ln.startswith(f"def {nome}(")), None)
        if inicio is None:
            continue
        fim = len(linhas)
        for j in range(inicio + 1, len(linhas)):
            if linhas[j].startswith("def ") and not linhas[j].startswith("def _"):
                fim = j
                break
        blocos.append("\n".join(linhas[inicio:fim]).strip())
    return "\n\n".join(blocos)


class DocumentacaoPDF(FPDF):
    def __init__(self) -> None:
        super().__init__(format="A4", unit="mm")
        self.set_auto_page_break(auto=True, margin=18)
        for estilo, caminho in resolver_fontes().items():
            self.add_font(FAMILIA_FONTE, estilo, str(caminho))

    def footer(self) -> None:
        self.set_y(-12)
        self.set_font(FAMILIA_FONTE, "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, f"Acqua Orbit DC - Grupo 13 | Pagina {self.page_no()}", align="C")

    def largura_util(self) -> float:
        return self.w - self.l_margin - self.r_margin

    def nova_secao(self, titulo: str) -> None:
        self.add_page()
        self.set_x(self.l_margin)
        self.set_font(FAMILIA_FONTE, "B", 16)
        self.set_text_color(15, 90, 110)
        self.multi_cell(self.largura_util(), 9, titulo)
        self.ln(2)
        self.set_draw_color(15, 90, 110)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(5)
        self.set_text_color(30, 30, 30)

    def paragrafo(self, texto: str, estilo: str = "", tamanho: int = 10) -> None:
        if not texto.strip():
            self.ln(3)
            return
        self.set_x(self.l_margin)
        self.set_font(FAMILIA_FONTE, estilo, tamanho)
        self.multi_cell(self.largura_util(), 5.5, texto.replace("\t", "    "))

    def item_lista(self, texto: str) -> None:
        self.paragrafo(f"- {texto.lstrip('- ').strip()}")

    def capa(self) -> None:
        self.add_page()
        if LOGO_FIAP.exists():
            largura_logo = 50
            self.image(str(LOGO_FIAP), x=(self.w - largura_logo) / 2, y=14, w=largura_logo)
            self.set_y(58)
        else:
            self.set_y(30)

        self.set_font(FAMILIA_FONTE, "B", 22)
        self.set_text_color(15, 90, 110)
        self.cell(0, 12, "Acqua Orbit DC", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(2)
        self.set_font(FAMILIA_FONTE, "", 12)
        self.set_text_color(50, 50, 50)
        self.cell(0, 7, "Global Solution 2026.1 - FIAP", new_x="LMARGIN", new_y="NEXT", align="C")
        self.cell(
            0,
            7,
            "Economia Espacial aplicada a data centers sustentaveis",
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
        )
        self.ln(8)
        self.set_font(FAMILIA_FONTE, "B", 12)
        self.cell(0, 7, "Grupo 13", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(2)
        self.set_font(FAMILIA_FONTE, "", 10)
        for nome in INTEGRANTES:
            self.cell(0, 6, nome, new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(6)
        self.set_font(FAMILIA_FONTE, "I", 9)
        self.cell(0, 6, LINK_REPOSITORIO, new_x="LMARGIN", new_y="NEXT", align="C")
        self.cell(
            0,
            6,
            f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
        )

    def indice(self) -> None:
        self.nova_secao("Indice")
        secoes = [
            "1. Documento academico da Global Solution",
            "2. Resultados da ultima execucao",
            "3. Evidencias visuais",
            "4. Modelo de IA (quando treinado)",
            "5. Anexo - trechos de codigo",
            "6. Links para entrega",
        ]
        for secao in secoes:
            self.item_lista(secao)

    def documento_academico(self) -> None:
        if not ARQUIVO_DOCUMENTO_GS.exists():
            self.nova_secao("Documento academico da Global Solution")
            self.paragrafo("Arquivo nao encontrado: document/ai_project_document_fiap.md")
            return

        self.nova_secao("1. Documento academico da Global Solution")
        conteudo = _preparar_documento_gs(ARQUIVO_DOCUMENTO_GS.read_text(encoding="utf-8"))
        self._renderizar_markdown(conteudo)

    def resultados_execucao(self) -> None:
        self.nova_secao("2. Resultados da ultima execucao")

        if not ARQUIVO_RESULTADOS.exists():
            self.paragrafo(
                "Arquivo src/data/resultados_regioes.csv nao encontrado. "
                "Execute a etapa 5 do pipeline antes de gerar o PDF."
            )
            return

        try:
            import pandas as pd

            df = pd.read_csv(ARQUIVO_RESULTADOS).sort_values(
                "score_final_poc_0_10", ascending=False
            )
        except Exception as erro:
            self.paragrafo(f"Erro ao ler resultados: {erro}")
            return

        self.paragrafo(
            "Tabela gerada a partir de src/data/resultados_regioes.csv "
            "(etapa 05). Reflete a classificacao por regras deterministicas da POC."
        )
        self.ln(2)

        colunas = [
            ("regiao", "Regiao"),
            ("estado", "UF"),
            ("score_final_poc_0_10", "Score"),
            ("classificacao_final", "Classificacao"),
            ("indice_esg_resiliencia_score_0_10", "ESG"),
            ("risco_ambiental_climatico_score_0_10", "Risco"),
            ("classificacao_qualidade_agua", "Agua"),
        ]
        cols_ok = [(c, r) for c, r in colunas if c in df.columns]

        self.set_font(FAMILIA_FONTE, "B", 8)
        self.set_x(self.l_margin)
        self.multi_cell(
            self.largura_util(),
            5,
            " | ".join(rotulo for _, rotulo in cols_ok),
        )
        self.ln(1)
        self.set_font(FAMILIA_FONTE, "", 8)
        for _, linha in df.iterrows():
            self.set_x(self.l_margin)
            valores = " | ".join(
                f"{linha[col]:.2f}" if isinstance(linha[col], float) else str(linha[col])
                for col, _ in cols_ok
            )
            self.multi_cell(self.largura_util(), 5, valores)

    def evidencias_visuais(self, capturas: list[tuple[str, Path]]) -> None:
        if not capturas:
            return

        self.nova_secao("3. Evidencias visuais")
        self.paragrafo(
            "Quatro capturas geradas a partir dos resultados atuais: ranking da POC, "
            "dashboard HTML (etapa 06) e duas telas do Streamlit interativo (etapa 09)."
        )
        self.ln(3)

        for titulo, caminho in capturas:
            if not caminho.exists():
                continue
            if self.get_y() > self.h - 80:
                self.add_page()
            self.set_font(FAMILIA_FONTE, "B", 11)
            self.set_x(self.l_margin)
            self.multi_cell(self.largura_util(), 6, titulo)
            self.ln(2)

            largura = self.largura_util()
            if self.get_y() + largura * 0.55 > self.h - 20:
                self.add_page()
            self.set_x(self.l_margin)
            self.image(str(caminho), w=largura)
            self.ln(6)

    def modelo_ia(self) -> None:
        if not ARQUIVO_MODELO_META.exists():
            return

        try:
            metadata = json.loads(ARQUIVO_MODELO_META.read_text(encoding="utf-8"))
        except Exception:
            return

        self.nova_secao("4. Modelo de IA")
        self.paragrafo(
            "RandomForest treinado sobre src/data/resultados_regioes.csv. "
            "Usado na visao Analise interativa (IA) do Streamlit."
        )
        self.ln(1)
        self.item_lista(f"Algoritmo: {metadata.get('algoritmo', 'N/A')}")
        self.item_lista(f"MAE nas regioes reais: {metadata.get('mae_regioes_reais', 'N/A')}")
        self.item_lista(f"R2 no teste: {metadata.get('r2_teste', 'N/A')}")
        self.item_lista(f"Treinado em: {metadata.get('treinado_em', 'N/A')}")
        self.item_lista(f"Arquivo: src/models/score_regiao_model.joblib")

    def anexo_codigo(self) -> None:
        self.nova_secao("5. Anexo - trechos de codigo")
        self.paragrafo(
            "Trechos representativos em texto, conforme exigencia da Global Solution. "
            "Codigo completo no repositorio."
        )
        self.ln(2)

        for titulo, caminho, funcoes in TRECHOS_CODIGO:
            trecho = extrair_funcoes(caminho, funcoes)
            if not trecho:
                continue
            self.set_font(FAMILIA_FONTE, "B", 11)
            self.set_x(self.l_margin)
            self.multi_cell(self.largura_util(), 6, titulo)
            self.ln(1)
            self.paragrafo(f"Arquivo: {caminho.relative_to(ROOT).as_posix()}", tamanho=9)
            self.ln(1)
            self._renderizar_codigo(trecho.splitlines())

    def links_entrega(self) -> None:
        self.nova_secao("6. Links para entrega")
        self.item_lista(f"Repositorio: {LINK_REPOSITORIO}")
        self.item_lista("Video demonstrativo (YouTube nao listado): [inserir link antes da entrega]")
        self.item_lista(
            'Para o podio: incluir "QUERO CONCORRER" no inicio do video e mencionar no PDF.'
        )
        self.ln(3)
        self.paragrafo("Arquivos principais de entrega:", estilo="B")
        entregaveis = [
            "document/ai_project_document_fiap.md",
            "src/output/acqua_orbit_dc_documentacao.pdf",
            "src/data/resultados_regioes.csv",
            "src/output/dashboard_poc.html",
            "src/frontend/dashboard_streamlit.py",
            "scripts/database/01_criar_tabelas_oracle.sql",
        ]
        for arquivo in entregaveis:
            self.item_lista(arquivo)

    def _renderizar_codigo(self, linhas: list[str]) -> None:
        self.set_fill_color(245, 245, 245)
        self.set_font(FAMILIA_FONTE, "", 7)
        largura = self.largura_util()
        for linha in linhas:
            if self.get_y() > self.h - 20:
                self.add_page()
                self.set_font(FAMILIA_FONTE, "", 7)
            self.set_x(self.l_margin)
            texto = linha if linha else " "
            if len(texto) > 105:
                texto = texto[:105] + " ..."
            self.multi_cell(largura, 4.0, texto, fill=True)
        self.ln(3)
        self.set_text_color(30, 30, 30)

    def _renderizar_markdown(self, conteudo: str) -> None:
        em_codigo = False
        buffer: list[str] = []

        for linha in conteudo.splitlines():
            if linha.strip().startswith("```"):
                if em_codigo:
                    self._renderizar_codigo(buffer)
                    buffer = []
                    em_codigo = False
                else:
                    em_codigo = True
                continue

            if em_codigo:
                buffer.append(linha)
                continue

            if not linha.strip():
                self.ln(2)
                continue

            if linha.startswith("# "):
                self.ln(2)
                self.set_font(FAMILIA_FONTE, "B", 14)
                self.set_x(self.l_margin)
                self.multi_cell(self.largura_util(), 7, linha[2:].strip())
                self.ln(1)
                continue

            if linha.startswith("## "):
                self.ln(2)
                self.set_font(FAMILIA_FONTE, "B", 12)
                self.set_x(self.l_margin)
                self.multi_cell(self.largura_util(), 6.5, linha[3:].strip())
                self.ln(1)
                continue

            if linha.startswith("### "):
                self.ln(1)
                self.set_font(FAMILIA_FONTE, "B", 11)
                self.set_x(self.l_margin)
                self.multi_cell(self.largura_util(), 6, linha[4:].strip())
                self.ln(1)
                continue

            if linha.startswith("#### "):
                self.set_font(FAMILIA_FONTE, "B", 10)
                self.set_x(self.l_margin)
                self.multi_cell(self.largura_util(), 5.5, linha[5:].strip())
                continue

            if re.match(r"^\|.+\|$", linha.strip()):
                celulas = [c.strip() for c in linha.strip("|").split("|")]
                self.set_font(FAMILIA_FONTE, "", 8)
                self.set_x(self.l_margin)
                self.multi_cell(self.largura_util(), 4.5, " | ".join(celulas))
                continue

            if set(linha.strip()) <= {"-", "|", " ", ":"}:
                continue

            if linha.startswith("- ") or linha.startswith("* "):
                self.item_lista(linha[2:])
            elif re.match(r"^\d+\.\s", linha):
                self.paragrafo(linha)
            else:
                self.paragrafo(linha)


def gerar_pdf() -> tuple[Path, list[tuple[str, Path]]]:
    OUTPUT.mkdir(parents=True, exist_ok=True)

    capturas: list[tuple[str, Path]] = []
    try:
        capturas = gerar_capturas_pdf()
        print(f"Capturas geradas: {len(capturas)} imagens em src/output/pdf_capturas/")
    except FileNotFoundError as erro:
        print(f"Aviso: capturas nao geradas ({erro}).")

    pdf = DocumentacaoPDF()
    pdf.capa()
    pdf.indice()
    pdf.documento_academico()
    pdf.resultados_execucao()
    pdf.evidencias_visuais(capturas)
    pdf.modelo_ia()
    pdf.anexo_codigo()
    pdf.links_entrega()

    pdf.output(str(ARQUIVO_PDF))
    return ARQUIVO_PDF, capturas


def main() -> None:
    print("Acqua Orbit DC - Geracao do PDF de documentacao")
    print("-" * 48)
    arquivo, capturas = gerar_pdf()
    print(f"PDF gerado: {arquivo}")
    print(f"Tamanho: {arquivo.stat().st_size / 1024:.1f} KB")
    if capturas:
        print(f"Capturas no PDF: {len(capturas)}")


if __name__ == "__main__":
    main()
