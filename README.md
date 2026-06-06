# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Acqua Orbit DC

## Grupo 13

Repositório: https://github.com/georgiamendesrocha/Fiap_GS_acquaorbit_DC

## Vídeo demonstrativo (Global Solution)

Vídeo de até 5 minutos no YouTube (**não listado**), conforme exigência da GS.

| Item | Valor |
|------|--------|
| Status | Pendente de publicação |
| Link | `https://youtu.be/SEU_LINK_AQUI` |
| Configuração | `config/entrega_gs.py` → `LINK_VIDEO_YOUTUBE` |

Quando o vídeo estiver no ar, substitua `SEU_LINK_AQUI` nesta tabela e no `config/entrega_gs.py`, depois regenere o PDF (`python menu.py` → opção **10**).

## 👨‍🎓 Integrantes

- Edemir Sufiatti - RM571375
- Carlos Magnus Costa Amaral - RM573978
- Georgia Mendes Rocha - RM573281
- Marina Leme Soares - RM570461
- Jocasta de Kacia Bortolacci - RM564730

## 👩‍🏫 Professores

### Tutor(a)

- Nicolly Candida Rodrigues de Souza

### Coordenador(a)

- Andre Godoi Chiovato

## 📜 Descrição

POC da Global Solution 2026.1 que compara três regiões candidatas a data center (Barueri/SP, Rio de Janeiro/RJ e Curitiba/PR) usando dados climáticos da NASA POWER, indicadores ambientais parametrizados, sensores de água simulados e regras de classificação ESG.

O projeto entrega pipeline executável, CSVs de resultado, dashboards (HTML e Streamlit), modelo de IA (RandomForest), persistência opcional em Oracle e PDF de documentação consolidado.

Solução acadêmica. Não substitui laudo técnico, auditoria ESG ou projeto de engenharia.

## Objetivo

Avaliar, com base em clima e coordenadas geográficas, qual região apresenta melhor equilíbrio entre risco ambiental, reuso pluvial, infraestrutura crítica e resiliência para apoiar decisão em data centers sustentáveis.

## Tecnologias

Python 3.10+, Pandas, Requests, Scikit-learn, Joblib, Matplotlib, Streamlit, FPDF2, CSV, HTML/SVG, NASA POWER, Oracle (`oracledb`, opcional).

## 📁 Estrutura de pastas

```
.github/              problem-report.md
assets/               logo-fiap.png
config/               oracle.example.env
document/             ai_project_document_fiap.md
scripts/database/     SQL Oracle (01, 02) e modelagem (03)
src/
  api/                nasa_power.py
  pipeline/           etapas 02 a 09
  ml/                 modelo_score_regiao.py, treinar_modelo.py
  frontend/           dashboards HTML e Streamlit
  db/                 conexão Oracle
  config/             carregar_env.py
  data/               CSVs de entrada e saída
  models/             modelo .joblib e metadata JSON
  output/             relatórios, dashboards, PDF e capturas
  menu.py             menu principal
  paths.py            caminhos centralizados
menu.py               atalho: python menu.py
requirements.txt
README.md
```

## Pipeline — etapas e scripts

| Etapa | Script | Saída principal |
|-------|--------|-----------------|
| 1 (opcional) | `src/api/nasa_power.py` | `src/data/nasa_power_2025_diario.csv` |
| 2 | `src/pipeline/02_tratar_dados_climaticos.py` | `src/data/nasa_power_2025_diario_tratado.csv` |
| 3 | `src/pipeline/03_montar_regioes_csv.py` | `src/data/regioes.csv` |
| 4 | `src/pipeline/04_validar_regioes_csv.py` | `src/output/relatorio_validacao_regioes_csv.md` |
| 5 | `src/pipeline/05_calcular_resultados_poc.py` | `src/data/resultados_regioes.csv` |
| 6 | `src/frontend/gerar_dashboard_html.py` | `src/output/dashboard_poc.html` |
| 7 | `src/pipeline/07_persistir_oracle_csv.py` | Oracle ou `src/output/fallback_csv/` |
| 8 (opcional) | `src/pipeline/08_consultar_resultados_oracle.py` | consulta no terminal |
| 9 | `src/ml/treinar_modelo.py` | `src/models/score_regiao_model.joblib` |
| 10 | `src/pipeline/09_gerar_pdf_documentacao.py` | `src/output/acqua_orbit_dc_documentacao.pdf` |

