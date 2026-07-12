# Teste Técnico – Analista de Dados / BI

# Grupo Central

## Projeto: Análise de Carteirização Comercial – NutriMax Distribuidora

---

## Objetivo do Projeto

Este projeto foi desenvolvido como solução para o teste técnico do processo seletivo para a posição de **Analista de Dados / BI do Grupo Central**.

O objetivo principal foi desenvolver uma análise estratégica da carteira de clientes da empresa fictícia **NutriMax Distribuidora**, avaliando a viabilidade da implantação de uma operação de visitação comercial.

A solução busca apoiar a tomada de decisão através da análise de dados comerciais, geográficos e financeiros, identificando:

* Potencial da carteira atual;
* Clientes prioritários para atuação comercial;
* Regiões com maior oportunidade;
* Cobertura geográfica da operação;
* Eficiência das rotas de visitação;
* Impacto financeiro da estratégia proposta.

---

# Contexto do Negócio

A NutriMax Distribuidora atua no segmento de nutrição e suplementação, atendendo profissionais da saúde e estabelecimentos comerciais localizados em São Paulo e região metropolitana.

Com o objetivo de expandir o relacionamento comercial, a empresa pretende estruturar uma operação de visitação externa inicialmente composta por um representante comercial, tendo como base operacional a região da Vila Mariana.

O desafio consiste em avaliar a carteira existente e responder:

* Quais clientes possuem maior potencial comercial?
* A cobertura geográfica atual permite uma operação eficiente?
* Quais regiões devem ser priorizadas?
* Como estruturar uma rota comercial mais eficiente?
* A estratégia proposta apresenta viabilidade operacional e financeira?

---

# Objetivos da Análise

Durante o desenvolvimento do projeto foram realizadas análises para:

* Validar e preparar a base de clientes disponibilizada;
* Avaliar a qualidade e consistência dos dados;
* Entender o perfil da carteira de clientes;
* Analisar distribuição geográfica por regiões;
* Identificar clientes prioritários;
* Avaliar oportunidades comerciais;
* Calcular cobertura considerando a distância da base operacional;
* Criar uma sugestão de rota de visitação;
* Comparar aspectos operacionais e financeiros da estratégia.

---

# Tecnologias e Ferramentas Utilizadas

As principais ferramentas utilizadas no desenvolvimento foram:

* **Python** – tratamento, análise e preparação dos dados;
* **Pandas** – manipulação das bases de dados;
* **Streamlit** – desenvolvimento do dashboard interativo;
* **Altair** – construção de gráficos analíticos;
* **PyDeck** – visualização geográfica e mapas;
* **Git e GitHub** – versionamento e documentação do projeto.

---

# Estrutura do Projeto

```text
├── data/
│   ├── carteirizacao_sp_simulado.csv
│   └── custos_visitacao.csv
│
├── dashboard/
│   └── app.py
│
├── docs/
│   ├── metodologia.md
│   └── apresentacao.md
│
├── imagens/
│
├── scripts/
│
├── video_apresentacao/
│   └── Vídeo Apresentação.mp4
│
├── requirements.txt
│
└── README.md
```

---

# Metodologia

O desenvolvimento da solução foi dividido nas seguintes etapas:

## 1. Preparação e validação dos dados

* Importação das bases disponibilizadas;
* Avaliação da estrutura dos dados;
* Identificação de inconsistências;
* Tratamento e padronização das informações.

## 2. Análise exploratória da carteira

Foram avaliados:

* Volume total de clientes;
* Distribuição por perfil profissional;
* Distribuição geográfica;
* Concentração de clientes por região;
* Características da carteira comercial.

## 3. Análise geográfica

A análise considerou:

* Localização dos clientes;
* Distância entre clientes e base operacional;
* Área de cobertura estimada;
* Identificação de clientes dentro e fora do raio definido.

## 4. Priorização comercial

Foram identificados clientes estratégicos considerando:

* Potencial comercial;
* Localização;
* Perfil do cliente;
* Oportunidade de atuação.

## 5. Construção do Dashboard

Os resultados foram consolidados em um dashboard executivo desenvolvido em Streamlit, permitindo uma visão integrada dos indicadores comerciais e geográficos.

---

# Dashboard

O dashboard foi desenvolvido para apresentar uma visão executiva da carteira comercial e apoiar decisões relacionadas à operação de visitação.

As principais análises disponíveis são:

### Prévia da Base Tratada

Apresentação da estrutura final dos dados após o processo de preparação e validação.

### Visão Geral da Carteira

Indicadores gerais sobre quantidade de clientes, distribuição e características principais da carteira.

### Perfil da Carteira

Análise dos clientes considerando suas características comerciais.

### Perfil Profissional

Avaliação da distribuição dos clientes por tipo de profissional.

### Distribuição Geográfica

Análise dos clientes por região/zona e concentração territorial.

### Ranking de Clientes Prioritários

Identificação dos clientes com maior potencial para atuação comercial.

### Mapa da Carteira

Visualização geográfica dos clientes e sua distribuição espacial.

### Oportunidades Comerciais

Identificação de regiões e clientes com potencial de expansão.

### Cobertura Comercial

Avaliação da capacidade de atendimento considerando a localização da base operacional.

### Rota Sugerida

Construção de uma sugestão de sequência de visitas para otimização da operação comercial.

### Mapa da Rota

Representação visual da rota planejada.

---

# Resultados Esperados

A solução desenvolvida permite apoiar a tomada de decisão comercial através de uma visão baseada em dados, possibilitando:

* Melhor direcionamento dos esforços comerciais;
* Priorização dos clientes mais relevantes;
* Redução de deslocamentos improdutivos;
* Melhor planejamento das visitas;
* Identificação de oportunidades de expansão;
* Avaliação da viabilidade da operação proposta.

---

# Vídeo de Apresentação

A apresentação detalhada da solução está disponível na pasta:

```
video_apresentacao/
```
Caso não conseguir acessar pela pasta tem como acessar pelo drive que está com o link dentro da mesma.

---

# Autor

Projeto desenvolvido por **Carolina Fagundes** como parte do processo seletivo para a vaga de **Analista de Dados / BI do Grupo Central Farma**.


