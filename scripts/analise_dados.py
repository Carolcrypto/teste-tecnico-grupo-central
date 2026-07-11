# ============================================================
# TESTE TÉCNICO - ANALISTA DE DADOS / BI
# NutriMax Distribuidora
#
# Objetivo:
# Preparar, validar e enriquecer a base de clientes para
# apoiar as análises de carteirização e visitação comercial.
# ============================================================


# ============================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# ============================================================

from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# 2. CONFIGURAÇÕES E LEITURA DAS BASES
# ============================================================

# Coordenadas da base operacional informadas no teste
# Vila Mariana - São Paulo
LATITUDE_BASE = -23.5875
LONGITUDE_BASE = -46.6396

# Raio de cobertura proposto
RAIO_KM = 25

# Caminho da raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Arquivos de entrada
ARQUIVO_CLIENTES = (
    BASE_DIR / "data" / "carteirizacao_sp_simulado.csv"
)

ARQUIVO_CUSTOS = (
    BASE_DIR / "data" / "custos_visitacao.csv"
)

# Arquivo de saída
ARQUIVO_SAIDA = (
    BASE_DIR / "data" / "carteirizacao_tratada.csv"
)


# Leitura das bases
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


# Validação inicial da leitura
print("\n========== LEITURA DAS BASES ==========")

print(f"Base de clientes: {clientes.shape[0]} linhas")
print(f"Base de clientes: {clientes.shape[1]} colunas")

print(f"\nBase de custos: {custos.shape[0]} linhas")
print(f"Base de custos: {custos.shape[1]} colunas")

print("\nBases carregadas com sucesso.")


# ============================================================
# 3. AUDITORIA DA QUALIDADE DOS DADOS
# ============================================================

print("\n========== AUDITORIA DOS DADOS ==========")


# ------------------------------------------------------------
# 3.1 Valores ausentes
# ------------------------------------------------------------

print("\n--- Valores ausentes por coluna ---")
print(clientes.isnull().sum())


# ------------------------------------------------------------
# 3.2 Registros duplicados
# ------------------------------------------------------------

linhas_duplicadas = clientes.duplicated().sum()

ids_duplicados = (
    clientes["id_cliente"]
    .duplicated()
    .sum()
)

print("\n--- Registros duplicados ---")

print(
    f"Linhas totalmente duplicadas: "
    f"{linhas_duplicadas}"
)

print(
    f"IDs de clientes duplicados: "
    f"{ids_duplicados}"
)


# ------------------------------------------------------------
# 3.3 Tipos dos dados
# ------------------------------------------------------------

print("\n--- Tipos dos dados ---")
print(clientes.dtypes)


# ------------------------------------------------------------
# 3.4 Valores das variáveis categóricas
# ------------------------------------------------------------

print("\n--- Valores únicos: Zona ---")
print(
    clientes["zona"]
    .value_counts(dropna=False)
)

print("\n--- Valores únicos: Canal de Venda ---")
print(
    clientes["canal_venda"]
    .value_counts(dropna=False)
)

print("\n--- Valores únicos: Já Visitado ---")
print(
    clientes["ja_visitado"]
    .value_counts(dropna=False)
)


# ------------------------------------------------------------
# 3.5 Validação das coordenadas geográficas
# ------------------------------------------------------------

latitude_ausente = (
    clientes["latitude"]
    .isnull()
    .sum()
)

longitude_ausente = (
    clientes["longitude"]
    .isnull()
    .sum()
)

print("\n--- Coordenadas ausentes ---")

print(
    f"Latitude ausente: "
    f"{latitude_ausente}"
)

print(
    f"Longitude ausente: "
    f"{longitude_ausente}"
)


# ------------------------------------------------------------
# 3.6 Resumo das variáveis numéricas
# ------------------------------------------------------------

print("\n--- Resumo numérico ---")

print(
    clientes[
        [
            "qtd_pedidos_12m",
            "faturamento_12m",
            "latitude",
            "longitude"
        ]
    ].describe()
)


# ------------------------------------------------------------
# 3.7 Identificação de faturamento negativo
# ------------------------------------------------------------

clientes_faturamento_negativo = clientes[
    clientes["faturamento_12m"] < 0
]

print("\n--- Faturamento negativo ---")

print(
    f"Clientes com faturamento negativo: "
    f"{len(clientes_faturamento_negativo)}"
)

if not clientes_faturamento_negativo.empty:

    print(
        clientes_faturamento_negativo[
            [
                "id_cliente",
                "nome_fantasia",
                "qtd_pedidos_12m",
                "faturamento_12m"
            ]
        ]
    )


# ============================================================
# 4. TRATAMENTO E PADRONIZAÇÃO
# ============================================================

print("\n========== TRATAMENTO DOS DADOS ==========")


# Preserva a base original
clientes_tratados = clientes.copy()


