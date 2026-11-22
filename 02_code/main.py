# -*- coding: utf-8 -*-
"""
Lê as temperaturas das pastas informadas, gera CSVs com vírgula como decimal
e salva gráficos (curvas individuais e média±desvio das triplicatas).

Compatível com Excel PT-BR: usa sep=';' e decimal=','.
Sem dependência de 'natsort' (usa ordenação natural implementada aqui).
"""

import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.close("all")

# ================================
# CONFIGURAÇÕES
# ================================
# Intervalo (s) entre frames/linhas (ajuste se necessário)
DT = 0.111

# Pastas com as medições (ajuste ou acrescente mais se precisar)
ROOT_FOLDERS = [
 
   r"2-ITA=49,9-Sexta Pele (Branca com Pinta)\660nm + 808nm\IR_07433",
   r"2-ITA=49,9-Sexta Pele (Branca com Pinta)\660nm + 808nm\IR_07434",
   r"2-ITA=49,9-Sexta Pele (Branca com Pinta)\660nm + 808nm\IR_07435",
]

# Nome do CSV de média/DP gerado a cada triplicata
TRIPLICATA_NOME = "dado.csv"

# Pasta onde os PNGs serão salvos (ao lado dos CSVs)
FIGS_SUBPASTA = "figuras"


# ================================
# FUNÇÕES AUXILIARES
# ================================
def natural_key(s: str):
    """
    Chave de ordenação "natural" (IR_1, IR_2, IR_10) sem usar natsort.
    Divide a string em blocos de números e texto para ordenar como humanos.
    """
    parts = re.split(r'(\d+)', s)
    key = []
    for p in parts:
        if p.isdigit():
            key.append(int(p))
        else:
            key.append(p.lower())
    return tuple(key)


def parse_temperature_from_line(texto: str) -> float:
    """
    Procura o ÚLTIMO número na linha, aceitando vírgula ou ponto como decimal.
    Ex.: '... 33,56 ...' -> 33.56  |  '... 33.56 ...' -> 33.56
    """
    matches = re.findall(r'[-+]?\d+(?:[.,]\d+)?', texto)
    if not matches:
        raise ValueError("Não encontrei número na linha para extrair temperatura.")
    raw = matches[-1].replace(",", ".")
    return float(raw)


def ler_temperaturas_de_pasta(pasta: str):
    """
    Lê todos os arquivos (somente arquivos, ignora subpastas) na pasta,
    em ordem natural, e extrai a temperatura a partir da linha 5 (índice 4).
    Se a linha 5 não existir, faz fallback para todo o conteúdo.
    """
    if not os.path.isdir(pasta):
        raise FileNotFoundError(f"Pasta não encontrada: {pasta}")

    arquivos = [f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]
    arquivos = sorted(arquivos, key=natural_key)

    temps = []
    for nome in arquivos:
        caminho = os.path.join(pasta, nome)
        with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
            linhas = f.readlines()

        if len(linhas) >= 5:
            fonte = linhas[4]
        else:
            # Fallback: usa todo o conteúdo se não houver linha 5
            fonte = " ".join(linhas)

        temp = parse_temperature_from_line(fonte)
        temps.append(temp)

    return temps, arquivos


def salvar_csv_individual(pasta_raiz: str, nome_pasta: str, tempo_s: np.ndarray, temperaturas_c: np.ndarray):
    """
    Salva CSV individual com vírgula como decimal e ';' como separador.
    """
    df = pd.DataFrame({
        "Tempo (s)": tempo_s,
        "Temperatura (°C)": temperaturas_c
    })
    saida_csv = os.path.join(pasta_raiz, f"{nome_pasta}.csv")
    df.to_csv(saida_csv, index=False, sep=";", decimal=",", encoding="utf-8")
    return saida_csv


def salvar_fig_individual(pasta_raiz: str, nome_pasta: str, tempo_s: np.ndarray, temperaturas_c: np.ndarray, titulo: str):
    """
    Salva PNG da curva individual na subpasta 'figuras'.
    """
    figs_dir = os.path.join(pasta_raiz, FIGS_SUBPASTA)
    os.makedirs(figs_dir, exist_ok=True)
    saida_png = os.path.join(figs_dir, f"{nome_pasta}.png")

    plt.figure()
    plt.plot(tempo_s, temperaturas_c)
    plt.xlabel("Tempo (s)")
    plt.ylabel("Temperatura (°C)")
    plt.title(titulo)
    plt.tight_layout()
    plt.savefig(saida_png, dpi=150)
    plt.close()
    return saida_png


def salvar_triplicata(pasta_raiz: str, tempo_s: np.ndarray, triplicata: list):
    """
    A partir de 3 listas (triplicata), corta pelo mínimo comprimento, calcula média/DP,
    salva CSV (decimal=',') e PNG (média ± DP).
    """
    nmin = min(len(lst) for lst in triplicata)
    blocos = np.array([lst[:nmin] for lst in triplicata], dtype=float)

    media = blocos.mean(axis=0)
    desvio = blocos.std(axis=0)
    tempo_cortado = tempo_s[:nmin]

    # CSV com vírgula como decimal e ';' como separador
    df = pd.DataFrame({
        "Tempo (s)": tempo_cortado,
        "Média (°C)": media,
        "Desvio padrão (°C)": desvio
    })
    saida_csv = os.path.join(pasta_raiz, TRIPLICATA_NOME)
    df.to_csv(saida_csv, index=False, sep=";", decimal=",", encoding="utf-8")

    # Figura média ± DP
    figs_dir = os.path.join(pasta_raiz, FIGS_SUBPASTA)
    os.makedirs(figs_dir, exist_ok=True)
    saida_png = os.path.join(figs_dir, "triplicata_media_dp.png")

    plt.figure()
    plt.fill_between(tempo_cortado, media - desvio, media + desvio, alpha=0.2, label="Desvio padrão")
    plt.plot(tempo_cortado, media, label="Média")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Temperatura (°C)")
    plt.title("Média ± Desvio (Triplicata)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(saida_png, dpi=150)
    plt.close()

    return saida_csv, saida_png


# ================================
# EXECUÇÃO
# ================================
triplicata_buffer = []
for idx, pasta in enumerate(ROOT_FOLDERS):
    # pasta_raiz = diretório pai da pasta do IR_XXXXX (onde salvaremos CSV/figuras)
    pasta_raiz = os.path.dirname(pasta)
    nome_pasta = os.path.basename(pasta)

    # Lê temperaturas e nomes de arquivos (em ordem natural)
    temps, _ = ler_temperaturas_de_pasta(pasta)

    # Eixo do tempo (começa em 0 com passo DT)
    t = np.arange(len(temps)) * DT
    data = np.array(temps, dtype=float)

    # Salvar CSV individual (vírgula como decimal)
    salvar_csv_individual(pasta_raiz, nome_pasta, t, data)

    # Título com amostra + experimento (sem depender de chdir)
    sample_name = os.path.basename(os.path.dirname(pasta_raiz))  # nome da amostra
    exp_name = os.path.basename(pasta_raiz)                      # nome do experimento
    titulo = f"{sample_name}\n{exp_name}"

    # Salvar figura individual
    salvar_fig_individual(pasta_raiz, nome_pasta, t, data, titulo)

    # Monta triplicata
    triplicata_buffer.append(data)
    # A cada 3 pastas, gera média/DP
    if (idx + 1) % 3 == 0:
        salvar_triplicata(pasta_raiz, t, triplicata_buffer)
        triplicata_buffer = []

print("✅ Concluído: CSVs com decimal vírgula e figuras PNG foram gerados ao lado das pastas.")
