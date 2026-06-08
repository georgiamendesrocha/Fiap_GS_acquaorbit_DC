# Relatorio de Persistencia Oracle/CSV - Acqua Orbit DC

## Etapa executada

Persistencia dos resultados finais da POC em Oracle opcional, com fallback automatico em CSV.

## Modo utilizado

CSV fallback

## Registros processados

3

## Detalhe

Variaveis ORACLE_USER, ORACLE_PASSWORD e ORACLE_DSN nao encontradas em .env.

## Estrutura logica

- `AO_REGIOES`: dados cadastrais e geograficos das regioes.
- `AO_INDICADORES`: indicadores climaticos, ambientais e de infraestrutura.
- `AO_RESULTADOS_POC`: sensores simulados, indices finais e classificacao.

## Apoio Oracle

- `scripts/database/01_criar_tabelas_oracle.sql`: cria ou recria as tabelas Oracle.
- `scripts/database/02_consultas_oracle.sql`: consultas para validacao e demonstracao.
- `scripts/database/03_modelagem_dados.md`: documentacao da modelagem e tipagem.

## Fallback CSV

Quando Oracle nao esta configurado ou indisponivel, os dados sao salvos em:

- `output/fallback_csv/ao_regioes.csv`
- `output/fallback_csv/ao_indicadores.csv`
- `output/fallback_csv/ao_resultados_poc.csv`
