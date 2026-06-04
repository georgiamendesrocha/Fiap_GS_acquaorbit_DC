# FIAP - Faculdade de Informatica e Administracao Paulista

# Acqua Orbit DC

## Grupo 13

## Integrantes

- Edemir Sufiatti - RM571375
- Carlos Magnus Costa Amaral - RM573978
- Georgia Mendes Rocha - RM573281
- Marina Leme Soares - RM570461
- Jocasta de Kacia Bortolacci - RM564730

## Professores

### Tutor(a)

- Nicolly Candida Rodrigues de Souza

### Coordenador(a)

- Andre Godoi Chiovato

## Descricao

O Acqua Orbit DC e uma prova de conceito academica desenvolvida para a Global Solution 2026.1 da FIAP. A proposta utiliza dados climaticos por coordenadas geograficas, analise de dados em Python, indicadores ambientais, sensores simulados e criterios de infraestrutura critica digital para comparar regioes candidatas a instalacao ou operacao de data centers sustentaveis e resilientes.

A POC avalia tres regioes oficiais:

- Barueri/Tambore - SP
- Rio de Janeiro - eixo Barra/Jacarepagua/Parque Olimpico - RJ
- Curitiba - PR

O projeto usa dados climaticos publicos da NASA POWER para o periodo de referencia de 2025 e organiza os resultados em CSVs, relatorios Markdown e um dashboard HTML simples. A classificacao final das regioes considera risco ambiental e climatico, potencial de reuso pluvial, qualidade simulada da agua, conectividade critica, disponibilidade energetica, refrigeracao e criterios ESG/resiliencia.

A solucao nao substitui laudos tecnicos, auditorias ESG, estudos ambientais ou projetos profissionais de data center. Ela funciona como uma ferramenta academica de apoio a decisao e demonstracao tecnica.

## Objetivo

Responder, dentro do contexto da economia espacial, como dados climaticos e geograficos podem apoiar decisoes sustentaveis na Terra. No caso da POC, esses dados sao aplicados a uma comparacao simplificada de regioes para data centers.

## Tecnologias utilizadas

- Python
- Pandas
- Requests
- CSV
- Oracle opcional
- HTML e SVG
- Dados climaticos NASA POWER
- Simulacao de sensores de agua
- Regras explicaveis para classificacao final

## Estrutura de pastas

- `data`: arquivos CSV de entrada, bases tratadas e resultados finais.
- `database`: scripts SQL, consultas Oracle e documentacao da modelagem relacional opcional.
- `config`: exemplo de configuracao das variaveis de ambiente Oracle.
- `output`: relatorios gerados e dashboard HTML da POC.
- `scripts`: scripts das etapas de tratamento, montagem, validacao, calculo e visualizacao.
- `nasa_power_pipeline.py`: script opcional para extrair dados climaticos da NASA POWER.
- `requirements.txt`: dependencias Python do projeto.
- `README.md`: guia geral do projeto.

## Principais arquivos gerados

- `data/nasa_power_2025_diario_tratado.csv`: base diaria tratada com dados climaticos de 2025.
- `data/regioes.csv`: base oficial da POC com dados climaticos, ambientais e de infraestrutura.
- `data/resultados_regioes.csv`: resultado final com sensores simulados, indices e classificacao.
- `output/dashboard_poc.html`: dashboard simples para visualizacao dos resultados.
- `output/relatorio_resultados_poc.md`: relatorio da classificacao final da POC.
- `output/relatorio_visualizacoes_poc.md`: relatorio da etapa de visualizacao.
- `database/01_criar_tabelas_oracle.sql`: estrutura Oracle opcional.
- `database/02_consultas_oracle.sql`: consultas SQL para validacao e demonstracao no Oracle.
- `database/03_modelagem_dados.md`: descricao tecnica da modelagem Oracle.
- `output/fallback_csv`: arquivos gerados quando Oracle nao esta configurado.

## Como executar o projeto

### 1. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 2. Opcional: baixar novamente os dados climaticos da NASA POWER

Esta etapa exige acesso a internet. O projeto ja possui uma base CSV salva em `data/nasa_power_2025_diario.csv`.

```powershell
python nasa_power_pipeline.py
```

