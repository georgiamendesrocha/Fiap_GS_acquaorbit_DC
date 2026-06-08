<img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=30% height=30%>

# Acqua Orbit DC

## Grupo 13

### Integrantes

- Edemir Sufiatti - RM571375
- Carlos Magnus Costa Amaral - RM573978
- Georgia Mendes Rocha - RM573281
- Marina Leme Soares - RM570461
- Jocasta de Kacia Bortolacci - RM564730

### Professores

- Tutor(a): Nicolly Candida Rodrigues de Souza
- Coordenador(a): André Godoi Chiovato

## Sumário

1. Introdução
2. Visão geral do projeto
3. Desenvolvimento da solução
4. Resultados obtidos
5. Conclusões e possíveis evoluções fora do escopo da POC atual
6. Referências
7. Anexos

## 1. Introdução

### 1.1 Contexto

A Global Solution 2026.1 tem como tema a economia espacial e seus impactos na Terra. Dentro desse contexto, dados climáticos, coordenadas geográficas, sensores e automação podem apoiar decisões mais sustentáveis em setores críticos.

O Acqua Orbit DC aplica essa ideia ao planejamento de data centers sustentáveis e resilientes. Data centers dependem de energia, água, refrigeração, conectividade e baixa exposição a riscos ambientais. Por isso, comparar regiões candidatas exige integrar dados climáticos, geoespaciais, ESG e de infraestrutura crítica digital.

### 1.2 Problema

O problema central é a dificuldade de comparar regiões candidatas a data centers a partir de dados dispersos sobre clima, risco ambiental, água, conectividade, energia e resiliência operacional.

Uma região pode ter bom potencial de reuso pluvial, mas risco de inundação elevado. Outra pode ter conectividade forte, mas maior demanda de refrigeração. A POC organiza esses fatores em uma classificação simples e explicável.

### 1.3 Proposta

O Acqua Orbit DC é uma POC acadêmica que compara três regiões oficiais:

- Barueri/Tamboré - SP
- Rio de Janeiro/RJ (Barra/Jacarepaguá/Parque Olímpico)
- Curitiba - PR

A solução usa dados climáticos de 2025 da NASA POWER, indicadores parametrizados, sensores simulados, regras calculadas e persistência opcional em Oracle para gerar uma classificação final por região.

A proposta transforma dados climáticos, ambientais e operacionais em uma visão simples, comparativa e demonstrável, indicando quais regiões apresentam melhor equilíbrio entre risco ambiental, potencial de reuso pluvial, infraestrutura crítica e resiliência.

Embora tenha sido desenvolvida no contexto acadêmico da Global Solution 2026.1, a estrutura da solução foi pensada para permitir evolução futura com dados em tempo real, sensores físicos, integração com banco de dados e apoio técnico a decisões ambientais e operacionais.

## 2. Visão Geral do Projeto

### 2.1 Objetivos

O objetivo principal é demonstrar como dados climáticos por coordenadas geográficas podem apoiar decisões ESG sobre infraestrutura crítica na Terra.

Objetivos específicos:

- tratar dados climáticos reais da NASA POWER;
- montar uma base oficial `regioes.csv`;
- validar a estrutura e qualidade da base;
- simular sensores de água;
- calcular indicadores ambientais, geoespaciais, hídricos, energéticos e de conectividade;
- gerar classificação final das regiões;
- apresentar resultados em CSV, relatórios e dashboard HTML;
- persistir resultados em Oracle opcional ou fallback CSV.

### 2.2 Público-alvo

A POC pode apoiar discussões acadêmicas e demonstrações para equipes de ESG, sustentabilidade, planejamento de data centers, infraestrutura tecnológica, gestão de risco e análise ambiental.

### 2.3 Escopo

Esta POC está dentro de um escopo acadêmico. Ela não representa laudo técnico, auditoria ESG, estudo profissional de data center, análise hidrológica, projeto energético ou avaliação real de telecomunicações.

## 3. Desenvolvimento da Solução

### 3.1 Tecnologias utilizadas

- Python
- Pandas
- Requests
- Oracle opcional com `oracledb`
- CSV
- HTML e SVG
- NASA POWER
- Regras determinísticas para simulação e classificação

### 3.2 Arquitetura geral

O projeto foi organizado como um pipeline em etapas:

1. Extração ou uso da base climática NASA POWER.
2. Tratamento dos dados climáticos diários.
3. Montagem do CSV oficial da POC.
4. Validação do CSV oficial.
5. Cálculo dos indicadores finais e sensores simulados.
6. Geração de dashboard HTML.
7. Persistência opcional em Oracle ou fallback CSV.

### 3.3 Dados climáticos

Os dados climáticos utilizados são da NASA POWER, com período de referência de 2025. As variáveis usadas incluem:

