# # Teste Técnico – Analista de Dados / BI

## Grupo Central

## Objetivo

Este projeto foi desenvolvido como solução para o teste técnico do processo seletivo para Analista de Dados / BI do Grupo Central.

O objetivo é construir um dashboard executivo capaz de apoiar a tomada de decisão sobre a implantação de uma operação de visitação comercial para a empresa fictícia **NutriMax Distribuidora**, utilizando análises geográficas, indicadores comerciais e avaliação financeira para responder se a estratégia proposta é viável e quais clientes devem compor a carteira de visitação.

---

## Contexto

A NutriMax Distribuidora comercializa produtos de nutrição e suplementação para profissionais da saúde e estabelecimentos comerciais na cidade de São Paulo e região metropolitana.

A diretoria pretende implantar uma equipe de visitação externa composta inicialmente por um representante comercial, com base operacional na Vila Mariana e cobertura estimada em um raio de 25 km.

Este projeto tem como finalidade analisar a base de clientes disponibilizada, avaliar a cobertura geográfica, identificar oportunidades comerciais e apresentar uma recomendação baseada em dados para apoiar essa decisão.

---

## Objetivos da Análise

Durante o desenvolvimento foram avaliados os seguintes pontos:

* Distribuição geográfica da carteira de clientes;
* Qualidade dos dados disponibilizados;
* Concentração de clientes e faturamento por região;
* Cobertura da carteira considerando um raio de 25 km a partir da Vila Mariana;
* Relação entre visitas comerciais e faturamento;
* Identificação de clientes estratégicos fora da área de cobertura;
* Comparação entre os custos operacionais de visitas pontuais e da abertura de uma segunda base comercial;
* Elaboração de recomendações para apoio à tomada de decisão.

---

## Ferramentas Utilizadas

* Power BI
* Python
* Pandas
* Git
* GitHub

---

## Estrutura do Projeto

```text
├── data/
│   ├── carteirizacao_sp_simulado.csv
│   └── custos_visitacao.csv
│
├── dashboard/
│   └── Carteirizacao.pbix
│
├── docs/
│   ├── metodologia.md
│   └── apresentacao.md
│
├── imagens/
│
├── scripts/
│
└── README.md
```

---

## Metodologia

O desenvolvimento da análise seguiu as seguintes etapas:

1. Importação e validação das bases de dados;
2. Tratamento de valores ausentes e padronização dos dados;
3. Cálculo da distância entre cada cliente e a base operacional utilizando coordenadas geográficas;
4. Classificação dos clientes dentro e fora do raio de cobertura proposto;
5. Construção dos indicadores de desempenho;
6. Desenvolvimento do dashboard executivo;
7. Elaboração das recomendações de negócio baseadas nas evidências obtidas.

---

## Dashboard

O dashboard foi desenvolvido para responder às questões propostas no teste técnico por meio de indicadores, mapas e visualizações interativas, permitindo avaliar:

* Cobertura geográfica da operação;
* Distribuição dos clientes;
* Potencial de faturamento;
* Impacto das visitas comerciais;
* Viabilidade financeira da estratégia proposta.

---

## Resultados

Os resultados obtidos são apresentados no dashboard e sustentam a recomendação executiva construída ao longo da análise, considerando aspectos comerciais, geográficos e financeiros.

---

## Como Executar

1. Clone este repositório;
2. Abra o arquivo **dashboard/Carteirizacao.pbix** no Power BI Desktop;
3. Atualize as conexões de dados, caso necessário;
4. Navegue pelas páginas do dashboard para visualizar a análise completa.

---

## Autor

Projeto desenvolvido por **Carolina Fagundes** como parte do processo seletivo para a vaga de Analista de Dados / BI do Grupo Central.