### 3. Tratar os dados climaticos diarios

```powershell
python scripts\02_tratar_dados_climaticos.py
```

### 4. Montar o CSV oficial da POC

```powershell
python scripts\03_montar_regioes_csv.py
```

### 5. Validar o CSV oficial

```powershell
python scripts\04_validar_regioes_csv.py
```

### 6. Calcular os resultados finais

```powershell
python scripts\05_calcular_resultados_poc.py
```

### 7. Gerar o dashboard HTML

```powershell
python scripts\06_gerar_visualizacoes.py
```

Depois da execucao, abra o arquivo abaixo no navegador:

```text
output/dashboard_poc.html
```

### 8. Persistir resultados sem Oracle usando fallback CSV

Se as credenciais Oracle nao estiverem configuradas, o script usa fallback automatico em CSV. Esse modo permite executar a POC mesmo sem banco de dados:

```powershell
python scripts\07_persistir_oracle_csv.py
```

Arquivos gerados no fallback:

```text
output/fallback_csv/ao_regioes.csv
output/fallback_csv/ao_indicadores.csv
output/fallback_csv/ao_resultados_poc.csv
```

Saida esperada no terminal:

```text
Persistencia concluida em modo: CSV fallback
```

### 9. Opcional: executar com Oracle via SQL Developer e terminal

O Oracle e opcional. Para usar banco de dados, e necessario criar as tabelas no Oracle SQL Developer e configurar as credenciais no terminal.

#### 9.1. Criar ou recriar as tabelas no Oracle SQL Developer

Atencao: o script `database/01_criar_tabelas_oracle.sql` e reexecutavel para a POC. Ele remove as tabelas `AO_RESULTADOS_POC`, `AO_INDICADORES` e `AO_REGIOES` se elas ja existirem e depois cria tudo novamente.

Use esse script quando quiser preparar a base do zero antes de carregar os dados.

1. Abra o Oracle SQL Developer.
2. Conecte usando suas credenciais da FIAP.
3. Clique com o botao direito na conexao e escolha `Open SQL Worksheet` ou `Abrir Planilha SQL`.
4. Abra o arquivo abaixo no projeto:

```text
database/01_criar_tabelas_oracle.sql
```

5. Copie todo o conteudo do arquivo SQL.
6. Cole na planilha SQL do Oracle SQL Developer.
7. Execute com o botao de run ou com `Ctrl + Enter`.

Saida esperada no SQL Developer:

```text
Procedimento PL/SQL concluido com sucesso.
Table AO_REGIOES criado.
Table AO_INDICADORES criado.
Table AO_RESULTADOS_POC criado.
```

#### 9.2. Configurar credenciais com `.env`

O arquivo `config/oracle.example.env` mostra o formato esperado das credenciais. Para uso local, crie um arquivo chamado `.env` na raiz do projeto, ao lado do `README.md`.

Exemplo de `.env`:

```env
ORACLE_USER=RM000000
ORACLE_PASSWORD=sua_senha
ORACLE_DSN=oracle.fiap.com.br:1521/ORCL
```

O arquivo `.env` contem senha e nao deve ser enviado ao GitHub. Ele ja esta protegido pelo `.gitignore`.

#### 9.3. Carregar o `.env` no PowerShell

No terminal PowerShell, dentro da raiz do projeto, execute:

```powershell
Get-Content .env | ForEach-Object {
    if ($_ -and -not $_.Trim().StartsWith("#") -and $_ -match "=") {
        $partes = $_ -split "=", 2
        Set-Item -Path "Env:$($partes[0].Trim())" -Value $partes[1].Trim().Trim('"')
    }
}
```

Confira se o usuario carregou:

```powershell
$env:ORACLE_USER
```

Saida esperada:

```text
RM573281
```

#### 9.4. Persistir dados no Oracle

Com as tabelas criadas e o `.env` carregado, execute:

```powershell
python scripts\07_persistir_oracle_csv.py
```

Saida esperada:

```text
Persistencia concluida em modo: Oracle
```

Se aparecer `CSV fallback`, verifique se o `.env` foi carregado, se o pacote `oracledb` esta instalado e se usuario, senha e DSN estao corretos.

