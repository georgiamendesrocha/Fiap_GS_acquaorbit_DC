# Arquitetura de sensores (evolucao ESP32)

A POC atual simula leituras em `src/pipeline/05_calcular_resultados_poc.py` (`simular_sensores_agua`).
Este diretorio documenta a integracao fisica prevista para a disciplina **AI Computer Systems & Sensors**.

## Fluxo alvo

```text
ESP32 + sensores (pH, turbidez, nivel, condutividade, temp. agua)
        -> serial/MQTT -> gateway Python -> etapa 5 / Oracle -> Streamlit
```

## Mapeamento simulado -> sensor fisico

| Campo Python | Sensor alvo | Unidade |
|--------------|-------------|---------|
| `ph_agua` | Sonda pH | escala 0-14 |
| `turbidez_ntu` | Turbidimetro | NTU |
| `condutividade_us_cm` | Condutividade | uS/cm |
| `nivel_reservatorio_pct` | Ultrassom / boia | % |
| `temperatura_agua_c` | DS18B20 / NTC | °C |

## Possível evolução futura

Nesta POC, os sensores são simulados em Python e registrados nos CSVs do projeto.

Em uma evolução futura, um ESP32 poderia publicar leituras em JSON via Serial ou MQTT, e um gateway Python poderia substituir a função de simulação por leitura real.

Essa integração física não está implementada nesta entrega. O que está implementado agora é a simulação dos sensores, o processamento em Python, a geração dos resultados e a visualização nos dashboards.
