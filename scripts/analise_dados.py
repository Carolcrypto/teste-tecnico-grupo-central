from pathlib import Path
import pandas as pd
import numpy as np

# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Localização da base operacional: Vila Mariana - São Paulo
LATITUDE_BASE = -23.5875
LONGITUDE_BASE = -46.6396
RAIO_KM = 25

# Caminho da raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Arquivos de entrada
ARQUIVO_CLIENTES = BASE_DIR / "data" / "carteirizacao_sp_simulado.csv"
ARQUIVO_CUSTOS = BASE_DIR / "data" / "custos_visitacao.csv"

# Arquivo de saída
ARQUIVO_SAIDA = BASE_DIR / "data" / "carteirizacao_tratada.csv"


# ============================================================
# LEITURA DOS DADOS
# ============================================================

clientes = pd.read_csv(
    ARQUIVO_CLIENTES,
    sep=";",
    encoding="utf-8"
)

custos = pd.read_csv(
    ARQUIVO_CUSTOS,
    sep=";",
    encoding="utf-8"
)

print("Bases carregadas com sucesso.")
print(f"Total de clientes: {len(clientes)}")


# ============================================================
# TRATAMENTO INICIAL
# ============================================================

# Remove espaços extras dos nomes das colunas
clientes.columns = clientes.columns.str.strip()
custos.columns = custos.columns.str.strip()

# Converte as datas
clientes["data_cadastro"] = pd.to_datetime(
    clientes["data_cadastro"],
    errors="coerce"
)

clientes["data_ultima_compra"] = pd.to_datetime(
    clientes["data_ultima_compra"],
    errors="coerce"
)

# Identifica se o cliente possui CEP preenchido
clientes["possui_cep"] = np.where(
    clientes["cep"].notna() &
    clientes["cep"].astype(str).str.strip().ne(""),
    "Sim",
    "Não"
)


# ============================================================
# CÁLCULO DA DISTÂNCIA - FÓRMULA DE HAVERSINE
# ============================================================

def calcular_distancia(lat_cliente, lon_cliente):
    """
    Calcula a distância em quilômetros entre o cliente
    e a base operacional localizada na Vila Mariana.
    """

    raio_terra = 6371

    lat1 = np.radians(LATITUDE_BASE)
    lon1 = np.radians(LONGITUDE_BASE)

    lat2 = np.radians(lat_cliente)
    lon2 = np.radians(lon_cliente)

    diferenca_lat = lat2 - lat1
    diferenca_lon = lon2 - lon1

    a = (
        np.sin(diferenca_lat / 2) ** 2
        + np.cos(lat1)
        * np.cos(lat2)
        * np.sin(diferenca_lon / 2) ** 2
    )

    c = 2 * np.arctan2(
        np.sqrt(a),
        np.sqrt(1 - a)
    )

    return raio_terra * c


clientes["distancia_km"] = calcular_distancia(
    clientes["latitude"],
    clientes["longitude"]
)

# Arredonda a distância para duas casas decimais
clientes["distancia_km"] = clientes["distancia_km"].round(2)


# ============================================================
# CLASSIFICAÇÃO DO RAIO DE COBERTURA
# ============================================================

clientes["dentro_raio_25km"] = np.where(
    clientes["distancia_km"] <= RAIO_KM,
    "Sim",
    "Não"
)


# ============================================================
# INDICADORES PRINCIPAIS
# ============================================================

total_clientes = len(clientes)

clientes_com_cep = (
    clientes["possui_cep"] == "Sim"
).sum()

clientes_dentro_raio = (
    clientes["dentro_raio_25km"] == "Sim"
).sum()

faturamento_total = clientes["faturamento_12m"].sum()

faturamento_dentro_raio = clientes.loc[
    clientes["dentro_raio_25km"] == "Sim",
    "faturamento_12m"
].sum()

percentual_clientes_raio = (
    clientes_dentro_raio / total_clientes * 100
)

percentual_faturamento_raio = (
    faturamento_dentro_raio / faturamento_total * 100
)


# ============================================================
# RESULTADOS NO TERMINAL
# ============================================================

print("\n========== RESUMO DA ANÁLISE ==========")

print(f"Total de clientes: {total_clientes}")

print(
    f"Clientes com CEP: "
    f"{clientes_com_cep} "
    f"({clientes_com_cep / total_clientes * 100:.1f}%)"
)

print(
    f"Clientes dentro do raio de 25 km: "
    f"{clientes_dentro_raio} "
    f"({percentual_clientes_raio:.1f}%)"
)

print(
    f"Faturamento total: "
    f"R$ {faturamento_total:,.2f}"
)

print(
    f"Faturamento dentro do raio: "
    f"R$ {faturamento_dentro_raio:,.2f} "
    f"({percentual_faturamento_raio:.1f}%)"
)


# ============================================================
# EXPORTAÇÃO DA BASE TRATADA
# ============================================================

clientes.to_csv(
    ARQUIVO_SAIDA,
    index=False,
    sep=";",
    encoding="utf-8-sig"
)

print("\nBase tratada exportada com sucesso:")
print(ARQUIVO_SAIDA)
