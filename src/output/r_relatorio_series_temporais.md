# Relatorio R - Series temporais climaticas

## Disciplina

Statistical Computing with R - Series Temporais (analise de padroes e anomalias).

## Entrada

- `src/data/nasa_power_2025_diario_tratado.csv`
- Registros: 1095
- Regioes: 3

## Metodo

- Agregacao diaria por regiao (temperatura media e precipitacao).
- Deteccao de anomalias por z-score (|z| > 2).
- Graficos PNG em `src/output/r_graficos/`.

## Resultados por regiao

### Barueri/Tamboré

- Dias analisados: 365
- Temperatura media anual (serie diaria): 20.56 C
- Precipitacao acumulada: 754.35 mm

#### Anomalias detectadas (|z| > 2)

- Total: 32 (temperatura e/ou precipitacao)

  - 2025-06-11 | temp_media = 13.02 (z = -2.1)
  - 2025-06-12 | temp_media = 12.02 (z = -2.38)
  - 2025-06-24 | temp_media = 12.9 (z = -2.13)
  - 2025-06-25 | temp_media = 11.34 (z = -2.57)
  - 2025-07-02 | temp_media = 11.11 (z = -2.63)
  - ... (+27 eventos)
#### Graficos

- `serie_temp_Barueri_Tambor_.png`
- `serie_precip_Barueri_Tambor_.png`

### Rio de Janeiro - Barra/Jacarepaguá/Parque Olímpico

- Dias analisados: 365
- Temperatura media anual (serie diaria): 23.22 C
- Precipitacao acumulada: 1011.26 mm

#### Anomalias detectadas (|z| > 2)

- Total: 20 (temperatura e/ou precipitacao)

  - 2025-06-25 | temp_media = 18.19 (z = -2.02)
  - 2025-07-30 | temp_media = 18.12 (z = -2.05)
  - 2025-08-12 | temp_media = 18.2 (z = -2.02)
  - 2025-12-31 | temp_media = 28.21 (z = 2.01)
  - 2025-01-01 | precipitacao_diaria_mm = 31.47 (z = 4.25)
  - ... (+15 eventos)
#### Graficos

- `serie_temp_Rio_de_Janeiro_Barra_Jacarepagu_Parque_Ol_mpico.png`
- `serie_precip_Rio_de_Janeiro_Barra_Jacarepagu_Parque_Ol_mpico.png`

### Curitiba

- Dias analisados: 365
- Temperatura media anual (serie diaria): 18.14 C
- Precipitacao acumulada: 1135.64 mm

#### Anomalias detectadas (|z| > 2)

- Total: 36 (temperatura e/ou precipitacao)

  - 2025-05-29 | temp_media = 9.4 (z = -2.01)
  - 2025-06-12 | temp_media = 9.38 (z = -2.01)
  - 2025-06-24 | temp_media = 5 (z = -3.02)
  - 2025-06-25 | temp_media = 6.74 (z = -2.62)
  - 2025-07-01 | temp_media = 8.69 (z = -2.17)
  - ... (+31 eventos)
#### Graficos

- `serie_temp_Curitiba.png`
- `serie_precip_Curitiba.png`

## Uso no projeto

A serie diaria alimenta a etapa 3 (regioes.csv), os dashboards e o painel Streamlit (aba Clima).
A deteccao de anomalias apoia a leitura de riscos climaticos na POC.

