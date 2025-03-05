## Análise da Matriz BCG de Produtos
Este projeto tem como objetivo calcular a posição dos produtos de uma empresa na Matriz BCG (Boston Consulting Group) utilizando faturamento e custo de produção dos produtos. A Matriz BCG é uma ferramenta estratégica que ajuda as empresas a entenderem a posição de seus produtos no mercado e tomar decisões de investimento com base nas suas vacas leiteiras, estrelas, interrogações e abacaxis.

## Objetivo
Classificar os produtos da empresa nas quatro categorias da Matriz BCG:
Vacas Leiteiras: Produtos com alta lucratividade e baixo faturamento relativo.
Estrelas: Produtos com alta lucratividade e alto faturamento relativo.
Interrogações: Produtos com baixa lucratividade e alto faturamento relativo.
Abacaxis: Produtos com baixa lucratividade e baixo faturamento relativo.
Como Funciona
A matriz é construída com base em dois parâmetros principais:

Lucratividade: A diferença entre o faturamento e o custo de produção, representada como uma porcentagem do faturamento.

Lucratividade
=
Faturamento
−
Custo de Produ
c
¸
a
˜
o
Faturamento
×
100
Lucratividade= 
Faturamento
Faturamento−Custo de Produ 
c
¸
​
  
a
˜
 o
​
 ×100
Faturamento Relativo: A participação de cada produto no faturamento total da empresa.

Faturamento Relativo
=
Faturamento do Produto
Faturamento Total da Empresa
×
100
Faturamento Relativo= 
Faturamento Total da Empresa
Faturamento do Produto
​
 ×100
Com base nesses cálculos, os produtos são classificados na matriz.

Estrutura do Banco de Dados
Para realizar a análise, utilizamos uma tabela chamada produtos com as seguintes colunas:

id_produto: Identificador único do produto.
nome_produto: Nome do produto.
faturamento: Valor total de vendas do produto.
custo_producao: Custo total de produção do produto.



-- Passo 1: Calcular o faturamento total da empresa
WITH faturamento_total AS (
  SELECT SUM(faturamento) AS faturamento_empresa
  FROM produtos
)

-- Passo 2: Calcular a lucratividade e o faturamento relativo para cada produto
SELECT 
  p.id_produto,
  p.nome_produto,
  p.faturamento,
  p.custo_producao,
  -- Calculando a lucratividade
  ((p.faturamento - p.custo_producao) / p.faturamento) * 100 AS lucratividade,
  -- Calculando o faturamento relativo
  (p.faturamento / f.faturamento_empresa) * 100 AS faturamento_relativo
FROM 
  produtos p
JOIN 
  faturamento_total f
ORDER BY 
  faturamento_relativo DESC;


WITH faturamento_total AS (
  SELECT SUM(faturamento) AS faturamento_empresa
  FROM produtos
)
SELECT 
  p.id_produto,
  p.nome_produto,
  p.faturamento,
  p.custo_producao,
  ((p.faturamento - p.custo_producao) / p.faturamento) * 100 AS lucratividade,
  (p.faturamento / f.faturamento_empresa) * 100 AS faturamento_relativo,
  CASE
    -- Categoria Vacas Leiteiras
    WHEN ((p.faturamento - p.custo_producao) / p.faturamento) * 100 >= 30 
         AND (p.faturamento / f.faturamento_empresa) * 100 < 10 THEN 'Vacas Leiteiras'
    -- Categoria Estrelas
    WHEN ((p.faturamento - p.custo_producao) / p.faturamento) * 100 >= 30 
         AND (p.faturamento / f.faturamento_empresa) * 100 >= 10 THEN 'Estrelas'
    -- Categoria Interrogações
    WHEN ((p.faturamento - p.custo_producao) / p.faturamento) * 100 < 30
         AND (p.faturamento / f.faturamento_empresa) * 100 >= 10 THEN 'Interrogações'
    -- Categoria Abacaxis
    ELSE 'Abacaxis'
  END AS categoria_bcg
FROM 
  produtos p
JOIN 
  faturamento_total f
ORDER BY 
  faturamento_relativo DESC;
