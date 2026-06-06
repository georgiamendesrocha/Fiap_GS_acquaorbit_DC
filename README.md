# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Acqua Orbit DC

## Grupo 13

Repositório: https://github.com/georgiamendesrocha/Fiap_GS_acquaorbit_DC

## Vídeo demonstrativo (Global Solution)

| Item | Valor |
|------|--------|
| Link do vídeo | Aguardando link |
| Concorrência ao pódio | Sim |

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

- André Godoi Chiovato

## 📜 Descrição

POC da Global Solution 2026.1 que compara três regiões candidatas a data center (Barueri/SP, Rio de Janeiro/RJ e Curitiba/PR) usando dados climáticos da NASA POWER, indicadores ambientais parametrizados, sensores de água simulados e regras de classificação ESG.

O projeto entrega pipeline executável via `python menu.py`, CSVs de resultado, dashboards (HTML e Streamlit), análise de séries temporais em R (opção **R**), modelo de IA (RandomForest), persistência opcional em Oracle, integração com as disciplinas do semestre e PDF de documentação consolidado.

Solução acadêmica. Não substitui laudo técnico, auditoria ESG ou projeto de engenharia.

## Objetivo

Avaliar, com base em clima e coordenadas geográficas, qual região apresenta melhor equilíbrio entre risco ambiental, reuso pluvial, infraestrutura crítica e resiliência para apoiar decisão em data centers sustentáveis.

## Tecnologias

Python 3.10+, R 4.x (`Rscript`), Pandas, Requests, Scikit-learn, Joblib, Matplotlib, Streamlit, FPDF2, CSV, HTML/SVG, NASA POWER, Oracle (`oracledb`, opcional).

## 📁 Estrutura de pastas

```
.github/              problem-report.md
assets/               logo-fiap.png
config/               entrega_gs.py, oracle.example.env
document/             ai_project_document_fiap.md
scripts/database/     SQL Oracle (01, 02) e modelagem (03)
scripts/r/            analise de series temporais em R
hardware/esp32/       arquitetura de sensores (evolucao embarcada)
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
| R (lote) | `scripts/r/analise_serie_climatica.R` | `src/output/r_relatorio_series_temporais.md`, `r_graficos/` |

## Prints das etapas (terminal)

Cada etapa confirma no terminal o que foi processado e onde os arquivos foram salvos. Exemplos reais de execução com sucesso (caminhos abreviados como `src/...`):

### Etapa 1 — NASA POWER (opcional, requer internet)

```text
Consultando NASA POWER: Barueri/Tamboré
Consultando NASA POWER: Rio de Janeiro - Barra/Jacarepaguá/Parque Olímpico
Consultando NASA POWER: Curitiba
Arquivos gerados:
src/data/nasa_power_2025_diario.csv
src/data/clima_regioes_2025.csv
```

### Etapa 2 — Tratamento climático

```text
Acqua Orbit DC - Tratamento dos dados climaticos diarios
Base carregada: 1095 registros
Base diaria tratada com cabecalho interpretavel
Validacao concluida
Arquivos salvos com sucesso

