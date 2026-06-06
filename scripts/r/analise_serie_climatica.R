# Acqua Orbit DC - Analise de series temporais (disciplina R)
# Le serie diaria NASA POWER, identifica anomalias e gera relatorio + graficos.

suppressPackageStartupMessages({
  if (!requireNamespace("jsonlite", quietly = TRUE)) {
    install.packages("jsonlite", repos = "https://cloud.r-project.org")
  }
})

raiz <- Sys.getenv("ACQUA_ROOT", unset = NA_character_)
if (is.na(raiz) || !dir.exists(raiz)) {
  raiz <- normalizePath(file.path(getwd(), "..", ".."), winslash = "/", mustWork = FALSE)
  if (!file.exists(file.path(raiz, "README.md"))) {
    raiz <- normalizePath(getwd(), winslash = "/")
  }
}

arquivo_csv <- file.path(raiz, "src", "data", "nasa_power_2025_diario_tratado.csv")
dir_saida <- file.path(raiz, "src", "output")
dir_graficos <- file.path(dir_saida, "r_graficos")

if (!file.exists(arquivo_csv)) {
  stop(paste("Arquivo nao encontrado:", arquivo_csv, "- Execute a etapa 2 do pipeline."))
}

dir.create(dir_graficos, recursive = TRUE, showWarnings = FALSE)

dados <- read.csv(arquivo_csv, stringsAsFactors = FALSE, fileEncoding = "UTF-8")
dados$data <- as.Date(dados$data)

detectar_anomalias <- function(valores, nome_var) {
  media <- mean(valores, na.rm = TRUE)
  desvio <- sd(valores, na.rm = TRUE)
  if (is.na(desvio) || desvio == 0) {
    return(data.frame())
  }
  z <- (valores - media) / desvio
  idx <- which(abs(z) > 2)
  if (length(idx) == 0) {
    return(data.frame())
  }
  data.frame(
    variavel = nome_var,
    indice = idx,
    valor = round(valores[idx], 2),
    z_score = round(z[idx], 2),
    stringsAsFactors = FALSE
  )
}

regioes <- unique(dados$regiao)
linhas_relatorio <- c(
  "# Relatorio R - Series temporais climaticas",
  "",
  "## Disciplina",
  "",
  "Statistical Computing with R - Series Temporais (analise de padroes e anomalias).",
  "",
  "## Entrada",
  "",
  "- `src/data/nasa_power_2025_diario_tratado.csv`",
  paste0("- Registros: ", nrow(dados)),
  paste0("- Regioes: ", length(regioes)),
  "",
  "## Metodo",
  "",
  "- Agregacao diaria por regiao (temperatura media e precipitacao).",
  "- Deteccao de anomalias por z-score (|z| > 2).",
  "- Graficos PNG em `src/output/r_graficos/`.",
  "",
  "## Resultados por regiao",
  ""
)

resumo_json <- list(
  gerado_em = format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
  registros = nrow(dados),
  regioes = as.list(regioes),
  anomalias = list()
)

for (regiao in regioes) {
  subset <- dados[dados$regiao == regiao, ]
  subset <- subset[order(subset$data), ]

  linhas_relatorio <- c(
    linhas_relatorio,
    paste0("### ", regiao),
    "",
    paste0("- Dias analisados: ", nrow(subset)),
    paste0(
      "- Temperatura media anual (serie diaria): ",
      round(mean(subset$temp_media, na.rm = TRUE), 2), " C"
    ),
    paste0(
      "- Precipitacao acumulada: ",
      round(sum(subset$precipitacao_diaria_mm, na.rm = TRUE), 2), " mm"
    ),
    ""
  )

  png_temp <- file.path(
    dir_graficos,
    paste0("serie_temp_", gsub("[^A-Za-z0-9]+", "_", regiao), ".png")
  )
  png(png_temp, width = 900, height = 480, res = 110)
  plot(
    subset$data,
    subset$temp_media,
    type = "l",
    col = "#0f8b8d",
    lwd = 2,
    main = paste("Serie temporal - Temperatura media -", regiao),
    xlab = "Data",
    ylab = "Temp. media (C)"
  )
  grid()
  dev.off()

  png_chuva <- file.path(
    dir_graficos,
    paste0("serie_precip_", gsub("[^A-Za-z0-9]+", "_", regiao), ".png")
  )
  png(png_chuva, width = 900, height = 480, res = 110)
  plot(
    subset$data,
    subset$precipitacao_diaria_mm,
    type = "l",
    col = "#d95d39",
    lwd = 2,
    main = paste("Serie temporal - Precipitacao diaria -", regiao),
    xlab = "Data",
    ylab = "Precipitacao (mm)"
  )
  grid()
  dev.off()

  anomalias <- rbind(
    detectar_anomalias(subset$temp_media, "temp_media"),
    detectar_anomalias(subset$precipitacao_diaria_mm, "precipitacao_diaria_mm")
  )

  if (nrow(anomalias) > 0) {
    anomalias$data <- as.character(subset$data[anomalias$indice])
    resumo_json$anomalias[[regiao]] <- anomalias
    linhas_relatorio <- c(
      linhas_relatorio,
      "#### Anomalias detectadas (|z| > 2)",
      "",
      paste0(
        "- Total: ",
        nrow(anomalias),
        " (temperatura e/ou precipitacao)"
      ),
      ""
    )
    for (i in seq_len(min(5, nrow(anomalias)))) {
      linhas_relatorio <- c(
        linhas_relatorio,
        paste0(
          "  - ",
          anomalias$data[i],
          " | ",
          anomalias$variavel[i],
          " = ",
          anomalias$valor[i],
          " (z = ",
          anomalias$z_score[i],
          ")"
        )
      )
    }
    if (nrow(anomalias) > 5) {
      linhas_relatorio <- c(linhas_relatorio, paste0("  - ... (+", nrow(anomalias) - 5, " eventos)"))
    }
  } else {
    resumo_json$anomalias[[regiao]] <- data.frame()
    linhas_relatorio <- c(
      linhas_relatorio,
      "#### Anomalias detectadas",
      "",
      "- Nenhuma anomalia com |z| > 2 nesta regiao.",
      ""
    )
  }

  linhas_relatorio <- c(
    linhas_relatorio,
    "#### Graficos",
    "",
    paste0("- `", basename(png_temp), "`"),
    paste0("- `", basename(png_chuva), "`"),
    ""
  )
}

linhas_relatorio <- c(
  linhas_relatorio,
  "## Uso no projeto",
  "",
  "A serie diaria alimenta a etapa 3 (regioes.csv), os dashboards e o painel Streamlit (aba Clima).",
  "A deteccao de anomalias apoia a leitura de riscos climaticos na POC.",
  ""
)

arquivo_md <- file.path(dir_saida, "r_relatorio_series_temporais.md")
arquivo_json <- file.path(dir_saida, "r_resumo_series_temporais.json")
writeLines(linhas_relatorio, arquivo_md, useBytes = TRUE)
jsonlite::write_json(resumo_json, arquivo_json, pretty = TRUE, auto_unbox = TRUE)

cat("Analise R concluida.\n")
cat("-", arquivo_md, "\n")
cat("-", arquivo_json, "\n")
cat("- Graficos em:", dir_graficos, "\n")
