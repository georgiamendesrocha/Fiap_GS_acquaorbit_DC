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
- Coordenador(a): Andre Godoi Chiovato

## Sumario

1. Introducao
2. Visao geral do projeto
3. Desenvolvimento da solucao
4. Resultados obtidos
5. Conclusões e possíveis evoluções fora do escopo da POC atual
6. Referencias
7. Anexos

## 1. Introducao

### 1.1 Contexto

A Global Solution 2026.1 tem como tema a economia espacial e seus impactos na Terra. Dentro desse contexto, dados climaticos, coordenadas geograficas, sensores e automacao podem apoiar decisoes mais sustentaveis em setores criticos.

O Acqua Orbit DC aplica essa ideia ao planejamento de data centers sustentaveis e resilientes. Data centers dependem de energia, agua, refrigeracao, conectividade e baixa exposicao a riscos ambientais. Por isso, comparar regioes candidatas exige integrar dados climaticos, geoespaciais, ESG e de infraestrutura critica digital.

### 1.2 Problema

O problema central e a dificuldade de comparar regioes candidatas a data centers a partir de dados dispersos sobre clima, risco ambiental, agua, conectividade, energia e resiliencia operacional.

Uma regiao pode ter bom potencial de reuso pluvial, mas risco de inundacao elevado. Outra pode ter conectividade forte, mas maior demanda de refrigeracao. A POC organiza esses fatores em uma classificacao simples e explicavel.

### 1.3 Proposta

O Acqua Orbit DC e uma POC academica que compara tres regioes oficiais:

- Barueri/Tambore - SP
- Rio de Janeiro - Barra/Jacarepagua/Parque Olimpico - RJ
- Curitiba - PR

A solucao usa dados climaticos de 2025 da NASA POWER, indicadores parametrizados, sensores simulados, regras calculadas e persistencia opcional em Oracle para gerar uma classificacao final por regiao.

## 2. Visao Geral do Projeto

### 2.1 Objetivos

O objetivo principal e demonstrar como dados climaticos por coordenadas geograficas podem apoiar decisoes ESG sobre infraestrutura critica na Terra.

Objetivos especificos:

- tratar dados climaticos reais da NASA POWER;
- montar uma base oficial `regioes.csv`;
- validar a estrutura e qualidade da base;
- simular sensores de agua;
- calcular indicadores ambientais, geoespaciais, hidricos, energeticos e de conectividade;
- gerar classificacao final das regioes;
- apresentar resultados em CSV, relatorios e dashboard HTML;
- persistir resultados em Oracle opcional ou fallback CSV.

### 2.2 Publico-alvo

A POC pode apoiar discussoes academicas e demonstracoes para equipes de ESG, sustentabilidade, planejamento de data centers, infraestrutura tecnologica, gestao de risco e analise ambiental.

### 2.3 Escopo

Esta POC esta dentro de um escopo academico. Ela nao representa laudo tecnico, auditoria ESG, estudo profissional de data center, analise hidrologica, projeto energetico ou avaliacao real de telecomunicacoes.

## 3. Desenvolvimento da Solucao

### 3.1 Tecnologias utilizadas

- Python
- Pandas
- Requests
- Oracle opcional com `oracledb`
- CSV
- HTML e SVG
- NASA POWER
- Regras deterministicas para simulacao e classificacao

### 3.2 Arquitetura geral

O projeto foi organizado como um pipeline em etapas:

1. Extracao ou uso da base climatica NASA POWER.
2. Tratamento dos dados climaticos diarios.
3. Montagem do CSV oficial da POC.
4. Validacao do CSV oficial.
5. Calculo dos indicadores finais e sensores simulados.
6. Geracao de dashboard HTML.
7. Persistencia opcional em Oracle ou fallback CSV.

### 3.3 Dados climaticos

Os dados climaticos utilizados sao da NASA POWER, com periodo de referencia de 2025. As variaveis usadas incluem:

- temperatura media;
- temperatura maxima;
- temperatura minima;
- precipitacao;
- umidade;
- vento;
- radiacao solar.

Esses dados sao tratados em `src/pipeline/02_tratar_dados_climaticos.py` e resultam no arquivo `data/nasa_power_2025_diario_tratado.csv`.

### 3.4 Montagem do `regioes.csv`