# ------------------------------------------------------------
# 4.1 Padronização dos nomes das colunas
# ------------------------------------------------------------

clientes_tratados.columns = (
    clientes_tratados.columns
    .str.strip()
    .str.lower()
)


# ------------------------------------------------------------
# 4.2 Conversão das datas
# ------------------------------------------------------------

clientes_tratados["data_cadastro"] = pd.to_datetime(
    clientes_tratados["data_cadastro"],
    errors="coerce"
)

clientes_tratados["data_ultima_compra"] = pd.to_datetime(
    clientes_tratados["data_ultima_compra"],
    errors="coerce"
)


# ------------------------------------------------------------
# 4.3 Padronização do canal de venda
# ------------------------------------------------------------

# Primeiro remove espaços extras
clientes_tratados["canal_venda"] = (
    clientes_tratados["canal_venda"]
    .str.strip()
)

# Corrige as variações identificadas durante a auditoria
padronizacao_canal = {
    "distribuidor": "Distribuidor",
    "loja fisica": "Loja Física",
    "Indicacao": "Indicação",
    "indicacao": "Indicação"
}

clientes_tratados["canal_venda"] = (
    clientes_tratados["canal_venda"]
    .replace(padronizacao_canal)
)


# ------------------------------------------------------------
# 4.4 Validação da padronização
# ------------------------------------------------------------

print("\n--- Canais após padronização ---")

print(
    clientes_tratados["canal_venda"]
    .value_counts()
)

print("\nTratamento e padronização concluídos.")


# ============================================================
# 5. CRIAÇÃO DAS VARIÁVEIS AUXILIARES
# ============================================================

print(
    "\n========== CRIAÇÃO DAS VARIÁVEIS AUXILIARES =========="
)


# ------------------------------------------------------------
# 5.1 Indicador de CEP preenchido
# ------------------------------------------------------------

clientes_tratados["possui_cep"] = np.where(
    clientes_tratados["cep"].notna()
    & clientes_tratados["cep"]
    .astype(str)
    .str.strip()
    .ne(""),
    "Sim",
    "Não"
)


# ------------------------------------------------------------
# 5.2 Função para cálculo da distância
# ------------------------------------------------------------

def calcular_distancia_haversine(
    lat_cliente,
    lon_cliente
):
    """
    Calcula a distância geográfica em linha reta,
    em quilômetros, entre cada cliente e a base
    operacional localizada na Vila Mariana.

    A função utiliza a fórmula de Haversine.
    """

    raio_terra_km = 6371

    lat_base = np.radians(LATITUDE_BASE)
    lon_base = np.radians(LONGITUDE_BASE)

    lat_cliente = np.radians(lat_cliente)
    lon_cliente = np.radians(lon_cliente)

    diferenca_lat = lat_cliente - lat_base
    diferenca_lon = lon_cliente - lon_base

    a = (
        np.sin(diferenca_lat / 2) ** 2
        + np.cos(lat_base)
        * np.cos(lat_cliente)
        * np.sin(diferenca_lon / 2) ** 2
    )

    c = 2 * np.arctan2(
        np.sqrt(a),
        np.sqrt(1 - a)
    )

    distancia = raio_terra_km * c

    return distancia


# ------------------------------------------------------------
# 5.3 Cálculo da distância até a Vila Mariana
# ------------------------------------------------------------

clientes_tratados["distancia_km"] = (
    calcular_distancia_haversine(
        clientes_tratados["latitude"],
        clientes_tratados["longitude"]
    )
    .round(2)
)


# ------------------------------------------------------------
# 5.4 Classificação dentro ou fora do raio de 25 km
# ------------------------------------------------------------

clientes_tratados["dentro_raio_25km"] = np.where(
    clientes_tratados["distancia_km"] <= RAIO_KM,
    "Sim",
    "Não"
)


# ============================================================
# 6. VALIDAÇÃO DAS VARIÁVEIS AUXILIARES
# ============================================================

print("\n--- Preenchimento do CEP ---")

print(
    clientes_tratados["possui_cep"]
    .value_counts()
)


print("\n--- Cobertura do raio de 25 km ---")

print(
    clientes_tratados["dentro_raio_25km"]
    .value_counts()
)


print("\n--- Resumo das distâncias ---")

print(
    clientes_tratados["distancia_km"]
    .describe()
)


print("\nVariáveis auxiliares criadas com sucesso.")


# ============================================================
# 7. EXPORTAÇÃO DA BASE TRATADA
# ============================================================

clientes_tratados.to_csv(
    ARQUIVO_SAIDA,
    index=False,
    sep=";",
    encoding="utf-8-sig"
)

print("\n========== EXPORTAÇÃO ==========")

print("Base tratada exportada com sucesso.")

print(
    f"Arquivo gerado em: "
    f"{ARQUIVO_SAIDA}"
)