Saidas:
- src/data/nasa_power_2025_diario_tratado.csv
- src/output/relatorio_tratamento_dados_climaticos.md
```

### Etapa 3 — Montagem do `regioes.csv`

```text
Acqua Orbit DC - Montagem do regioes.csv
Resumo climatico preparado: 3 regioes
Indicadores complementares integrados
Arquivo regioes.csv gerado com sucesso
- src/data/regioes.csv
- src/output/relatorio_montagem_regioes_csv.md
```

### Etapa 4 — Validação

```text
Ácqua Orbit DC — Validação do regioes.csv
Validação aprovada.
Relatório: src/output/relatorio_validacao_regioes_csv.md
```

### Etapa 5 — Resultados e sensores

```text
Acqua Orbit DC - Calculo dos resultados finais da POC
Base regioes carregada: 3 regioes
Indicadores finais calculados
Etapa 05 concluida com sucesso
- src/data/resultados_regioes.csv
- src/output/relatorio_resultados_poc.md
```

Ranking gravado no relatório:

```text
1. Barueri/Tamboré - score 7.11 - favorável
2. Curitiba - score 6.81 - atenção
3. Rio de Janeiro - Barra/Jacarepaguá/Parque Olímpico - score 5.92 - atenção
```

### Etapa 6 — Dashboard HTML

```text
Acqua Orbit DC - Geracao de visualizacoes da POC
Resultados carregados: 3 regioes
Etapa 06 concluida com sucesso
- src/output/dashboard_poc.html
- src/output/relatorio_visualizacoes_poc.md
```

### Etapa 7 — Persistência Oracle ou CSV

**Com Oracle configurado (`.env`):**

```text
Acqua Orbit DC - Persistencia Oracle opcional / CSV fallback
Resultados carregados: 3 regioes
Credenciais Oracle carregadas de: .env
Usuario Oracle: RM571375
Estrutura Oracle ja existente.
Persistencia concluida em modo: Oracle
- src/output/relatorio_persistencia_oracle_csv.md
```

**Sem Oracle (fallback automático):**

```text
Persistencia concluida em modo: CSV fallback
- src/output/relatorio_persistencia_oracle_csv.md
- src/output/fallback_csv/ao_regioes.csv
- src/output/fallback_csv/ao_indicadores.csv
- src/output/fallback_csv/ao_resultados_poc.csv
```

### Etapa 8 — Consulta Oracle (opcional)

```text
Credenciais Oracle carregadas de: .env
Usuario Oracle: RM571375
Estrutura Oracle ja existente.
Ranking Oracle - Acqua Orbit DC
--------------------------------
Barueri / SP | score 7.11 | favorável
Curitiba / PR | score 6.81 | atenção
Rio de Janeiro / RJ | score 5.92 | atenção
```

### Etapa 9 — Modelo de IA

```text
Acqua Orbit DC - Treinamento do modelo de IA
------------------------------------------------
Modelo salvo em: src/models/score_regiao_model.joblib
Metadados: src/models/score_regiao_metadata.json
Treinamento concluido com sucesso.
```

### Análise R — séries temporais (ação em lote `R` no menu)

```text
>> Executando: scripts\r\analise_serie_climatica.R
--------------------------------------------------------------
Analise R concluida.
- src/output/r_relatorio_series_temporais.md
- src/output/r_resumo_series_temporais.json
- Graficos em: src/output/r_graficos
--------------------------------------------------------------
Analise R concluida com sucesso.
```

**Pré-requisito:** etapa 2. Se `Rscript` não estiver no PATH, o menu exibe erro com instrução de instalação.

### Etapa 10 — PDF de documentação

```text
Acqua Orbit DC - Geracao do PDF de documentacao
------------------------------------------------
Capturas geradas: 4 imagens em src/output/pdf_capturas/
PDF gerado: src/output/acqua_orbit_dc_documentacao.pdf
Tamanho: 338.6 KB
Capturas no PDF: 4
```

> Se `LINK_VIDEO_YOUTUBE` estiver vazio em `config/entrega_gs.py`, aparece também: `Aviso: LINK_VIDEO_YOUTUBE vazio em config/entrega_gs.py`

**Ações em lote no menu:** `P` (pipeline 2–7), `N` (com NASA 1–7), `R` (séries temporais em R, após etapa 2), `T`/`S`/`D` (IA e dashboards). Os prints das etapas aparecem em sequência ao usar `P`.

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
| `src/output/r_relatorio_series_temporais.md` | Relatório R — séries temporais e anomalias |
| `src/output/r_graficos/` | Gráficos PNG gerados pelo script R |
| `hardware/esp32/README.md` | Arquitetura de sensores embarcados (evolução) |

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

Requisitos: Python 3.10+, R 4.x com `Rscript` no PATH (opção R), PowerShell. Internet só na etapa 1. Oracle é opcional.

### Instalação

```powershell
pip install -r requirements.txt
```

### Menu

```powershell
python menu.py
```

| Opção | Função (igual ao `python menu.py`) |
|-------|-------------------------------------|
| 1 | Extrair dados da NASA POWER (opcional, internet) |
| 2 | Tratar dados climáticos diários |
| 3 | Montar CSV oficial (`regioes.csv`) |
| 4 | Validar CSV oficial |
| 5 | Calcular resultados e sensores simulados |
| 6 | Gerar dashboard HTML |
| 7 | Persistir Oracle / fallback CSV |
| 8 | Consultar Oracle (opcional) |
| **Complementares** | |
| 9 | Treinar e salvar modelo de IA |
| 10 | Gerar PDF de documentação |
| **Ações em lote** | |
| P | Pipeline etapas 2 a 7 em sequência |
| N | Pipeline etapas 1 a 7 (com NASA) |
| R | Análise R (após etapa 2; requer `Rscript`) |
| T | Treinar IA (atalho da opção 9) |
| D | Abrir `dashboard_poc.html` (requer etapa 6) |
| S | Streamlit: POC HTML + análise IA (requer etapa 5) |
| 0 | Sair |

**Ordem sugerida para demonstração e vídeo:** `P` → `R` → `9` (ou `T`) → `S` → `10`.

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

Análise R (séries temporais, após etapa 2) — pelo menu: opção **R**, ou manualmente:

```powershell
$env:ACQUA_ROOT = (Get-Location).Path
Rscript scripts\r\analise_serie_climatica.R
```

Dashboard HTML no navegador:

```text
src/output/dashboard_poc.html
```

### PDF de documentação (etapa 10)

Gera `src/output/acqua_orbit_dc_documentacao.pdf` com a mesma abertura do README e corpo resumido:

1. Capa — integrantes, **QUERO CONCORRER** (pódio), professores, repositório e vídeo
2. Introdução — descrição, objetivo e tema espacial
3. Desenvolvimento — tecnologias, pipeline, menu (`P`, `R`, `9`, `S`) e entregas
4. Resultados Esperados — ranking, capturas, análise R e IA
5. Conclusões — origem dos dados, disciplinas, ética, segurança, sensores, formação social
6. Anexo — trechos de código em texto
7. Links para entrega

Pré-requisitos: etapa 5 para o PDF base; etapa 9 para capturas Streamlit IA; opção **R** para gráficos e resumo R no PDF.

```powershell
python src\pipeline\09_gerar_pdf_documentacao.py
```

### Entrega na plataforma FIAP

Checklist final (além do repositório Git):

1. Gravar vídeo de até 5 min (`menu.py` → `P` → `R` → `9` → `S` → dashboards).
2. Rodar análise R antes do PDF: `python menu.py` → opção **R** (ação em lote).
3. Subir no YouTube como **não listado**.
4. Editar `config/entrega_gs.py`:
   - `LINK_VIDEO_YOUTUBE` = URL do vídeo
   - `CONCORRER_PODIO = True` somente se forem ao pódio
5. Regenerar PDF: `python menu.py` → opção **10**.
6. Enviar na plataforma o arquivo `src/output/acqua_orbit_dc_documentacao.pdf`.

Roteiro detalhado por disciplina: seção [Integração com as disciplinas do semestre](#integração-com-as-disciplinas-do-semestre).

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

## Integração com as disciplinas do semestre

O tema oficial da GS é **data center sustentável** (economia espacial → decisão na Terra). A tabela abaixo mostra como cada disciplina aparece no repositório.

| Disciplina | Cobertura | Evidência no projeto |
|------------|-----------|----------------------|
| AI Challenges (ética IAG) | Forte na narrativa | Regras transparentes etapa 5; IA comparativa, não decisão final — ver seção abaixo |
| Python – Scikit-learn e Streamlit | Forte | `src/ml/`, `dashboard_streamlit*.py`, etapas 9 e S |
| Statistical Computing with R – Séries temporais | Implementado | Opção **R** no menu; `scripts/r/analise_serie_climatica.R` + `src/output/r_*` |
| Cognitive Data Science – DDL | Forte | `scripts/database/01_criar_tabelas_oracle.sql`, etapas 7 e 8 |
| Cognitive Cybersecurity | Documentado + prática básica | `.env` no `.gitignore`, `carregar_env.py` — ver seção abaixo |
| AI Computer Systems & Sensors | Parcial (simulado + arquitetura) | `simular_sensores_agua()`, `hardware/esp32/README.md` |
| Machine Learning & Modelling | Forte | RandomForest, metadata JSON, comparativo IA x regras |
| Formação Social | Forte na narrativa | ESG, impacto territorial — ver seção abaixo |

### Ética e governança da IA (AI Challenges)

- **Transparência:** a classificação oficial usa regras determinísticas na etapa 5 (`classificar_regiao`), documentadas no relatório e no CSV.
- **Papel da IA:** o RandomForest (etapa 9) **compara e ranqueia**; não substitui licenciamento, laudo ambiental nem decisão humana.
- **Viés e limites:** apenas 3 regiões; o treino usa ampliação sintética (`score_regiao_metadata.json`) — o modelo **não generaliza** para outras cidades.
- **Responsabilidade:** scores parametrizados e sensores simulados; a POC declara limites acadêmicos no README e no PDF.

### Séries temporais em R

Análise da série diária NASA POWER (disciplina **Statistical Computing with R**).

**Pré-requisito:** etapa 2 (`nasa_power_2025_diario_tratado.csv`).

```powershell
python menu.py
# opcao R (ou manualmente: Rscript scripts\r\analise_serie_climatica.R)
```

**Saídas:**

| Arquivo | Conteúdo |
|---------|----------|
| `src/output/r_relatorio_series_temporais.md` | Resumo por região e anomalias (z-score \|z\| > 2) |
| `src/output/r_resumo_series_temporais.json` | Metadados da execução |
| `src/output/r_graficos/*.png` | Séries de temperatura e precipitação |

A mesma série alimenta a etapa 3, o dashboard HTML e a aba **Clima** do Streamlit.

### Segurança dos dados (Cognitive Cybersecurity)

| Prática | Implementação |
|---------|----------------|
| Credenciais fora do Git | `.env` / `.ENV` listados no `.gitignore` |
| Exemplo sem segredo | `config/oracle.example.env` |
| Carregamento seguro | `src/config/carregar_env.py` — variáveis só em ambiente local |
| Dados da POC | Sem dados pessoais; clima público NASA POWER |
| Evolução futura | TLS em APIs, MQTT com TLS para sensores, roles Oracle |

**Não fazer:** commitar `.env`, senhas em código ou prints com `ORACLE_PASSWORD`.

### Sensores e sistemas embarcados (AI Computer Systems & Sensors)

Hoje as leituras são **simuladas** em Python, com os mesmos campos que um barramento ESP32/MQTT entregaria:

| Campo | Sensor alvo |
|-------|-------------|
| `ph_agua` | Sonda pH |
| `turbidez_ntu` | Turbidímetro |
| `condutividade_us_cm` | Condutividade |
| `nivel_reservatorio_pct` | Ultrassom / boia |
| `temperatura_agua_c` | DS18B20 / NTC |

Arquitetura de evolução: `hardware/esp32/README.md`.

```text
ESP32 + sensores -> MQTT/Serial -> Python (etapa 5) -> Oracle/CSV -> Streamlit
```

### Impacto social e formação social

- **Território:** compara Barueri/SP, Rio/RJ e Curitiba/PR — regiões com pressões ambientais e urbanas distintas (Mata Atlântica, calor costeiro, clima mais ameno no Sul).
- **Água e energia:** data centers consomem água de refrigeração e energia; a POC explicita reuso pluvial, risco hídrico e demanda térmica.
- **Equidade:** score alto não dispensa **consulta a comunidades, órgãos ambientais e poder público** — tecnologia apoia, não substitui diálogo social.
- **Sustentabilidade:** critérios ESG na classificação; solução inclusiva no sentido de balancear clima, infraestrutura e resiliência, não só eficiência econômica.

### Roteiro do vídeo (5 min) — por disciplina

| Tempo | Mostrar | Disciplina |
|-------|---------|------------|
| 0:00–0:45 | Grupo, tema espacial, problema do data center | Formação social |
| 0:45–1:30 | `python menu.py` → `P` (prints das etapas) | Python |
| 1:30–2:00 | Gráfico R ou `r_relatorio_series_temporais.md` | R, séries temporais |
| 2:00–2:30 | Sensores no CSV + `hardware/esp32/README.md` | Sensores |
| 2:30–3:00 | SQL Developer / etapa 7 ou 8 | DDL Oracle |
| 3:00–3:45 | Streamlit + etapa 9 (metadata do modelo) | ML, Streamlit |
| 3:45–4:15 | Regras etapa 5 vs IA; limites e viés | Ética IAG |
| 4:15–4:45 | `.env` fora do repo | Cybersecurity |
| 4:45–5:00 | Ranking + link GitHub | Fechamento GS |

## 🗃 Histórico de lançamentos

* 1.2.0 - 06/06/2026 — README e PDF revisados (menu, R, disciplinas, ética).
* 1.1.2 - 06/06/2026 — Opção R movida para ações em lote no menu.
* 1.1.1 - 06/06/2026 — Análise R integrada ao menu (opção R).
* 1.1.0 - 06/06/2026 — Integração disciplinar no README, análise R de séries temporais, arquitetura ESP32.
* 1.0.0 - 06/06/2026 — Menu, Streamlit duplo (POC + IA), PDF com logo FIAP, template FIAP.
* 0.7.0 - 04/06/2026 — Persistência Oracle e fallback CSV.
* 0.6.0 - 04/06/2026 — Dashboard HTML.
* 0.5.0 - 04/06/2026 — Resultados finais e classificação.
* 0.1.0 - 03/06/2026 — Proposta e extração NASA POWER.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/georgiamendesrocha/Fiap_GS_acquaorbit_DC">Acqua Orbit DC</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
