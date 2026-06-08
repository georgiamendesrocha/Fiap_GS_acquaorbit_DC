"""
Acqua Orbit DC - Etapa 09
Gera PDF de entrega da Global Solution.

Estrutura alinhada ao README (início igual, corpo resumido):
  1. Capa — logo FIAP, grupo, repo, vídeo, integrantes, professores
  2. Introdução — descrição e objetivo
  3. Desenvolvimento — tecnologias, pipeline, menu (P, 9, S, 10; R opcional)
  4. Resultados — ranking, capturas, análise R, modelo IA
  5. Conclusões — dados, disciplinas, ética, segurança, sensores, social
  6. Anexo — trechos de código em texto
  7. Links para entrega

Saída: src/output/acqua_orbit_dc_documentacao.pdf
"""

from __future__ import annotations

import json
import re
import sys
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
ARQUIVO_R_RESUMO = OUTPUT / "r_resumo_series_temporais.json"
DIR_R_GRAFICOS = OUTPUT / "r_graficos"
LOGO_FIAP = ASSETS / "logo-fiap.png"

# Espelha src/menu.py (exib_menu + processar_opcao)
ETAPAS_MENU = [
    ("1", "Extrair dados climáticos da NASA POWER", "opcional, requer internet"),
    ("2", "Tratar dados climáticos diários", ""),
    ("3", "Montar CSV oficial da POC (regioes.csv)", ""),
    ("4", "Validar CSV oficial", ""),
    ("5", "Calcular resultados finais e sensores simulados", ""),
    ("6", "Gerar dashboard HTML", ""),
    ("7", "Persistir no Oracle / fallback CSV", ""),
    ("8", "Consultar resultados no Oracle", "opcional"),
]

MENU_COMPLEMENTARES = [
    ("9", "Treinar e salvar modelo de IA (dashboard Streamlit)", "src/ml/treinar_modelo.py"),
    ("10", "Gerar PDF da documentação do projeto", "src/pipeline/09_gerar_pdf_documentacao.py"),
]

MENU_ACOES_LOTE = [
    ("P", "Executar pipeline completo", "etapas 2 a 7 em sequência"),
    ("N", "Executar pipeline com NASA", "etapas 1 a 7 em sequência"),
    ("R", "Análise de séries temporais em R", "complementar; após etapa 2; requer Rscript no PATH"),
    ("T", "Treinar e salvar modelo de IA", "atalho da opção 9"),
    ("D", "Abrir dashboard HTML no navegador", "abre src/output/dashboard_poc.html; requer etapa 6"),
    (
        "S",
        "Iniciar dashboard Streamlit interativo",
        "duas visões no app: POC HTML (etapa 6) e análise IA; requer etapa 5",
    ),
    ("0", "Sair", "encerra o menu"),
]

DISCIPLINAS_RESUMO = [
    ("AI Challenges (ética IAG)", "Regras etapa 5; IA comparativa, não decisão final"),
    ("Python + sklearn + Streamlit", "Pipeline, menu, etapas 9 e S"),
    ("R - Séries temporais", "Opção R; z-score e gráficos em src/output/r_graficos"),
    ("DDL Oracle", "scripts/database/01_*.sql; etapas 7 e 8"),
    ("Cybersecurity", ".env fora do Git; carregar_env.py"),
    ("Sensores / ESP32", "simular_sensores_agua(); hardware/esp32/README.md"),
    ("ML & Modelling", "RandomForest, metadata JSON, comparativo IA x regras"),
    ("Formação social", "ESG, impacto territorial Barueri, Rio e Curitiba"),
]

INTEGRANTES = [
    "Edemir Sufiatti - RM571375",
    "Carlos Magnus Costa Amaral - RM573978",
    "Georgia Mendes Rocha - RM573281",
    "Marina Leme Soares - RM570461",
    "Jocasta de Kacia Bortolacci - RM564730",
]

TUTOR = "Nicolly Candida Rodrigues de Souza"
COORDENADOR = "André Godoi Chiovato"

PIPELINE_RESUMO = [
    ("1", "NASA POWER", "Baixa clima real por coordenadas (opcional)"),
    ("2", "Tratamento", "Prepara série climática diária"),
    ("3", "Regiões", "Monta regioes.csv"),
    ("4", "Validação", "Confere estrutura do CSV"),
    ("5", "Resultados", "Scores, sensores simulados e classificação"),
    ("6", "Dashboard HTML", "Gera dashboard_poc.html"),
    ("7", "Persistência", "Oracle ou fallback CSV"),
    ("8", "Consulta Oracle", "Ranking no terminal (opcional)"),
]