## Entregáveis para avaliação

### Dados

| Arquivo | Conteúdo |
|---------|----------|
| `src/data/regioes.csv` | Base oficial: clima, risco, infraestrutura, reuso pluvial |
| `src/data/resultados_regioes.csv` | Resultado final: sensores, índices, score e classificação |
| `src/data/nasa_power_2025_diario_tratado.csv` | Série diária tratada (NASA POWER, 2025) |

### Visualização

| Arquivo | Conteúdo |
|---------|----------|
| `src/output/dashboard_poc.html` | Dashboard estático: ranking, 6 gráficos, mapa, sensores |
| `src/frontend/dashboard_streamlit.py` | Entrada do Streamlit (duas visões no mesmo app) |
| `src/frontend/dashboard_streamlit_poc.py` | Réplica do HTML no Streamlit |
| `src/frontend/dashboard_streamlit_interativo.py` | Painel com ranking IA, indicadores, clima, mapa |

**Streamlit — duas visões** (seletor no topo da tela):

1. **Dashboard POC (HTML)** — conteúdo da etapa 06. Exige etapa 5.
2. **Análise interativa (IA)** — pódio, ranking IA, comparativo, clima NASA, sensores, mapa. Exige etapa 9 (modelo treinado).

### Documentação

| Arquivo | Conteúdo |
|---------|----------|
| `document/ai_project_document_fiap.md` | Documento acadêmico da GS |
| `src/output/acqua_orbit_dc_documentacao.pdf` | PDF consolidado com logo FIAP, entregáveis, capturas e código |
| `src/output/relatorio_*.md` | Relatório de cada etapa do pipeline |
| `src/output/pdf_capturas/` | Imagens geradas automaticamente para o PDF |

### Banco de dados (opcional)

| Arquivo | Conteúdo |
|---------|----------|
| `scripts/database/01_criar_tabelas_oracle.sql` | Tabelas `AO_REGIOES`, `AO_INDICADORES`, `AO_RESULTADOS_POC` |
| `scripts/database/02_consultas_oracle.sql` | Consultas de validação e ranking |
| `scripts/database/03_modelagem_dados.md` | Modelagem e dicionário de dados |
| `src/output/fallback_csv/` | Cópia em CSV quando Oracle não está configurado |

### Modelo de IA

| Arquivo | Conteúdo |
|---------|----------|
| `src/models/score_regiao_model.joblib` | Modelo RandomForest treinado |
| `src/models/score_regiao_metadata.json` | Features, MAE, R² e data do treino |

## 🔧 Como executar

Requisitos: Python 3.10+, PowerShell. Internet só na etapa 1. Oracle é opcional.

### Instalação

```powershell
pip install -r requirements.txt
```

### Menu

```powershell
python menu.py
```

| Opção | Função |
|-------|--------|
| 1 | NASA POWER (opcional, requer internet) |
| 2 | Tratar dados climáticos |
| 3 | Montar `regioes.csv` |
| 4 | Validar CSV |
| 5 | Calcular resultados e sensores |
| 6 | Gerar dashboard HTML |
| 7 | Persistir Oracle ou fallback CSV |
| 8 | Consultar Oracle (opcional) |
| 9 / T | Treinar modelo de IA |
| 10 | Gerar PDF de documentação |
| P | Pipeline completo (etapas 2 a 7) |
| N | Pipeline com NASA (etapas 1 a 7) |
| S | Streamlit (POC HTML ou análise interativa IA) |
| D | Abrir `dashboard_poc.html` no navegador |
| 0 | Sair |

Ordem sugerida para demonstração: `P` → `9` → `S` → `10`.

### Execução manual

```powershell
python src\pipeline\02_tratar_dados_climaticos.py
python src\pipeline\03_montar_regioes_csv.py
python src\pipeline\04_validar_regioes_csv.py
python src\pipeline\05_calcular_resultados_poc.py
python src\frontend\gerar_dashboard_html.py
python src\pipeline\07_persistir_oracle_csv.py
python src\ml\treinar_modelo.py
streamlit run src\frontend\dashboard_streamlit.py
python src\pipeline\09_gerar_pdf_documentacao.py
```

NASA POWER (internet):

```powershell
python src\api\nasa_power.py
```

Dashboard HTML no navegador:

```text
src/output/dashboard_poc.html
```