#### 9.5. Consultar pelo Oracle SQL Developer

Na planilha SQL do Oracle SQL Developer, voce pode executar uma consulta direta:

```sql
SELECT
    r.CIDADE,
    r.ESTADO,
    p.SCORE_FINAL,
    p.CLASS_FINAL
FROM AO_REGIOES r
JOIN AO_RESULTADOS_POC p
    ON p.REGIAO_ID = r.REGIAO_ID
ORDER BY p.SCORE_FINAL DESC;
```

Saida esperada:

```text
Barueri        SP  7,11  favoravel
Curitiba       PR  6,81  atencao
Rio de Janeiro RJ  5,92  atencao
```

Tambem existe um arquivo com consultas prontas para validacao e apresentacao:

```text
database/02_consultas_oracle.sql
```

Para usar, abra o arquivo, copie uma consulta por vez na planilha SQL do Oracle SQL Developer e execute. As consultas verificam quantidade de registros, ranking final, sensores simulados, risco ambiental, reuso pluvial e resiliencia ESG.

#### 9.6. Consultar pelo terminal

Depois de carregar o `.env`, tambem e possivel consultar o Oracle pelo terminal:

```powershell
python scripts\08_consultar_resultados_oracle.py
```

Saida esperada:

```text
Ranking Oracle - Acqua Orbit DC
--------------------------------
Barueri / SP | score 7.11 | favoravel
Curitiba / PR | score 6.81 | atencao
Rio de Janeiro / RJ | score 5.92 | atencao
```

### 10. Instalar o driver Oracle, se necessario

O pacote `oracledb` ja esta listado em `requirements.txt`. Se precisar instalar separadamente:

```powershell
pip install oracledb
```

## Fluxo da solucao

1. Extracao ou uso da base diaria NASA POWER.
2. Tratamento dos dados climaticos diarios.
3. Montagem do `regioes.csv` com indicadores regionais.
4. Validacao estrutural do `regioes.csv`.
5. Calculo de sensores simulados, indices finais e classificacao.
6. Geracao de dashboard HTML para apresentacao.
7. Persistencia opcional em Oracle ou fallback automatico em CSV.

## Origem dos dados

- Dados climaticos: reais, obtidos da NASA POWER.
- Riscos ambientais: parametrizados para fins academicos.
- Reuso pluvial: calculado a partir da precipitacao e de area/capacidade simuladas.
- Sensores de agua: simulados por regras deterministicas.
- Infraestrutura critica digital: parametrizada.
- Classificacao final: calculada por regras explicaveis.
- Persistencia: Oracle opcional ou CSV como fallback automatico.

## Resultado atual da POC

Ranking gerado pela etapa 05:

1. Barueri/Tambore - favoravel
2. Curitiba - atencao
3. Rio de Janeiro - Barra/Jacarepagua/Parque Olimpico - atencao

## Limites da solucao

O Acqua Orbit DC e uma POC academica. Ele nao realiza engenharia real de data center, analise hidrologica profissional, auditoria ESG, licenciamento ambiental, analise profissional de telecomunicacoes ou estudo tecnico de energia. Os sensores sao simulados e os indicadores parametrizados devem ser entendidos como demonstracao metodologica.

## Historico de lancamentos

- 0.8.0 - 04/06/2026
  - Refinamento da modelagem Oracle, criacao de consultas SQL e documentacao tecnica da camada relacional.
- 0.7.0 - 04/06/2026
  - Inclusao da persistencia opcional em Oracle e fallback automatico em CSV.
- 0.6.0 - 04/06/2026
  - Criacao do dashboard HTML da POC.
- 0.5.0 - 04/06/2026
  - Calculo dos resultados finais, sensores simulados e classificacao.
- 0.4.0 - 04/06/2026
  - Montagem e validacao do `regioes.csv`.
- 0.3.0 - 04/06/2026
  - Tratamento dos dados climaticos diarios.
- 0.2.0 - 03/06/2026
  - Extracao e organizacao dos dados NASA POWER.
- 0.1.0 - 03/06/2026
  - Definicao da proposta Acqua Orbit DC.

## Licenca

Projeto academico desenvolvido para a FIAP Global Solution 2026.1. Uso restrito para fins educacionais.
