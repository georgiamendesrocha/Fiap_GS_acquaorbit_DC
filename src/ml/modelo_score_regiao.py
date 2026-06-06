"""
Modelo de IA para predicao do score final de regioes candidatas.

Treina um regressor com base nos indicadores climaticos, ambientais
e de infraestrutura, salva o artefato em models/ e expoe funcoes de inferencia.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC if (_SRC / "paths.py").exists() else _SRC.parent))
from paths import DATA, DOCUMENT, MODELS, OUTPUT, ROOT, SCRIPTS_DB, SRC, ASSETS  # noqa: E402

import json
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ARQUIVO_RESULTADOS = DATA / "resultados_regioes.csv"
ARQUIVO_MODELO = MODELS / "score_regiao_model.joblib"
ARQUIVO_METADADOS = MODELS / "score_regiao_metadata.json"

FEATURES_MODELO = [
    "temperatura_media_anual_c",
    "temperatura_maxima_anual_c",
    "precipitacao_total_anual_mm",
    "umidade_media_anual_pct",
    "velocidade_vento_media_anual_m_s",
    "radiacao_solar_media_anual_kwh_m2_dia",
    "risco_hidrico_score_0_10",
    "risco_inundacao_score_0_10",
    "sensibilidade_territorial_score_0_10",
    "demanda_refrigeracao_score_0_10",
    "potencial_pluvial_m3_ano",
    "conectividade_critica_score_0_10",
    "redundancia_fibra_score_0_10",
    "disponibilidade_energetica_score_0_10",
    "risco_rota_unica_score_0_10",
    "resiliencia_operacional_score_0_10",
    "ph_agua",
    "turbidez_ntu",
    "condutividade_us_cm",
    "temperatura_agua_c",
]

TARGET = "score_final_poc_0_10"


def classificar_score(score: float) -> str:
    if score >= 7.0:
        return "favorável"
    if score >= 5.5:
        return "atenção"
    if score >= 4.0:
        return "alto risco"
    return "crítica"


def _limitar_score(valor: float) -> float:
    return float(np.clip(valor, 0.0, 10.0))


def augmentar_dados(df: pd.DataFrame, multiplicador: int = 120, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    linhas = []

    for _, base in df.iterrows():
        linhas.append(base.to_dict())
        for _ in range(multiplicador):
            variacao = base.copy()
            for coluna in FEATURES_MODELO:
                valor = float(base[coluna])
                escala = max(abs(valor) * 0.08, 0.15)
                variacao[coluna] = valor + rng.normal(0, escala)
            variacao[TARGET] = float(base[TARGET]) + rng.normal(0, 0.12)
            variacao[TARGET] = _limitar_score(variacao[TARGET])
            linhas.append(variacao.to_dict())

    return pd.DataFrame(linhas)


def treinar_modelo(df: pd.DataFrame) -> tuple[Pipeline, dict]:
    faltantes = [c for c in FEATURES_MODELO + [TARGET] if c not in df.columns]
    if faltantes:
        raise ValueError(f"Colunas ausentes para treino do modelo: {faltantes}")

    base = df[FEATURES_MODELO + [TARGET, "regiao", "regiao_id"]].copy()
    for coluna in FEATURES_MODELO + [TARGET]:
        base[coluna] = pd.to_numeric(base[coluna], errors="coerce")

    if base[FEATURES_MODELO + [TARGET]].isna().any().any():
        raise ValueError("Existem valores invalidos nos dados de treino.")

    treino = augmentar_dados(base)
    x = treino[FEATURES_MODELO]
    y = treino[TARGET]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    modelo = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=180,
                    max_depth=8,
                    min_samples_leaf=2,
                    random_state=42,
                ),
            ),
        ]
    )
    modelo.fit(x_train, y_train)

    pred_teste = modelo.predict(x_test)
    pred_base = modelo.predict(base[FEATURES_MODELO])

    metadata = {
        "algoritmo": "RandomForestRegressor + StandardScaler",
        "features": FEATURES_MODELO,
        "target": TARGET,
        "amostras_treino": int(len(x_train)),
        "amostras_teste": int(len(x_test)),
        "mae_teste": round(float(mean_absolute_error(y_test, pred_teste)), 4),
        "r2_teste": round(float(r2_score(y_test, pred_teste)), 4),
        "mae_regioes_reais": round(float(mean_absolute_error(base[TARGET], pred_base)), 4),
        "treinado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "observacao": (
            "Modelo introdutorio treinado com ampliacao sintetica a partir das 3 regioes "
            "oficiais da POC para viabilizar aprendizado supervisionado."
        ),
    }
    return modelo, metadata


def salvar_modelo(modelo: Pipeline, metadata: dict) -> Path:
    ARQUIVO_MODELO.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"modelo": modelo, "metadata": metadata}, ARQUIVO_MODELO)
    ARQUIVO_METADADOS.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return ARQUIVO_MODELO


def carregar_modelo() -> tuple[Pipeline, dict]:
    if not ARQUIVO_MODELO.exists():
        raise FileNotFoundError(
            f"Modelo nao encontrado: {ARQUIVO_MODELO}. "
            "Execute: python ml/treinar_modelo.py"
        )
    pacote = joblib.load(ARQUIVO_MODELO)
    return pacote["modelo"], pacote["metadata"]


def predizer_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    modelo, metadata = carregar_modelo()
    features = metadata["features"]
    faltantes = [c for c in features if c not in df.columns]
    if faltantes:
        raise ValueError(f"Colunas ausentes para predicao: {faltantes}")

    entrada = df[features].apply(pd.to_numeric, errors="coerce")
    if entrada.isna().any().any():
        raise ValueError("Ha valores invalidos nos dados de entrada do modelo.")

    scores = modelo.predict(entrada)
    resultado = df.copy()
    resultado["score_ia_0_10"] = [_limitar_score(float(s)) for s in scores]
    resultado["classificacao_ia"] = resultado["score_ia_0_10"].map(classificar_score)
    resultado["origem_score_dashboard"] = "modelo_ia_treinado"
    return resultado.sort_values("score_ia_0_10", ascending=False).reset_index(drop=True)


def treinar_e_salvar() -> Path:
    if not ARQUIVO_RESULTADOS.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {ARQUIVO_RESULTADOS}. Execute a etapa 5 antes do treino."
        )
    df = pd.read_csv(ARQUIVO_RESULTADOS)
    modelo, metadata = treinar_modelo(df)
    return salvar_modelo(modelo, metadata)