### PDF de documentação (etapa 10)

Gera `src/output/acqua_orbit_dc_documentacao.pdf` com a mesma abertura do README e corpo resumido:

1. Capa — logo FIAP, grupo, repositório, vídeo, integrantes, professores
2. Introdução — descrição, objetivo e tema espacial
3. Desenvolvimento — tecnologias, pipeline resumido e como executar
4. Resultados — ranking, tabela da execução, capturas visuais e IA
5. Conclusões — origem dos dados e limites
6. Anexo — trechos de código em texto
7. Links para entrega

Pré-requisito: etapa 5. Para capturas do Streamlit IA, rodar etapa 9 antes.

```powershell
python src\pipeline\09_gerar_pdf_documentacao.py
```

### Entrega na plataforma FIAP

Checklist final (alem do repositorio Git):

1. Gravar video de ate 5 min (`menu.py` -> `P` -> `9` -> `S` -> dashboards).
2. Subir no YouTube como **Nao listado**.
3. Editar `config/entrega_gs.py`:
   - `LINK_VIDEO_YOUTUBE` = URL do video
   - `CONCORRER_PODIO = True` somente se forem ao podio
4. Regenerar PDF: `python menu.py` -> opcao **10**.
5. Enviar na plataforma o arquivo `src/output/acqua_orbit_dc_documentacao.pdf`.

**Roteiro sugerido do video (5 min):** grupo + tema -> problema -> `python menu.py` -> pipeline -> dashboard HTML -> Streamlit -> ranking -> disciplinas integradas -> link do repo.

### Oracle (opcional)

1. Executar `scripts/database/01_criar_tabelas_oracle.sql` no SQL Developer.
2. Criar `.env` na raiz do repositório (ou pasta pai) com base em `config/oracle.example.env`:

```env
ORACLE_USER=RM000000
ORACLE_PASSWORD=sua_senha
ORACLE_DSN=oracle.fiap.com.br:1521/ORCL
```

3. Carregar variáveis no PowerShell:

```powershell
Get-Content .env | ForEach-Object {
    if ($_ -and -not $_.Trim().StartsWith("#") -and $_ -match "=") {
        $partes = $_ -split "=", 2
        Set-Item -Path "Env:$($partes[0].Trim())" -Value $partes[1].Trim().Trim('"')
    }
}
```

4. Persistir e consultar:

```powershell
python src\pipeline\07_persistir_oracle_csv.py
python src\pipeline\08_consultar_resultados_oracle.py
```

Sem Oracle, a etapa 7 grava em `src/output/fallback_csv/` e exibe `Persistencia concluida em modo: CSV fallback`.

Consultas prontas: `scripts/database/02_consultas_oracle.sql`.

Ranking esperado:

```text
Barueri / SP        | score 7.11 | favorável
Curitiba / PR       | score 6.81 | atenção
Rio de Janeiro / RJ | score 5.92 | atenção
```

## Origem dos dados

| Tipo | Origem |
|------|--------|
| Clima | NASA POWER (real, 2025) |
| Risco, infraestrutura, sensores | Parametrizados/simulados para a POC |
| Score e classificação final | Regras na etapa 05 |
| Ranking IA | RandomForest treinado sobre `resultados_regioes.csv` |

## Resultado da POC

| # | Região | Score | Classificação |
|---|--------|-------|---------------|
| 1 | Barueri/Tamboré | 7.11 | favorável |
| 2 | Curitiba | 6.81 | atenção |
| 3 | Rio de Janeiro (Barra/Jacarepaguá) | 5.92 | atenção |

## Limites

POC acadêmica com sensores simulados e indicadores parametrizados. Não cobre licenciamento ambiental, projeto elétrico, telecom ou engenharia de data center.

## 🗃 Histórico de lançamentos

* 1.0.0 - 06/06/2026 — Menu, Streamlit duplo (POC + IA), PDF com logo FIAP, template FIAP.
* 0.7.0 - 04/06/2026 — Persistência Oracle e fallback CSV.
* 0.6.0 - 04/06/2026 — Dashboard HTML.
* 0.5.0 - 04/06/2026 — Resultados finais e classificação.
* 0.1.0 - 03/06/2026 — Proposta e extração NASA POWER.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/georgiamendesrocha/Fiap_GS_acquaorbit_DC">Acqua Orbit DC</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