- temperatura média;
- temperatura máxima;
- temperatura mínima;
- precipitação;
- umidade;
- vento;
- radiação solar.

Esses dados são tratados em `src/pipeline/02_tratar_dados_climaticos.py` e resultam no arquivo `data/nasa_power_2025_diario_tratado.csv`.

### 3.4 Montagem do `regioes.csv`

O script `src/pipeline/03_montar_regioes_csv.py` consolida os dados climáticos anuais e adiciona indicadores parametrizados de risco hídrico, inundação, sensibilidade territorial, infraestrutura crítica e reuso pluvial.

O arquivo gerado é `data/regioes.csv`.

### 3.5 Validação

O script `src/pipeline/04_validar_regioes_csv.py` valida:

- presença das três regiões oficiais;
- colunas obrigatórias;
- ausência de nulos em campos críticos;
- scores entre 0 e 10;
- origem dos dados em valores permitidos.

### 3.6 Indicadores finais

O script `src/pipeline/05_calcular_resultados_poc.py` calcula:

- indicador geoespacial simplificado;
- índice de risco ambiental e climático;
- índice de potencial de reuso pluvial;
- índice de qualidade simulada da água;
- índice de conectividade crítica;
- índice de disponibilidade energética;
- índice de refrigeração e risco térmico;
- índice ESG e de resiliência;
- score final da POC;
- classificação final.

### 3.7 Sensores simulados

Os sensores de água são simulados por regras determinísticas, considerando variáveis climáticas e de risco. A simulação gera:

- nível do reservatório;
- pH da água;
- turbidez;
- condutividade;
- temperatura da água;
- classificação da qualidade da água.

As classificações possíveis são:

- adequada;
- necessita tratamento;
- deve ser descartada.

### 3.8 Oracle opcional e fallback CSV

O projeto possui persistência opcional em Oracle. O script `scripts/database/01_criar_tabelas_oracle.sql` cria as tabelas:

- `AO_REGIOES`;
- `AO_INDICADORES`;
- `AO_RESULTADOS_POC`.

As tabelas foram modeladas a partir das colunas reais de `data/resultados_regioes.csv`. A estrutura usa tipos Oracle compatíveis com cada grupo de dados, como `VARCHAR2` para textos, `CHAR(2)` para estado, `NUMBER` para medidas e scores, e `CLOB` para o parecer de apoio à decisão. Também foram adicionadas restrições de validação para coordenadas, percentuais, pH e scores entre 0 e 10.

O script `src/pipeline/07_persistir_oracle_csv.py` tenta gravar os dados no Oracle quando as credenciais estão configuradas. Caso contrário, gera fallback automático em CSV dentro de `output/fallback_csv`.

O script `src/pipeline/08_consultar_resultados_oracle.py` permite consultar o ranking salvo no Oracle diretamente pelo terminal.

O arquivo `scripts/database/02_consultas_oracle.sql` concentra consultas de validação para contagem de registros, ranking final, sensores simulados, risco ambiental, potencial de reuso pluvial e resiliência ESG.

### 3.9 Visualizações

O script `src/frontend/gerar_dashboard_html.py` gera `output/dashboard_poc.html`, contendo:

- ranking final;
- gráfico de score final;
- gráfico ESG/resiliência;
- gráfico de risco ambiental;
- gráfico de conectividade;
- gráfico de energia;
- gráfico de reuso pluvial;
- mapa simplificado por latitude e longitude;
- tabela de sensores simulados.

## 4. Resultados Obtidos

### 4.1 Ranking final

| Posição | Região | Score final | Classificação |
|---|---|---:|---|
| 1 | Barueri/Tamboré - SP | 7.11 | favorável |
| 2 | Curitiba - PR | 6.81 | atenção |
| 3 | Rio de Janeiro/RJ | 5.92 | atenção |

### 4.2 Qualidade simulada da água

| Região | Qualidade simulada | Observação |
|---|---|---|
| Barueri/Tamboré | adequada | pH 6.81, turbidez 4.22 NTU, nível 25% |
| Curitiba | necessita tratamento | pH 7.17, turbidez 5.24 NTU, nível 25% |
| Rio de Janeiro/RJ | necessita tratamento | pH 6.95, turbidez 7.34 NTU, nível 25% |

### 4.3 Indicadores selecionados

| Região | ESG/resiliência | Risco ambiental | Potencial pluvial |
|---|---:|---:|---:|
| Barueri/Tamboré | 7.34 | 4.18 | 3017.40 m3/ano |
| Curitiba | 7.56 | 4.40 | 4542.56 m3/ano |
| Rio de Janeiro/RJ | 6.65 | 6.24 | 4045.04 m3/ano |

### 4.4 Análise dos resultados

