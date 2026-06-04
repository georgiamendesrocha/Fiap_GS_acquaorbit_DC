# Relatorio de Montagem do regioes.csv - Acqua Orbit DC

## Etapa executada

Integracao dos dados climaticos tratados com indicadores parametrizados, simulados e calculados da POC.

## Entrada climatica

- Preferencial: `data/nasa_power_2025_diario_tratado.csv`
- Alternativa: `data/clima_regioes_2025_tratado.csv`

## Arquivo gerado

- `data/regioes.csv`

## Regioes incluidas

- Barueri/Tamboré (Barueri/SP)
- Rio de Janeiro - Barra/Jacarepaguá/Parque Olímpico (Rio de Janeiro/RJ)
- Curitiba (Curitiba/PR)

## Origem dos dados

- Dados climaticos: NASA POWER, origem real.
- Riscos ambientais: parametrizados para fins academicos.
- Reuso pluvial: calculado a partir da precipitacao e de area/capacidade simuladas.
- Infraestrutura critica digital: parametrizada para representar conectividade, energia, redundancia e resiliencia.
- Demanda de refrigeracao: calculada a partir da temperatura media e maxima.

## Observacao

O arquivo `regioes.csv` e a base oficial de entrada da POC. Ele nao representa laudo tecnico real, auditoria de data center, estudo profissional de telecomunicacoes ou analise energetica profissional.
