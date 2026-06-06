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

## Prototipo minimo (futuro)

1. ESP32 publica JSON no Serial ou MQTT.
2. Script Python substitui `simular_sensores_agua` por leitura real quando `SENSORES_MODO=real`.
3. Mesmas colunas em `resultados_regioes.csv` para nao quebrar dashboards.

A POC academica mantem simulacao; a arquitetura garante continuidade tecnica com sensores embarcados.