RANKING_POC = [
    ("1", "Barueri/Tamboré - SP", "7.11", "favorável"),
    ("2", "Curitiba - PR", "6.81", "atenção"),
    ("3", "Rio de Janeiro/RJ", "5.92", "atenção"),
]

MENSAGEM_VIDEO_PENDENTE = (
    "Link do vídeo pendente. Será inserido em breve após a publicação no YouTube."
)

TRECHOS_CODIGO: list[tuple[str, Path, list[str]]] = [
    (
        "Simulação de sensores e classificação final",
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


def resolver_grafico_r() -> Path | None:
    if not DIR_R_GRAFICOS.exists():
        return None
    preferidos = list(DIR_R_GRAFICOS.glob("serie_temp_*.png"))
    if preferidos:
        return sorted(preferidos)[0]
    demais = list(DIR_R_GRAFICOS.glob("*.png"))
    return sorted(demais)[0] if demais else None


def contar_anomalias_r() -> int | None:
    if not ARQUIVO_R_RESUMO.exists():
        return None
    try:
        dados = json.loads(ARQUIVO_R_RESUMO.read_text(encoding="utf-8"))
        total = 0
        for regiao, eventos in (dados.get("anomalias") or {}).items():
            if isinstance(eventos, list):
                total += len(eventos)
        return total
    except Exception:
        return None


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


def rotulo_regiao_pdf(regiao: str, estado: str = "") -> str:
    """Rótulos curtos para tabelas do PDF sem alterar os CSVs de origem."""
    nome = str(regiao)
    uf = str(estado).strip()
    if "Rio de Janeiro" in nome:
        return "Rio de Janeiro/RJ"
    if "Barueri" in nome:
        return "Barueri/SP"
    if "Curitiba" in nome:
        return "Curitiba/PR"
    return f"{nome}/{uf}" if uf else nome


def legenda_grafico_r(grafico: Path) -> str:
    if grafico.name == "serie_temp_Barueri_Tambor_.png":
        return "Gráfico R: série temporal de temperatura média - Barueri/Tamboré"
    return f"Gráfico R: {grafico.name}"


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
        self.cell(0, 8, f"Acqua Orbit DC - Grupo 13 | Página {self.page_no()}", align="C")

    def largura_util(self) -> float:
        return self.w - self.l_margin - self.r_margin

    def garantir_espaco(self, altura_mm: float = 28) -> None:
        if self.get_y() > self.h - altura_mm:
            self.add_page()
            self.set_text_color(30, 30, 30)

    def subtitulo(self, texto: str) -> None:
        self.garantir_espaco(28)
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
        """Início igual ao README: logo, título, grupo, repo, vídeo, integrantes, professores."""
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
            "FIAP - Faculdade de Informática e Administração Paulista",
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
        self.ln(4)

        self.subtitulo("Integrantes")
        for nome in INTEGRANTES:
            self.item_lista(nome)

        if self.concorrer_podio:
            self.ln(3)
            self.set_font(FAMILIA_FONTE, "B", 14)
            self.set_text_color(15, 90, 110)
            self.cell(0, 9, "QUERO CONCORRER", new_x="LMARGIN", new_y="NEXT", align="C")
            self.set_text_color(50, 50, 50)
            self.ln(2)

        self.subtitulo("Professores")
        self.item_lista(f"Tutor(a): {TUTOR}")
        self.item_lista(f"Coordenador(a): {COORDENADOR}")

        self.ln(3)
        self.set_font(FAMILIA_FONTE, "", 10)
        self.cell(0, 6, f"Repositório: {LINK_REPOSITORIO}", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(4)

        self.subtitulo("Vídeo demonstrativo (Global Solution)")
        self.ln(1)
        self.linha_tabela(["Item", "Valor"], negrito=True)
        link = self.link_video or MENSAGEM_VIDEO_PENDENTE
        podio = "Sim" if self.concorrer_podio else "Não"
        self.linha_tabela(["Link do vídeo", link])
        self.linha_tabela(["Concorrência ao pódio", podio])

    def secao_introducao(self) -> None:
        self.nova_secao("1. Introdução")

        self.subtitulo("Descrição")
        self.paragrafo(
            "O Acqua Orbit DC é uma solução acadêmica desenvolvida para apoiar a análise de "
            "regiões candidatas à instalação ou operação de data centers sustentáveis. A aplicação "
            "compara Barueri/SP, Rio de Janeiro/RJ e Curitiba/PR a partir de dados climáticos da "
            "NASA POWER, indicadores ambientais parametrizados, sensores de água simulados e regras "
            "de classificação ESG."
        )
        self.paragrafo(
            "A proposta transforma dados climáticos, ambientais e operacionais em uma visão simples, "
            "comparativa e demonstrável, indicando quais regiões apresentam melhor equilíbrio entre "
            "risco ambiental, potencial de reuso pluvial, infraestrutura crítica e resiliência."
        )
        self.paragrafo(
            "Embora tenha sido desenvolvida no contexto acadêmico da Global Solution 2026.1, a "
            "estrutura da solução foi pensada para permitir evolução futura com dados em tempo real, "
            "sensores físicos, integração com banco de dados e apoio técnico a decisões ambientais "
            "e operacionais."
        )
        self.paragrafo(
            "O projeto entrega pipeline executável via menu (python menu.py), CSVs de resultado, "
            "dashboards HTML e Streamlit, análise de séries temporais em R (opção R), modelo de IA "
            "(RandomForest) e persistência opcional em Oracle."
        )
        self.paragrafo(
            "Solução acadêmica. Não substitui laudo técnico, auditoria ESG ou projeto de engenharia."
        )

        self.subtitulo("Objetivo")
        self.paragrafo(
            "Avaliar, com base em clima e coordenadas geográficas, qual região apresenta melhor "
            "equilíbrio entre risco ambiental, reuso pluvial, infraestrutura crítica e resiliência "
            "para apoiar decisão em data centers sustentáveis."
        )

        self.subtitulo("Resposta ao desafio da GS 2026.1")
        self.paragrafo(
            "Pergunta central: como a tecnologia espacial melhora processos e decisões na Terra? "
            "O Acqua Orbit DC utiliza dados de satélites (NASA POWER) para monitoramento climático "
            "e apoio à escolha de regiões para data centers sustentáveis — infraestrutura crítica "
            "que depende de água, energia, conectividade e resiliência ambiental."
        )

        self.subtitulo("Conexão com o tema espacial")
        self.paragrafo(
            "A NASA POWER fornece dados climáticos derivados de observações espaciais. "
            "A POC usa essas informações na Terra para comparar regiões candidatas a infraestrutura "
            "crítica digital com critérios ambientais e de resiliência."
        )

    def secao_desenvolvimento(self) -> None:
        self.nova_secao("2. Desenvolvimento da solução")

        self.subtitulo("Tecnologias")
        self.paragrafo(
            "Python 3.10+, R 4.x (Rscript), Pandas, Requests, Scikit-learn, Joblib, Matplotlib, "
            "Streamlit, FPDF2, CSV, HTML, NASA POWER e Oracle (oracledb, opcional)."
        )

        self.subtitulo("Arquitetura da solução")
        self.paragrafo(
            "Fluxo: etapas 1-8 do menu (NASA POWER → tratamento → regioes.csv → validação → "
            "resultados/sensores → dashboard HTML → Oracle/CSV → consulta Oracle). "
            "Complementos: opção R (séries temporais após etapa 2), opções 9/T (IA), S (Streamlit), "
            "10 (PDF)."
        )
        self.paragrafo(
            "Sensores de água simulados em Python; evolução ESP32/MQTT em hardware/esp32/README.md."
        )

        self.subtitulo("Decisões do grupo")
        self.item_lista("Três regiões oficiais (Barueri, Rio, Curitiba) para comparação territorial.")
        self.item_lista("Classificação oficial por regras ESG; IA como ranking comparativo.")
        self.item_lista("Menu unificado (python menu.py) como ponto único de execução da POC.")
        self.item_lista("Fallback CSV quando Oracle não está disponível.")

        self.subtitulo("Como executar")
        self.paragrafo("Instalação: pip install -r requirements.txt")
        self.paragrafo("Entrada: python menu.py (atalho na raiz do repositório).")
        self.paragrafo(
            "Ordem sugerida: P → 9 ou T → S → 10. Opcional: R, se o Rscript estiver instalado. "
            "A opção N inclui a etapa 1 (NASA POWER), que requer internet para consultar a NASA POWER."
        )

        self.subtitulo("Menu principal — etapas do pipeline [1] a [8]")
        self.linha_tabela(["Opção", "Ação no menu", "Obs."], negrito=True)
        for opcao, acao, obs in ETAPAS_MENU:
            self.linha_tabela([opcao, acao, obs or "-"])

        self.subtitulo("Menu — ações complementares")
        self.linha_tabela(["Opção", "Ação no menu", "Script"], negrito=True)
        for opcao, acao, script in MENU_COMPLEMENTARES:
            self.linha_tabela([opcao, acao, script])

        self.subtitulo("Menu — ações em lote")
        self.linha_tabela(["Opção", "Ação no menu", "Comportamento"], negrito=True)
        for opcao, acao, comportamento in MENU_ACOES_LOTE:
            self.linha_tabela([opcao, acao, comportamento])

        self.subtitulo("Resumo das etapas (scripts)")
        self.linha_tabela(["Etapa", "Módulo", "Saída principal"], negrito=True)
        for etapa, nome, descricao in PIPELINE_RESUMO:
            self.linha_tabela([etapa, nome, descricao])
        self.linha_tabela(["R", "scripts/r/analise_serie_climatica.R", "r_relatorio + r_graficos/"])
        self.linha_tabela(["9", "src/ml/treinar_modelo.py", "score_regiao_model.joblib"])
        self.linha_tabela(["10", "09_gerar_pdf_documentacao.py", "acqua_orbit_dc_documentacao.pdf"])

        self.subtitulo("Principais entregas")
        self.item_lista("src/data/resultados_regioes.csv (etapa 5)")
        self.item_lista("src/output/dashboard_poc.html (etapa 6)")
        self.item_lista("src/output/r_relatorio_series_temporais.md (opção R)")
        self.item_lista("src/models/score_regiao_model.joblib (opção 9 ou T)")
        self.item_lista("src/output/acqua_orbit_dc_documentacao.pdf (opção 10)")

    def secao_resultados(self, capturas: list[tuple[str, Path]]) -> None:
        self.nova_secao("3. Resultados Esperados")

        self.subtitulo("Ranking da POC")
        self.linha_tabela(["#", "Região", "Score", "Classificação"], negrito=True)
        for pos, regiao, score, classe in RANKING_POC:
            self.linha_tabela([pos, regiao, score, classe])

        if ARQUIVO_RESULTADOS.exists():
            try:
                import pandas as pd

                df = pd.read_csv(ARQUIVO_RESULTADOS).sort_values(
                    "score_final_poc_0_10", ascending=False
                )
                self.ln(3)
                self.subtitulo("Dados da última execução")
                self.linha_tabela(
                    ["Região", "UF", "Score", "Classificação", "Qualidade da água"],
                    negrito=True,
                )
                for _, row in df.iterrows():
                    self.linha_tabela(
                        [
                            rotulo_regiao_pdf(
                                str(row.get("regiao", "")),
                                str(row.get("estado", "")),
                            ),
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
            self.subtitulo("Evidências visuais")
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

        self._secao_analise_r()

        if ARQUIVO_MODELO_META_JSON.exists():
            try:
                meta = json.loads(ARQUIVO_MODELO_META_JSON.read_text(encoding="utf-8"))
                self.subtitulo("Modelo de IA")
                self.item_lista(f"Algoritmo: {meta.get('algoritmo', 'N/A')}")
                self.item_lista(f"MAE nas regiões avaliadas: {meta.get('mae_regioes_reais', 'N/A')}")
                self.item_lista(f"Treinado em: {meta.get('treinado_em', 'N/A')}")
                self.paragrafo(
                    "Esse valor deve ser interpretado com cautela, pois o modelo foi treinado em "
                    "contexto acadêmico, com três regiões reais e ampliação sintética."
                )
                self.paragrafo(
                    "Este modelo é comparativo e acadêmico. Ele não substitui a classificação oficial "
                    "por regras nem generaliza para outras cidades sem novos dados."
                )
            except Exception:
                pass

    def _secao_analise_r(self) -> None:
        if not ARQUIVO_R_RESUMO.exists() and not DIR_R_GRAFICOS.exists():
            self.ln(3)
            self.subtitulo("Análise R (séries temporais)")
            self.paragrafo(
                "Não executada nesta geração. Rode python menu.py → opção R (após etapa 2) e regenere o PDF."
            )
            return

        self.ln(3)
        self.subtitulo("Análise R (séries temporais)")
        self.paragrafo(
            "Disciplina Statistical Computing with R: série diária NASA POWER 2025, "
            "detecção de anomalias por z-score (|z| > 2) e gráficos em src/output/r_graficos/."
        )

        if ARQUIVO_R_RESUMO.exists():
            try:
                dados = json.loads(ARQUIVO_R_RESUMO.read_text(encoding="utf-8"))
                self.item_lista(f"Registros analisados: {dados.get('registros', 'N/A')}")
                self.item_lista(f"Gerado em: {dados.get('gerado_em', 'N/A')}")
                total_anomalias = contar_anomalias_r()
                if total_anomalias is not None:
                    self.item_lista(f"Anomalias detectadas (3 regiões): {total_anomalias}")
            except Exception:
                pass

        grafico = resolver_grafico_r()
        if grafico and grafico.exists():
            self.ln(2)
            self.set_font(FAMILIA_FONTE, "B", 10)
            self.set_x(self.l_margin)
            self.multi_cell(self.largura_util(), 6, legenda_grafico_r(grafico))
            self.ln(2)
            if self.get_y() > self.h - 90:
                self.add_page()
            largura = self.largura_util()
            self.set_x(self.l_margin)
            self.image(str(grafico), w=largura * 0.92)
            self.ln(5)

    def secao_conclusao(self) -> None:
        self.nova_secao("4. Conclusões")

        self.subtitulo("Origem dos dados")
        self.linha_tabela(["Tipo", "Origem"], negrito=True)
        self.linha_tabela(["Clima", "NASA POWER (real, 2025)"])
        self.linha_tabela(["Risco e infraestrutura", "Parametrizados para a POC"])
        self.linha_tabela(["Sensores de água", "Simulados em Python"])
        self.linha_tabela(["Classificação final", "Regras determinísticas (etapa 5)"])
        self.linha_tabela(["Ranking IA", "RandomForest sobre resultados_regioes.csv"])

        self.subtitulo("Integração com as disciplinas do semestre")
        self.linha_tabela(["Disciplina", "Evidência no projeto"], negrito=True)
        for disciplina, evidencia in DISCIPLINAS_RESUMO:
            self.linha_tabela([disciplina, evidencia])

        self.subtitulo("Ética e governança da IA")
        self.item_lista(
            "Classificação oficial por regras determinísticas; IA não substitui decisão humana."
        )
        self.item_lista(
            "Modelo treinado com 3 regiões e ampliação sintética — não generaliza para outras cidades."
        )
        self.item_lista(
            "POC acadêmica: não substitui laudo ambiental, auditoria ESG ou licenciamento."
        )

        self.subtitulo("Segurança dos dados")
        self.item_lista("Credenciais Oracle apenas em .env (fora do Git, listado no .gitignore).")
        self.item_lista("Exemplo sem segredo: config/oracle.example.env")
        self.item_lista("POC sem dados pessoais; clima público NASA POWER.")

        self.subtitulo("Sensores e sistemas embarcados")
        self.item_lista(
            "Leituras simuladas em Python (pH, turbidez, condutividade, nível, temperatura da água)."
        )
        self.item_lista("Arquitetura futura ESP32/MQTT documentada em hardware/esp32/README.md.")

        self.subtitulo("Impacto social e formação social")
        self.item_lista(
            "Comparação territorial ESG entre Barueri/SP, Rio/RJ e Curitiba/PR."
        )
        self.item_lista(
            "Score técnico não dispensa consulta a comunidades e órgãos ambientais."
        )

        self.subtitulo("Limites")
        self.paragrafo(
            "POC acadêmica com sensores simulados e indicadores parametrizados. "
            "Não cobre licenciamento ambiental, projeto elétrico, telecom ou engenharia de data center."
        )

        self.garantir_espaco(55)
        self.subtitulo("Conclusão")
        self.paragrafo(
            "O Acqua Orbit DC demonstra como dados climáticos de origem espacial podem apoiar "
            "a comparação de regiões candidatas a data centers sustentáveis. "
            "Barueri/SP liderou o ranking da POC com melhor equilíbrio entre clima, ESG, "
            "infraestrutura e qualidade simulada da água."
        )

    def anexo_codigo(self) -> None:
        self.nova_secao("5. Anexo - trechos de código")
        self.paragrafo(
            "Trechos em formato texto, conforme exigência da Global Solution. "
            "Código completo no repositório GitHub."
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
        self.item_lista(f"Repositório GitHub: {LINK_REPOSITORIO}")
        link = self.link_video or MENSAGEM_VIDEO_PENDENTE
        podio = "Sim" if self.concorrer_podio else "Não"
        self.item_lista(f"Link do vídeo: {link}")
        self.item_lista(f"Concorrência ao pódio: {podio}")
        if self.concorrer_podio:
            self.item_lista('Frase no documento e no vídeo: "QUERO CONCORRER"')
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
        print(f"Aviso: capturas não geradas ({erro}).")

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
    print("Acqua Orbit DC - Geração do PDF de documentação")
    print("-" * 48)
    arquivo, capturas = gerar_pdf()
    print(f"PDF gerado: {arquivo}")
    print(f"Tamanho: {arquivo.stat().st_size / 1024:.1f} KB")
    if capturas:
        print(f"Capturas no PDF: {len(capturas)}")


if __name__ == "__main__":
    main()
