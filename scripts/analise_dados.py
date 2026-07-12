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
# 4.0 Padronização dos nomes das colunas
# ------------------------------------------------------------

clientes_tratados.columns = (
    clientes_tratados.columns
    .str.strip()
    .str.lower()
)

# ------------------------------------------------------------
# 4.1 Correção de IDs duplicados
# ------------------------------------------------------------

# Identifica apenas as ocorrências repetidas,
# preservando o primeiro registro de cada ID
mascara_ids_duplicados = clientes_tratados[
    "id_cliente"
].duplicated(keep="first")

# Descobre o maior número de ID já existente
maior_id = (
    clientes_tratados["id_cliente"]
    .str.extract(r"(\d+)")
    [0]
    .astype(int)
    .max()
)

# Gera novos IDs únicos para os registros duplicados
novos_ids = [
    f"CLI-{numero:04d}"
    for numero in range(
        maior_id + 1,
        maior_id + 1 + mascara_ids_duplicados.sum()
    )
]

# Substitui somente as ocorrências duplicadas
clientes_tratados.loc[
    mascara_ids_duplicados,
    "id_cliente"
] = novos_ids

# Validação
print("\n--- Correção dos IDs duplicados ---")
print(
    f"IDs duplicados após correção: "
    f"{clientes_tratados['id_cliente'].duplicated().sum()}"
)