O script `src/pipeline/03_montar_regioes_csv.py` consolida os dados climaticos anuais e adiciona indicadores parametrizados de risco hidrico, inundacao, sensibilidade territorial, infraestrutura critica e reuso pluvial.

O arquivo gerado e `data/regioes.csv`.

### 3.5 Validacao

O script `src/pipeline/04_validar_regioes_csv.py` valida:

- presenca das tres regioes oficiais;
- colunas obrigatorias;
- ausencia de nulos em campos criticos;
- scores entre 0 e 10;
- origem dos dados em valores permitidos.

### 3.6 Indicadores finais

O script `src/pipeline/05_calcular_resultados_poc.py` calcula:

- indicador geoespacial simplificado;
- indice de risco ambiental e climatico;
- indice de potencial de reuso pluvial;
- indice de qualidade simulada da agua;
- indice de conectividade critica;
- indice de disponibilidade energetica;
- indice de refrigeracao e risco termico;
- indice ESG e de resiliencia;
- score final da POC;
- classificacao final.

### 3.7 Sensores simulados

Os sensores de agua sao simulados por regras deterministicas, considerando variaveis climaticas e de risco. A simulacao gera:

- nivel do reservatorio;
- pH da agua;
- turbidez;
- condutividade;
- temperatura da agua;
- classificacao da qualidade da agua.

As classificacoes possiveis sao:

- adequada;
- necessita tratamento;
- deve ser descartada.

### 3.8 Oracle opcional e fallback CSV

O projeto possui persistencia opcional em Oracle. O script `scripts/database/01_criar_tabelas_oracle.sql` cria as tabelas:

- `AO_REGIOES`;
- `AO_INDICADORES`;
- `AO_RESULTADOS_POC`.

As tabelas foram modeladas a partir das colunas reais de `data/resultados_regioes.csv`. A estrutura usa tipos Oracle compativeis com cada grupo de dados, como `VARCHAR2` para textos, `CHAR(2)` para estado, `NUMBER` para medidas e scores, e `CLOB` para o parecer de apoio a decisao. Tambem foram adicionadas restricoes de validacao para coordenadas, percentuais, pH e scores entre 0 e 10.

O script `src/pipeline/07_persistir_oracle_csv.py` tenta gravar os dados no Oracle quando as credenciais estao configuradas. Caso contrario, gera fallback automatico em CSV dentro de `output/fallback_csv`.

O script `src/pipeline/08_consultar_resultados_oracle.py` permite consultar o ranking salvo no Oracle diretamente pelo terminal.

O arquivo `scripts/database/02_consultas_oracle.sql` concentra consultas de validacao para contagem de registros, ranking final, sensores simulados, risco ambiental, potencial de reuso pluvial e resiliencia ESG.

### 3.9 Visualizacoes

O script `src/frontend/gerar_dashboard_html.py` gera `output/dashboard_poc.html`, contendo:

- ranking final;
- grafico de score final;
- grafico ESG/resiliencia;
- grafico de risco ambiental;
- grafico de conectividade;
- grafico de energia;
- grafico de reuso pluvial;
- mapa simplificado por latitude e longitude;
- tabela de sensores simulados.

## 4. Resultados Obtidos

### 4.1 Ranking final

| Posicao | Regiao | Score final | Classificacao |
|---|---|---:|---|
| 1 | Barueri/Tambore - SP | 7.11 | favoravel |
| 2 | Curitiba - PR | 6.81 | atencao |
| 3 | Rio de Janeiro - Barra/Jacarepagua/Parque Olimpico - RJ | 5.92 | atencao |

### 4.2 Qualidade simulada da agua

| Regiao | Qualidade simulada | Observacao |
|---|---|---|
| Barueri/Tambore | adequada | pH 6.81, turbidez 4.22 NTU, nivel 25% |
| Curitiba | necessita tratamento | pH 7.17, turbidez 5.24 NTU, nivel 25% |
| Rio de Janeiro | necessita tratamento | pH 6.95, turbidez 7.34 NTU, nivel 25% |

### 4.3 Indicadores selecionados

