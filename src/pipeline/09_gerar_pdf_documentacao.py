"""
Acqua Orbit DC - Etapa 09
Gera PDF de entrega da Global Solution.

Estrutura alinhada ao README (inicio igual, corpo resumido):
  1. Capa — logo FIAP, grupo, repo, video, integrantes, professores
  2. Introducao — descricao e objetivo
  3. Desenvolvimento — tecnologias, pipeline e execucao
  4. Resultados — ranking, evidencias visuais, modelo IA
  5. Conclusao — origem dos dados e limites
  6. Anexo — trechos de codigo em texto
  7. Links para entrega

Saida: src/output/acqua_orbit_dc_documentacao.pdf
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC if (_SRC / "paths.py").exists() else _SRC.parent))
from paths import DATA, MODELS, OUTPUT, ROOT, SRC, ASSETS  # noqa: E402

sys.path.insert(0, str(_SRC))
from pdf_gerar_capturas import gerar_capturas_pdf  # noqa: E402

from fpdf import FPDF

LINK_REPOSITORIO = "https://github.com/georgiamendesrocha/Fiap_GS_acquaorbit_DC"
ARQUIVO_ENTREGA_GS = ROOT / "config" / "entrega_gs.py"
ARQUIVO_PDF = OUTPUT / "acqua_orbit_dc_documentacao.pdf"
ARQUIVO_RESULTADOS = DATA / "resultados_regioes.csv"
ARQUIVO_MODELO_META = MODELS / "score_regiao_model.joblib"
ARQUIVO_MODELO_META_JSON = MODELS / "score_regiao_metadata.json"
LOGO_FIAP = ASSETS / "logo-fiap.png"

INTEGRANTES = [
    "Edemir Sufiatti - RM571375",
    "Carlos Magnus Costa Amaral - RM573978",
    "Georgia Mendes Rocha - RM573281",
    "Marina Leme Soares - RM570461",
    "Jocasta de Kacia Bortolacci - RM564730",
]

TUTOR = "Nicolly Candida Rodrigues de Souza"
COORDENADOR = "Andre Godoi Chiovato"

PIPELINE_RESUMO = [
    ("1 (opcional)", "NASA POWER", "Baixa clima real por coordenadas"),
    ("2", "Tratamento", "Prepara serie climatica diaria"),
    ("3", "Regioes", "Monta base oficial das 3 regioes"),
    ("4", "Validacao", "Confere estrutura do CSV"),
    ("5", "Resultados", "Calcula scores, sensores e classificacao"),
    ("6", "Dashboard HTML", "Gera dashboard_poc.html"),
    ("7", "Persistencia", "Oracle ou fallback CSV"),
    ("8 (opcional)", "Consulta Oracle", "Exibe ranking no terminal"),
    ("9", "Modelo IA", "Treina RandomForest"),
    ("10", "PDF", "Gera este documento"),
]

RANKING_POC = [
    ("1", "Barueri/Tambore - SP", "7.11", "favoravel"),
    ("2", "Curitiba - PR", "6.81", "atencao"),
    ("3", "Rio de Janeiro (Barra/Jacarepagua) - RJ", "5.92", "atencao"),
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


def carregar_config_entrega() -> tuple[str, bool]:
    valores: dict[str, str | bool] = {
        "LINK_VIDEO_YOUTUBE": "",
        "CONCORRER_PODIO": False,
    }
    if ARQUIVO_ENTREGA_GS.exists():
        exec(ARQUIVO_ENTREGA_GS.read_text(encoding="utf-8"), valores)
    link = str(valores.get("LINK_VIDEO_YOUTUBE", "")).strip()
    podio = bool(valores.get("CONCORRER_PODIO", False))
    return link, podio


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
    def __init__(self, link_video: str, concorrer_podio: bool) -> None:
        super().__init__(format="A4", unit="mm")
        self.link_video = link_video
        self.concorrer_podio = concorrer_podio
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

    def subtitulo(self, texto: str) -> None:
        self.ln(3)
        self.set_font(FAMILIA_FONTE, "B", 12)
        self.set_text_color(15, 90, 110)
        self.set_x(self.l_margin)
        self.multi_cell(self.largura_util(), 7, texto)
        self.ln(2)
        self.set_text_color(30, 30, 30)

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

    def linha_tabela(self, celulas: list[str], negrito: bool = False) -> None:
        self.set_x(self.l_margin)
        self.set_font(FAMILIA_FONTE, "B" if negrito else "", 9)
        self.multi_cell(self.largura_util(), 5, " | ".join(celulas))

    def capa(self) -> None:
        """Inicio igual ao README: logo, titulo, grupo, repo, video, integrantes, professores."""
        self.add_page()
        if LOGO_FIAP.exists():
            largura_logo = 48
            self.image(str(LOGO_FIAP), x=(self.w - largura_logo) / 2, y=12, w=largura_logo)
            self.set_y(54)
        else:
            self.set_y(25)

        self.set_font(FAMILIA_FONTE, "B", 11)
        self.set_text_color(50, 50, 50)
        self.cell(
            0,
            6,
            "FIAP - Faculdade de Informatica e Administracao Paulista",
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
        )
        self.ln(4)
        self.set_font(FAMILIA_FONTE, "B", 22)
        self.set_text_color(15, 90, 110)
        self.cell(0, 11, "Acqua Orbit DC", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(2)
        self.set_font(FAMILIA_FONTE, "B", 12)
        self.set_text_color(50, 50, 50)
        self.cell(0, 7, "Grupo 13", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(3)
        self.set_font(FAMILIA_FONTE, "", 10)
        self.cell(0, 6, f"Repositorio: {LINK_REPOSITORIO}", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(5)

        self.subtitulo("Video demonstrativo (Global Solution)")
        self.ln(1)
        self.linha_tabela(["Item", "Valor"], negrito=True)
        link = self.link_video or "Aguardando link"
        podio = "Sim" if self.concorrer_podio else "Nao"
        self.linha_tabela(["Link do video", link])
        self.linha_tabela(["Concorrencia ao podio", podio])
        self.ln(4)

        self.subtitulo("Integrantes")
        for nome in INTEGRANTES:
            self.item_lista(nome)

        self.subtitulo("Professores")
        self.item_lista(f"Tutor(a): {TUTOR}")
        self.item_lista(f"Coordenador(a): {COORDENADOR}")

        self.ln(4)
        self.set_font(FAMILIA_FONTE, "I", 9)
        self.cell(
            0,
            5,
            f"Documento gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
        )

    def secao_introducao(self) -> None:
        self.nova_secao("1. Introducao")

        self.subtitulo("Descricao")
        self.paragrafo(
            "POC da Global Solution 2026.1 que compara tres regioes candidatas a data center "
            "(Barueri/SP, Rio de Janeiro/RJ e Curitiba/PR) usando dados climaticos da NASA POWER, "
            "indicadores ambientais parametrizados, sensores de agua simulados e regras de "
            "classificacao ESG."
        )
        self.paragrafo(
            "O projeto entrega pipeline executavel, CSVs de resultado, dashboards HTML e Streamlit, "
            "modelo de IA (RandomForest) e persistencia opcional em Oracle."
        )
        self.paragrafo(
            "Solucao academica. Nao substitui laudo tecnico, auditoria ESG ou projeto de engenharia."
        )

        self.subtitulo("Objetivo")
        self.paragrafo(
            "Avaliar, com base em clima e coordenadas geograficas, qual regiao apresenta melhor "
            "equilibrio entre risco ambiental, reuso pluvial, infraestrutura critica e resiliencia "
            "para apoiar decisao em data centers sustentaveis."
        )

        self.subtitulo("Conexao com o tema espacial")
        self.paragrafo(
            "A NASA POWER fornece dados climaticos derivados de observacoes espaciais. "
            "A POC usa essas informacoes na Terra para comparar regioes candidatas a infraestrutura "
            "critica digital com criterios ambientais e de resiliencia."
        )

    def secao_desenvolvimento(self) -> None:
        self.nova_secao("2. Desenvolvimento da solucao")

        self.subtitulo("Tecnologias")
        self.paragrafo(
            "Python 3.10+, Pandas, Requests, Scikit-learn, Joblib, Matplotlib, Streamlit, "
            "FPDF2, CSV, HTML, NASA POWER e Oracle (oracledb, opcional)."
        )

        self.subtitulo("Pipeline resumido")
        self.linha_tabela(["Etapa", "Nome", "O que faz"], negrito=True)
        for etapa, nome, descricao in PIPELINE_RESUMO:
            self.linha_tabela([etapa, nome, descricao])

        self.subtitulo("Como executar")
        self.paragrafo("Instalacao: pip install -r requirements.txt")
        self.paragrafo("Menu principal: python menu.py")
        self.paragrafo("Ordem sugerida para demonstracao: P (pipeline 2-7) -> 9 (IA) -> S (Streamlit).")
        self.ln(1)
        self.paragrafo("Principais entregas geradas:", estilo="B")
        self.item_lista("src/data/resultados_regioes.csv")
        self.item_lista("src/output/dashboard_poc.html")
        self.item_lista("src/frontend/dashboard_streamlit.py (visoes POC e analise interativa IA)")
        self.item_lista("src/models/score_regiao_model.joblib (apos etapa 9)")

    def secao_resultados(self, capturas: list[tuple[str, Path]]) -> None:
        self.nova_secao("3. Resultados")

        self.subtitulo("Ranking da POC")
        self.linha_tabela(["#", "Regiao", "Score", "Classificacao"], negrito=True)
        for pos, regiao, score, classe in RANKING_POC:
            self.linha_tabela([pos, regiao, score, classe])

        if ARQUIVO_RESULTADOS.exists():
            try:
                import pandas as pd

                df = pd.read_csv(ARQUIVO_RESULTADOS).sort_values(
                    "score_final_poc_0_10", ascending=False
                )
                self.ln(3)
                self.subtitulo("Dados da ultima execucao")
                self.linha_tabela(
                    ["Regiao", "UF", "Score", "Classificacao", "Qualidade agua"],
                    negrito=True,
                )
                for _, row in df.iterrows():
                    self.linha_tabela(
                        [
                            str(row.get("regiao", ""))[:28],
                            str(row.get("estado", "")),
                            f"{row.get('score_final_poc_0_10', 0):.2f}",
                            str(row.get("classificacao_final", "")),
                            str(row.get("classificacao_qualidade_agua", "")),
                        ]
                    )
            except Exception:
                pass

        if capturas:
            self.ln(3)
            self.subtitulo("Evidencias visuais")
            self.paragrafo(
                "Capturas do ranking, dashboard HTML e Streamlit interativo."
            )
            self.ln(2)
            for titulo, caminho in capturas:
                if not caminho.exists():
                    continue
                if self.get_y() > self.h - 80:
                    self.add_page()
                self.set_font(FAMILIA_FONTE, "B", 10)
                self.set_x(self.l_margin)
                self.multi_cell(self.largura_util(), 6, titulo)
                self.ln(2)
                largura = self.largura_util()
                if self.get_y() + largura * 0.55 > self.h - 20:
                    self.add_page()
                self.set_x(self.l_margin)
                self.image(str(caminho), w=largura)
                self.ln(5)

        if ARQUIVO_MODELO_META_JSON.exists():
            try:
                meta = json.loads(ARQUIVO_MODELO_META_JSON.read_text(encoding="utf-8"))
                self.subtitulo("Modelo de IA")
                self.item_lista(f"Algoritmo: {meta.get('algoritmo', 'N/A')}")
                self.item_lista(f"MAE nas regioes reais: {meta.get('mae_regioes_reais', 'N/A')}")
                self.item_lista(f"Treinado em: {meta.get('treinado_em', 'N/A')}")
            except Exception:
                pass

    def secao_conclusao(self) -> None:
        self.nova_secao("4. Conclusoes")

        self.subtitulo("Origem dos dados")
        self.linha_tabela(["Tipo", "Origem"], negrito=True)
        self.linha_tabela(["Clima", "NASA POWER (real, 2025)"])
        self.linha_tabela(["Risco e infraestrutura", "Parametrizados para a POC"])
        self.linha_tabela(["Sensores de agua", "Simulados em Python"])
        self.linha_tabela(["Classificacao final", "Regras deterministicas (etapa 5)"])
        self.linha_tabela(["Ranking IA", "RandomForest sobre resultados_regioes.csv"])

        self.subtitulo("Limites")
        self.paragrafo(
            "POC academica com sensores simulados e indicadores parametrizados. "
            "Nao cobre licenciamento ambiental, projeto eletrico, telecom ou engenharia de data center."
        )

        self.subtitulo("Conclusao")
        self.paragrafo(
            "O Acqua Orbit DC demonstra como dados climaticos de origem espacial podem apoiar "
            "a comparacao de regioes candidatas a data centers sustentaveis. "
            "Barueri/SP liderou o ranking da POC com melhor equilibrio entre clima, ESG, "
            "infraestrutura e qualidade simulada da agua."
        )

    def anexo_codigo(self) -> None:
        self.nova_secao("5. Anexo - trechos de codigo")
        self.paragrafo(
            "Trechos em formato texto, conforme exigencia da Global Solution. "
            "Codigo completo no repositorio GitHub."
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
        self.item_lista(f"Repositorio GitHub: {LINK_REPOSITORIO}")
        link = self.link_video or "Aguardando link"
        podio = "Sim" if self.concorrer_podio else "Nao"
        self.item_lista(f"Link do video: {link}")
        self.item_lista(f"Concorrencia ao podio: {podio}")
        self.paragrafo(
            "Arquivo para upload na plataforma FIAP: src/output/acqua_orbit_dc_documentacao.pdf"
        )

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


def gerar_pdf() -> tuple[Path, list[tuple[str, Path]]]:
    OUTPUT.mkdir(parents=True, exist_ok=True)

    capturas: list[tuple[str, Path]] = []
    try:
        capturas = gerar_capturas_pdf()
        print(f"Capturas geradas: {len(capturas)} imagens em src/output/pdf_capturas/")
    except FileNotFoundError as erro:
        print(f"Aviso: capturas nao geradas ({erro}).")

    link_video, concorrer_podio = carregar_config_entrega()
    if not link_video:
        print("Aviso: LINK_VIDEO_YOUTUBE vazio em config/entrega_gs.py")

    pdf = DocumentacaoPDF(link_video, concorrer_podio)
    pdf.capa()
    pdf.secao_introducao()
    pdf.secao_desenvolvimento()
    pdf.secao_resultados(capturas)
    pdf.secao_conclusao()
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
