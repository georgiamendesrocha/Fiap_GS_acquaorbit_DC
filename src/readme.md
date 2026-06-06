# Código-fonte — Acqua Orbit DC

Todo o código, dados, modelos e saídas do projeto ficam em `src/`.

## Estrutura

| Pasta | Conteúdo |
|-------|----------|
| `api/` | Coleta NASA POWER |
| `pipeline/` | Etapas 02–09 do processamento |
| `ml/` | Treino e inferência de IA |
| `frontend/` | Dashboard Streamlit e HTML |
| `db/` | Conexão Oracle (`db.py`) |
| `config/` | Carregamento do `.env` (`carregar_env.py`) |
| `data/` | CSVs de entrada e resultados |
| `models/` | Modelo `.joblib` e metadados |
| `output/` | Relatórios, dashboards, PDF e capturas |
| `menu.py` | Menu interativo (atalho na raiz: `python menu.py`) |
| `paths.py` | Caminhos centralizados do projeto |

## Execução

```powershell
python menu.py
```