Barueri/Tamboré ficou em primeiro lugar por apresentar bom equilíbrio entre infraestrutura crítica, conectividade, menor risco de inundação parametrizado e classificação simulada de água adequada.

Curitiba ficou em segundo lugar. Apesar do bom potencial pluvial e bom índice ESG/resiliência, recebeu classificação final de atenção por exigir tratamento da água simulada e apresentar indicadores intermediários de infraestrutura.

Rio de Janeiro/RJ ficou em terceiro lugar. A região tem boa infraestrutura parametrizada, mas apresentou maior risco de inundação e maior risco ambiental/climático no modelo, ficando em classificação de atenção.

### 4.5 Validação da camada Oracle

A camada Oracle opcional foi testada no Oracle SQL Developer com as credenciais acadêmicas da FIAP.

Evidências da validação:

- tabelas `AO_REGIOES`, `AO_INDICADORES` e `AO_RESULTADOS_POC` criadas com sucesso;
- carga executada pelo script `src/pipeline/07_persistir_oracle_csv.py` em modo Oracle;
- `AO_REGIOES` retornou 3 registros;
- `AO_INDICADORES` retornou 3 registros;
- `AO_RESULTADOS_POC` retornou 3 registros;
- consulta de ranking retornou Barueri, Curitiba e Rio de Janeiro na ordem esperada;
- consulta de sensores simulados retornou as 3 regiões com pH, turbidez, condutividade e classificação da água;
- consulta de risco ambiental retornou as 3 regiões com relacionamento entre `AO_REGIOES`, `AO_INDICADORES` e `AO_RESULTADOS_POC`.

Resultado do ranking validado no Oracle:

| Posição | Cidade | Estado | Score final | Classificação |
|---|---|---|---:|---|
| 1 | Barueri | SP | 7.11 | favorável |
| 2 | Curitiba | PR | 6.81 | atenção |
| 3 | Rio de Janeiro | RJ | 5.92 | atenção |

## 5. Conclusões e possíveis evoluções fora do escopo da POC atual

### 5.1 Conclusão

O Acqua Orbit DC demonstra que dados climáticos por coordenadas, indicadores ambientais, sensores simulados e critérios de infraestrutura crítica podem ser combinados para gerar uma leitura comparativa simples e explicável sobre regiões candidatas a data centers sustentáveis.

A POC atende ao objetivo de conectar economia espacial, análise de dados e tomada de decisão na Terra, usando dados climáticos públicos e uma metodologia transparente.

### 5.2 Possíveis evoluções futuras fora do escopo da POC atual

Possíveis evoluções:

- incluir novas regiões;
- usar dados ambientais reais adicionais;
- integrar mapas interativos;
- ampliar a modelagem de risco hídrico e inundação;
- conectar a uma aplicação web;
- enriquecer a camada Oracle com consultas históricas;
- comparar cenários com pesos de decisão diferentes.

## 6. Referências

- NASA POWER: https://power.larc.nasa.gov/
- FIAP Global Solution 2026.1 - tema Economia Espacial.
- Documentação Oracle Python `oracledb`: https://python-oracledb.readthedocs.io/
- Pandas: https://pandas.pydata.org/

## 7. Anexos

### 7.1 Arquivos principais

- `README.md`
- `requirements.txt`
- `src/data/resultados_regioes.csv`
- `src/output/dashboard_poc.html`
- `src/output/acqua_orbit_dc_documentacao.pdf`
- `src/frontend/dashboard_streamlit.py`
- `src/models/score_regiao_model.joblib`
- `scripts/database/01_criar_tabelas_oracle.sql`
- `scripts/database/02_consultas_oracle.sql`
- `scripts/database/03_modelagem_dados.md`

### 7.2 Comandos principais

```powershell
pip install -r requirements.txt
python menu.py
```

Ou por etapa:

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

### 7.3 Dashboards

- HTML estático: `src/output/dashboard_poc.html`
- Streamlit: `src/frontend/dashboard_streamlit.py` (visões POC HTML e análise interativa IA)

### 7.4 Repositório do projeto

https://github.com/georgiamendesrocha/Fiap_GS_acquaorbit_DC

### 7.5 Vídeo demonstrativo

- Link do vídeo pendente. Será inserido em breve após a publicação no YouTube.
- Gravar até 5 minutos demonstrando menu, pipeline, dashboards e ranking.
- Publicar no YouTube como **não listado**.
- Colocar a URL em `config/entrega_gs.py` (campo `LINK_VIDEO_YOUTUBE`).
- Regenerar o PDF (`python menu.py` -> opção 10). O link aparece na capa e na seção 6 do PDF.
- Para o pódio: definir `CONCORRER_PODIO = True` e dizer **QUERO CONCORRER** nos primeiros segundos do vídeo.