| Regiao | ESG/resiliencia | Risco ambiental | Potencial pluvial |
|---|---:|---:|---:|
| Barueri/Tambore | 7.34 | 4.18 | 3017.40 m3/ano |
| Curitiba | 7.56 | 4.40 | 4542.56 m3/ano |
| Rio de Janeiro | 6.65 | 6.24 | 4045.04 m3/ano |

### 4.4 Analise dos resultados

Barueri/Tambore ficou em primeiro lugar por apresentar bom equilibrio entre infraestrutura critica, conectividade, menor risco de inundacao parametrizado e classificacao simulada de agua adequada.

Curitiba ficou em segundo lugar. Apesar do bom potencial pluvial e bom indice ESG/resiliencia, recebeu classificacao final de atencao por exigir tratamento da agua simulada e apresentar indicadores intermediarios de infraestrutura.

Rio de Janeiro ficou em terceiro lugar. A regiao tem boa infraestrutura parametrizada, mas apresentou maior risco de inundacao e maior risco ambiental/climatico no modelo, ficando em classificacao de atencao.

### 4.5 Validacao da camada Oracle

A camada Oracle opcional foi testada no Oracle SQL Developer com as credenciais academicas da FIAP.

Evidencias da validacao:

- tabelas `AO_REGIOES`, `AO_INDICADORES` e `AO_RESULTADOS_POC` criadas com sucesso;
- carga executada pelo script `src/pipeline/07_persistir_oracle_csv.py` em modo Oracle;
- `AO_REGIOES` retornou 3 registros;
- `AO_INDICADORES` retornou 3 registros;
- `AO_RESULTADOS_POC` retornou 3 registros;
- consulta de ranking retornou Barueri, Curitiba e Rio de Janeiro na ordem esperada;
- consulta de sensores simulados retornou as 3 regioes com pH, turbidez, condutividade e classificacao da agua;
- consulta de risco ambiental retornou as 3 regioes com relacionamento entre `AO_REGIOES`, `AO_INDICADORES` e `AO_RESULTADOS_POC`.

Resultado do ranking validado no Oracle:

| Posicao | Cidade | Estado | Score final | Classificacao |
|---|---|---|---:|---|
| 1 | Barueri | SP | 7.11 | favoravel |
| 2 | Curitiba | PR | 6.81 | atencao |
| 3 | Rio de Janeiro | RJ | 5.92 | atencao |

## 5. Conclusões e possíveis evoluções fora do escopo da POC atual

### 5.1 Conclusao

O Acqua Orbit DC demonstra que dados climaticos por coordenadas, indicadores ambientais, sensores simulados e criterios de infraestrutura critica podem ser combinados para gerar uma leitura comparativa simples e explicavel sobre regioes candidatas a data centers sustentaveis.

A POC atende ao objetivo de conectar economia espacial, analise de dados e tomada de decisao na Terra, usando dados climaticos publicos e uma metodologia transparente.

### 5.2 Possíveis evoluções futuras fora do escopo da POC atual

Possiveis evolucoes:

- incluir novas regioes;
- usar dados ambientais reais adicionais;
- integrar mapas interativos;
- ampliar a modelagem de risco hidrico e inundacao;
- conectar a uma aplicacao web;
- enriquecer a camada Oracle com consultas historicas;
- comparar cenarios com pesos de decisao diferentes.

## 6. Referencias

- NASA POWER: https://power.larc.nasa.gov/
- FIAP Global Solution 2026.1 - tema Economia Espacial.
- Documentacao Oracle Python `oracledb`: https://python-oracledb.readthedocs.io/
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

- HTML estatico: `src/output/dashboard_poc.html`
- Streamlit: `src/frontend/dashboard_streamlit.py` (visoes POC HTML e analise interativa IA)

### 7.4 Repositorio do projeto

https://github.com/georgiamendesrocha/Fiap_GS_acquaorbit_DC

### 7.5 Video demonstrativo

- Gravar ate 5 minutos demonstrando menu, pipeline, dashboards e ranking.
- Publicar no YouTube como **Nao listado**.
- Colocar a URL em `config/entrega_gs.py` (campo `LINK_VIDEO_YOUTUBE`).
- Regenerar o PDF (`python menu.py` -> opcao 10). O link aparece na capa e na secao 6 do PDF.
- Para o podio: definir `CONCORRER_PODIO = True` e dizer **QUERO CONCORRER** nos primeiros segundos do video.
