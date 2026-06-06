# Modelagem Oracle - Acqua Orbit DC

Este documento descreve a camada Oracle opcional da POC. A base principal do projeto continua sendo CSV, mas o Oracle foi adicionado para atender ao escopo de persistencia em banco relacional.

## Arquivos relacionados

- `scripts/database/01_criar_tabelas_oracle.sql`: cria a estrutura Oracle.
- `scripts/database/02_consultas_oracle.sql`: consultas SQL para demonstracao e validacao.
- `src/pipeline/07_persistir_oracle_csv.py`: carrega `data/resultados_regioes.csv` no Oracle ou gera fallback CSV.
- `src/pipeline/08_consultar_resultados_oracle.py`: consulta o ranking final pelo terminal.

## Aviso sobre recriacao das tabelas

O script `01_criar_tabelas_oracle.sql` e reexecutavel para a POC. Ao rodar, ele remove e recria as tabelas `AO_RESULTADOS_POC`, `AO_INDICADORES` e `AO_REGIOES`.

Use esse comportamento quando quiser limpar a base e fazer uma carga nova. Se ja houver dados importantes no schema, nao rode o script sem antes salvar esses dados.

## Origem dos dados

A tabela de origem da persistencia e:

```text
data/resultados_regioes.csv
```

Esse CSV e gerado pela etapa 05 e concentra:

- dados cadastrais e geograficos da regiao;
- indicadores climaticos vindos da NASA POWER;
- indicadores ambientais e de infraestrutura parametrizados;
- sensores de agua simulados;
- indices finais e classificacao da POC.

## Estrutura logica

### AO_REGIOES

Armazena uma linha por regiao analisada.

Principais campos:

- `REGIAO_ID`: chave primaria textual.
- `REGIAO`, `EIXO_REGIONAL`, `CIDADE`, `ESTADO`: identificacao territorial.
- `LATITUDE`, `LONGITUDE`: coordenadas da regiao.
- `CONTEXTO_TERRITORIAL`, `BIOMA_CONTEXTO`: descricao contextual.
- `PERIODO_REFERENCIA`: ano de referencia dos dados climaticos.
- `FONTE_CLIMATICA`, `FONTE_CLIMATICA_URL`, `ORIGEM_DADOS_CLIMATICOS`: rastreabilidade da origem.

### AO_INDICADORES

Armazena indicadores climaticos, ambientais e de infraestrutura ligados a uma regiao.

Principais campos:

- temperatura, precipitacao, umidade, vento e radiacao solar;
- scores de risco hidrico, inundacao e sensibilidade territorial;
- parametros de reuso pluvial, como area de captacao e reservatorio;
- indicadores de conectividade, energia e resiliencia operacional;
- colunas de origem para indicar se o dado e real, calculado, simulado ou parametrizado.

### AO_RESULTADOS_POC

Armazena os resultados finais da prova de conceito.

Principais campos:

- sensores simulados de agua;
- classificacao de qualidade da agua;
- scores finais por dimensao;
- score final da POC;
- classificacao final;
- parecer de apoio a decisao.

## Relacionamentos

As tres tabelas usam `REGIAO_ID` como chave de relacionamento.

```text
AO_REGIOES.REGIAO_ID
        |
        +-- AO_INDICADORES.REGIAO_ID
        |
        +-- AO_RESULTADOS_POC.REGIAO_ID
```

`AO_REGIOES` e a tabela principal. `AO_INDICADORES` e `AO_RESULTADOS_POC` possuem chave estrangeira para ela.

## Criterio de tipagem

A tipagem foi definida a partir do conteudo real de `data/resultados_regioes.csv` e do significado das colunas.

- Identificadores e descricoes curtas usam `VARCHAR2`.
- `ESTADO` usa `CHAR(2)`.
- Coordenadas usam `NUMBER(9, 6)`.
- Ano usa `NUMBER(4)`.
- Medidas e scores usam `NUMBER` com casas decimais.
- Textos longos de parecer usam `CLOB`.

Tambem foram incluidos `CHECK constraints` para limitar valores esperados, como:

- latitude entre -90 e 90;
- longitude entre -180 e 180;
- scores entre 0 e 10;
- percentual entre 0 e 100;
- pH entre 0 e 14.

## Fallback CSV

Se o Oracle nao estiver configurado ou indisponivel, a etapa 07 nao interrompe o projeto. Ela gera os arquivos:

```text
output/fallback_csv/ao_regioes.csv
output/fallback_csv/ao_indicadores.csv
output/fallback_csv/ao_resultados_poc.csv
```

Esse fallback formaliza que a aplicacao pode ser demonstrada com ou sem Oracle.