print(
    f"Total de clientes únicos após correção: "
    f"{clientes_tratados['id_cliente'].nunique()}"
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

# ============================================================
# 8. ANÁLISE DA COBERTURA DO RAIO DE 25 KM
# ============================================================

total_clientes = clientes_tratados["id_cliente"].nunique()

clientes_dentro_raio = (
    clientes_tratados["dentro_raio_25km"] == "Sim"
).sum()

percentual_clientes_raio = (
    clientes_dentro_raio / total_clientes * 100
)

faturamento_total = clientes_tratados["faturamento_12m"].sum()

faturamento_dentro_raio = clientes_tratados.loc[
    clientes_tratados["dentro_raio_25km"] == "Sim",
    "faturamento_12m"
].sum()

percentual_faturamento_raio = (
    faturamento_dentro_raio / faturamento_total * 100
)

print("=== COBERTURA DA CARTEIRA PROPOSTA ===")
print(f"Total de clientes: {total_clientes}")
print(f"Clientes dentro do raio: {clientes_dentro_raio}")
print(f"Cobertura de clientes: {percentual_clientes_raio:.1f}%")

print(f"\nFaturamento total: R$ {faturamento_total:,.2f}")
print(f"Faturamento dentro do raio: R$ {faturamento_dentro_raio:,.2f}")
print(f"Cobertura do faturamento: {percentual_faturamento_raio:.1f}%")

# ============================================================
# 9. ANÁLISE: VISITADOS X NÃO VISITADOS
# ============================================================

analise_visitacao = (
    clientes_tratados
    .groupby("ja_visitado")
    .agg(
        total_clientes=("id_cliente", "nunique"),
        faturamento_total=("faturamento_12m", "sum"),
        faturamento_medio=("faturamento_12m", "mean"),
        faturamento_mediano=("faturamento_12m", "median"),
        media_pedidos=("qtd_pedidos_12m", "mean")
    )
    .round(2)
)

# Médias de faturamento
media_visitados = clientes_tratados.loc[
    clientes_tratados["ja_visitado"] == "Sim",
    "faturamento_12m"
].mean()

media_nao_visitados = clientes_tratados.loc[
    clientes_tratados["ja_visitado"] == "Não",
    "faturamento_12m"
].mean()

# Diferença percentual
diferenca_percentual = (
    (media_visitados - media_nao_visitados)
    / media_nao_visitados
    * 100
)

# Exibição dos resultados
print("=== VISITADOS X NÃO VISITADOS ===")
print(analise_visitacao)

print("\n=== COMPARAÇÃO DO FATURAMENTO MÉDIO ===")
print(
    f"Faturamento médio dos visitados: "
    f"R$ {media_visitados:,.2f}"
)

print(
    f"Faturamento médio dos não visitados: "
    f"R$ {media_nao_visitados:,.2f}"
)

print(
    f"Diferença percentual: "
    f"{diferenca_percentual:.1f}%"
)

# ============================================================
# 10. CLIENTES DE ALTO VALOR FORA DO RAIO
# ============================================================

# Define como alto valor os clientes com faturamento
# igual ou superior ao percentil 80 da base
limite_alto_valor = (
    clientes_tratados["faturamento_12m"]
    .quantile(0.80)
)

# Cria a classificação de alto valor
clientes_tratados["alto_valor"] = np.where(
    clientes_tratados["faturamento_12m"] >= limite_alto_valor,
    "Sim",
    "Não"
)

# Identifica clientes que atendem simultaneamente aos critérios:
# alto valor, nunca visitados e fora do raio de 25 km
clientes_prioritarios_fora_raio = (
    clientes_tratados[
        (clientes_tratados["alto_valor"] == "Sim")
        & (clientes_tratados["ja_visitado"] == "Não")
        & (clientes_tratados["dentro_raio_25km"] == "Não")
    ]
    .sort_values(
        "faturamento_12m",
        ascending=False
    )
)

# Indicadores
quantidade_prioritarios = len(
    clientes_prioritarios_fora_raio
)

faturamento_prioritarios = (
    clientes_prioritarios_fora_raio[
        "faturamento_12m"
    ].sum()
)

# Exibição dos resultados
print(
    "=== CLIENTES DE ALTO VALOR, "
    "NUNCA VISITADOS E FORA DO RAIO ==="
)

print(
    f"\nLimite para classificação como alto valor: "
    f"R$ {limite_alto_valor:,.2f}"
)

print(
    f"Quantidade de clientes prioritários: "
    f"{quantidade_prioritarios}"
)

print(
    f"Faturamento total desses clientes: "
    f"R$ {faturamento_prioritarios:,.2f}"
)

print(
    clientes_prioritarios_fora_raio[
        [
            "id_cliente",
            "nome_fantasia",
            "tipo_profissional",
            "bairro",
            "zona",
            "distancia_km",
            "faturamento_12m",
            "ja_visitado"
        ]
    ]
)

# ============================================================
# 11. COMPARAÇÃO DE CUSTOS DA ESTRATÉGIA DE VISITAÇÃO
# ============================================================

# Transforma a base de custos em um dicionário
custos_dict = custos.set_index("item")["valor"].to_dict()

# Recupera os valores necessários
custo_visita_pontual = custos_dict[
    "custo_visita_pontual_fora_raio"
]

custo_segundo_ponto = custos_dict[
    "custo_abertura_2o_ponto"
]

salario_representante = custos_dict[
    "salario_representante"
]

capacidade_visitas_mes = custos_dict[
    "capacidade_visitas_mes"
]

# Quantidade de clientes prioritários identificados
quantidade_prioritarios = len(
    clientes_prioritarios_fora_raio
)

# Custo para realizar uma visita pontual
# em cada cliente prioritário fora do raio
custo_total_visitas_pontuais = (
    quantidade_prioritarios
    * custo_visita_pontual
)

# Diferença entre as duas alternativas
diferenca_custos = (
    custo_segundo_ponto
    - custo_total_visitas_pontuais
)

# Ponto de equilíbrio:
# quantidade de visitas pontuais que equivalem
# ao custo de abertura do segundo ponto
ponto_equilibrio_visitas = (
    custo_segundo_ponto
    / custo_visita_pontual
)

print("=== COMPARAÇÃO DE CUSTOS ===")

print(
    f"\nClientes prioritários fora do raio: "
    f"{quantidade_prioritarios}"
)

print(
    f"Custo por visita pontual: "
    f"R$ {custo_visita_pontual:,.2f}"
)

print(
    f"Custo total das visitas pontuais: "
    f"R$ {custo_total_visitas_pontuais:,.2f}"
)

print(
    f"Custo de abertura do segundo ponto: "
    f"R$ {custo_segundo_ponto:,.2f}"
)

print(
    f"Ponto de equilíbrio aproximado: "
    f"{ponto_equilibrio_visitas:.1f} visitas"
)

print(
    f"\nCapacidade de 1 representante: "
    f"{capacidade_visitas_mes:.0f} visitas/mês"
)

print(
    f"Salário mensal do representante: "
    f"R$ {salario_representante:,.2f}"
)

# Recomendação automática baseada no custo inicial
print("\n=== RESULTADO DA COMPARAÇÃO ===")

if custo_total_visitas_pontuais < custo_segundo_ponto:
    print(
        "Para atender inicialmente os clientes prioritários "
        "fora do raio, as visitas pontuais apresentam menor custo "
        "do que a abertura de um segundo ponto."
    )
else:
    print(
        "O custo das visitas pontuais já supera o custo inicial "
        "de abertura de um segundo ponto, indicando a necessidade "
        "de avaliar uma expansão da operação."
    )

# ============================================================
# 12. RESUMO DOS PRINCIPAIS INDICADORES
# ============================================================

indicadores_dashboard = pd.DataFrame({
    "indicador": [
        "Total de clientes",
        "Clientes dentro do raio de 25 km",
        "Cobertura de clientes (%)",
        "Faturamento total",
        "Faturamento dentro do raio",
        "Cobertura do faturamento (%)",
        "Faturamento médio - visitados",
        "Faturamento médio - não visitados",
        "Diferença de faturamento médio (%)",
        "Clientes prioritários fora do raio",
        "Faturamento dos prioritários fora do raio",
        "Custo das visitas pontuais",
        "Custo de abertura do segundo ponto"
    ],
    "valor": [
        total_clientes,
        clientes_dentro_raio,
        percentual_clientes_raio,
        faturamento_total,
        faturamento_dentro_raio,
        percentual_faturamento_raio,
        media_visitados,
        media_nao_visitados,
        diferenca_percentual,
        quantidade_prioritarios,
        faturamento_prioritarios,
        custo_total_visitas_pontuais,
        custo_segundo_ponto
    ]
})

print("=== RESUMO DOS INDICADORES DO DASHBOARD ===")
print(indicadores_dashboard)

# ============================================================
# 13. EXPORTAÇÃO FINAL DOS DADOS
# ============================================================

# Caminhos dos arquivos de saída
ARQUIVO_BASE_FINAL = (
    BASE_DIR / "data" / "carteirizacao_tratada.csv"
)

ARQUIVO_INDICADORES = (
    BASE_DIR / "data" / "indicadores_dashboard.csv"
)

ARQUIVO_PRIORITARIOS = (
    BASE_DIR / "data" / "clientes_prioritarios_fora_raio.csv"
)


# Exporta a base completa e enriquecida
clientes_tratados.to_csv(
    ARQUIVO_BASE_FINAL,
    index=False,
    sep=";",
    encoding="utf-8-sig"
)


# Exporta os indicadores do dashboard
indicadores_dashboard.to_csv(
    ARQUIVO_INDICADORES,
    index=False,
    sep=";",
    encoding="utf-8-sig"
)


# Exporta os clientes prioritários fora do raio
clientes_prioritarios_fora_raio.to_csv(
    ARQUIVO_PRIORITARIOS,
    index=False,
    sep=";",
    encoding="utf-8-sig"
)


print("=== EXPORTAÇÃO FINAL CONCLUÍDA ===")

print(f"\nBase tratada: {ARQUIVO_BASE_FINAL}")
print(f"Indicadores: {ARQUIVO_INDICADORES}")
print(f"Clientes prioritários: {ARQUIVO_PRIORITARIOS}")

# ============================================================
# 14. ANÁLISE DE CONCENTRAÇÃO POR BAIRRO E ZONA
# ============================================================

# ------------------------------------------------------------
# Análise por bairro
# ------------------------------------------------------------

analise_bairro = (
    clientes_tratados
    .groupby("bairro", as_index=False)
    .agg(
        total_clientes=("id_cliente", "nunique"),
        faturamento_total=("faturamento_12m", "sum")
    )
)

bairro_mais_clientes = (
    analise_bairro
    .sort_values("total_clientes", ascending=False)
    .iloc[0]
)

bairro_maior_faturamento = (
    analise_bairro
    .sort_values("faturamento_total", ascending=False)
    .iloc[0]
)


# ------------------------------------------------------------
# Análise por zona
# ------------------------------------------------------------

analise_zona = (
    clientes_tratados
    .groupby("zona", as_index=False)
    .agg(
        total_clientes=("id_cliente", "nunique"),
        faturamento_total=("faturamento_12m", "sum")
    )
)

zona_mais_clientes = (
    analise_zona
    .sort_values("total_clientes", ascending=False)
    .iloc[0]
)

zona_maior_faturamento = (
    analise_zona
    .sort_values("faturamento_total", ascending=False)
    .iloc[0]
)


# ------------------------------------------------------------
# Exibição dos resultados
# ------------------------------------------------------------

print("=== CONCENTRAÇÃO POR BAIRRO ===")

print(
    f"Bairro com mais clientes: "
    f"{bairro_mais_clientes['bairro']} "
    f"({bairro_mais_clientes['total_clientes']:.0f} clientes)"
)

print(
    f"Bairro com maior faturamento: "
    f"{bairro_maior_faturamento['bairro']} "
    f"(R$ {bairro_maior_faturamento['faturamento_total']:,.2f})"
)

print("\n=== CONCENTRAÇÃO POR ZONA ===")

print(
    f"Zona com mais clientes: "
    f"{zona_mais_clientes['zona']} "
    f"({zona_mais_clientes['total_clientes']:.0f} clientes)"
)

print(
    f"Zona com maior faturamento: "
    f"{zona_maior_faturamento['zona']} "
    f"(R$ {zona_maior_faturamento['faturamento_total']:,.2f})"
)

print("\n=== TABELA POR ZONA ===")
print(
    analise_zona.sort_values(
        "faturamento_total",
        ascending=False
    )
)

print("\n=== TOP 10 BAIRROS POR FATURAMENTO ===")
print(
    analise_bairro
    .sort_values(
        "faturamento_total",
        ascending=False
    )
    .head(10)
)
# ============================================================
# 15. QUALIDADE DA COBERTURA GEOGRÁFICA
# ============================================================

total_clientes = clientes_tratados["id_cliente"].nunique()

clientes_com_cep = (
    clientes_tratados["possui_cep"] == "Sim"
).sum()

clientes_sem_cep = (
    clientes_tratados["possui_cep"] == "Não"
).sum()

percentual_com_cep = (
    clientes_com_cep / total_clientes * 100
)

percentual_sem_cep = (
    clientes_sem_cep / total_clientes * 100
)

print("=== QUALIDADE DA COBERTURA GEOGRÁFICA ===")

print(f"Total de clientes: {total_clientes}")
print(
    f"Clientes com CEP: {clientes_com_cep} "
    f"({percentual_com_cep:.1f}%)"
)
print(
    f"Clientes sem CEP: {clientes_sem_cep} "
    f"({percentual_sem_cep:.1f}%)"
)

print("\n=== OBSERVAÇÃO PARA O DASHBOARD ===")

print(
    "A ausência de CEP limita análises baseadas diretamente "
    "no endereço postal. Entretanto, como a base possui "
    "latitude e longitude, a análise de cobertura geográfica "
    "e o cálculo da distância até a Vila Mariana podem ser "
    "realizados pelas coordenadas disponíveis."
)
# ============================================================
# 16. ANÁLISE DOS IDs DUPLICADOS
# ============================================================

ids_duplicados_lista = clientes[
    clientes["id_cliente"].duplicated(keep=False)
].sort_values("id_cliente")

print("\n========== ANÁLISE DOS IDs DUPLICADOS ==========")

print(
    ids_duplicados_lista.to_string(index=False)
)

print(
    f"\nQuantidade de IDs únicos com duplicidade: "
    f"{ids_duplicados_lista['id_cliente'].nunique()}"
)

print(
    f"Quantidade total de registros envolvidos: "
    f"{len(ids_duplicados_lista)}"
)
