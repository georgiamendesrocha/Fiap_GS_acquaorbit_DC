import requests
import pandas as pd
from pathlib import Path

REGIOES = [
    {
        "regiao": "Barueri/Tamboré",
        "cidade": "Barueri",
        "estado": "SP",
        "latitude": -23.5000,
        "longitude": -46.8700,
    },
    {
        "regiao": "Rio de Janeiro - Barra/Jacarepaguá/Parque Olímpico",
        "cidade": "Rio de Janeiro",
        "estado": "RJ",
        "latitude": -22.9700,
        "longitude": -43.3900,
    },
    {
        "regiao": "Curitiba",
        "cidade": "Curitiba",
        "estado": "PR",
        "latitude": -25.4300,
        "longitude": -49.2700,
    },
]

PARAMETROS = [
    "T2M",
    "T2M_MAX",
    "T2M_MIN",
    "PRECTOTCORR",
    "RH2M",
    "WS2M",
    "ALLSKY_SFC_SW_DWN",
]

URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

def consultar_nasa_power(regiao):
    params = {
        "start": "20250101",
        "end": "20251231",
        "latitude": regiao["latitude"],
        "longitude": regiao["longitude"],
        "community": "SB",
        "parameters": ",".join(PARAMETROS),
        "format": "JSON",
        "units": "metric",
        "time-standard": "LST",
    }

    resposta = requests.get(URL, params=params, timeout=60)
    resposta.raise_for_status()

    dados = resposta.json()["properties"]["parameter"]

    df = pd.DataFrame(dados)
    df.index.name = "data"
    df = df.reset_index()

    for campo, valor in regiao.items():
        df[campo] = valor

    return df

def gerar_base_climatica():
    bases = []

    for regiao in REGIOES:
        print(f"Consultando NASA POWER: {regiao['regiao']}")
        df = consultar_nasa_power(regiao)
        bases.append(df)

    df_final = pd.concat(bases, ignore_index=True)

    Path("data").mkdir(exist_ok=True)
    df_final.to_csv("data/nasa_power_2025_diario.csv", index=False, encoding="utf-8-sig")

    resumo = (
        df_final
        .groupby(["regiao", "cidade", "estado", "latitude", "longitude"])
        .agg(
            temp_media=("T2M", "mean"),
            temp_maxima=("T2M_MAX", "max"),
            temp_minima=("T2M_MIN", "min"),
            precipitacao_anual_mm=("PRECTOTCORR", "sum"),
            umidade_media=("RH2M", "mean"),
            vento_medio=("WS2M", "mean"),
            radiacao_media=("ALLSKY_SFC_SW_DWN", "mean"),
        )
        .reset_index()
    )

    resumo["periodo_referencia"] = "2025"
    resumo["fonte_climatica"] = "NASA POWER"
    resumo["origem_dados_climaticos"] = "real"

    resumo.to_csv("data/clima_regioes_2025.csv", index=False, encoding="utf-8-sig")

    print("Arquivos gerados:")
    print("data/nasa_power_2025_diario.csv")
    print("data/clima_regioes_2025.csv")

if __name__ == "__main__":
    gerar_base_climatica()