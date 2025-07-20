# Relatório Técnico: Identificação de Sistemas Dinâmicos com Dados Reais de Laboratório
**Alunos:** César Kerber, Lucas Ekroth e Paulo Rangel

## 1. Introdução

Este relatório técnico detalha o processo de identificação de um sistema dinâmico utilizando dados reais adquiridos no contexto do projeto de controle de nível em um tanque pulmão, desenvolvido no laboratório de controle de processos. O objetivo principal é estimar um modelo matemático que represente o comportamento dinâmico do sistema analisado, permitindo simulação, análise e comparação com os modelos desenvolvidos anteriormente com base na abordagem clássica (funções de transferência com tempo morto).

A identificação de sistemas é uma etapa crucial na engenharia de controle e automação, pois possibilita o desenvolvimento de controladores eficazes e a compreensão aprofundada da dinâmica de processos físicos. Neste caso, os dados utilizados — de nível e velocidade da bomba — são os mesmos obtidos no ensaio a 55% de velocidade do projeto anterior, permitindo uma análise complementar sob uma nova abordagem: a modelagem baseada em dados.

## 2. Metodologia

A metodologia empregada neste projeto seguiu as etapas clássicas da identificação de sistemas, conforme descrito na literatura e nas diretrizes da atividade proposta. As principais fases incluíram pré-processamento dos dados, aplicação de diferentes métodos de identificação e validação dos modelos obtidos.

### 2.1. Conexão com o Projeto Original

Os dados utilizados neste estudo foram extraídos do projeto de controle de nível no tanque pulmão, especificamente do ensaio com entrada em degrau para 55% da velocidade da bomba. No projeto anterior, esse experimento foi utilizado para construir modelos de primeira ordem com tempo morto utilizando métodos como Ziegler-Nichols, Miller e Sundaresan-Krishnaswamy. Aqui, esses mesmos dados servem como base para uma nova abordagem: a identificação baseada em dados por meio de modelos matemáticos ajustados diretamente aos valores registrados.

Essa interconexão demonstra como um experimento de controle pode fornecer insumos valiosos para múltiplas linhas de análise, evidenciando o caráter interdisciplinar da engenharia de controle e a importância de uma boa aquisição e documentação de dados.

### 2.2. Pré-processamento dos Dados

O arquivo `data55.csv` foi carregado e as colunas de tempo foram convertidas para segundos. Os dados iniciais com entrada e saída nulas foram removidos para focar na resposta dinâmica após a aplicação do degrau. O tempo foi reajustado para iniciar em zero após este corte.

Para o modelo ARX, os dados foram reamostrados com passo fixo de 1 segundo usando interpolação linear, assegurando uma malha temporal adequada à modelagem discreta.

### 2.3. Modelos de Identificação de Sistemas

Dois modelos principais foram investigados:

#### 2.3.1. Modelo de Primeira Ordem em Tempo Contínuo

Este modelo representa a resposta do nível do tanque a uma variação de velocidade da bomba como um sistema de primeira ordem puro. Utilizamos mínimos quadrados não-lineares (função `curve_fit` do SciPy) para estimar os parâmetros $\tau$ e $K$.

#### 2.3.2. Modelo ARX (AutoRegressive with eXogenous input)

Modelo em tempo discreto amplamente utilizado para análise de dados amostrados. A estrutura ARX permite representar o comportamento com atrasos explícitos e dependência temporal. Foi adotada uma estrutura de primeira ordem: `na=1`, `nb=1`, `nk=1`.

## 3. Resultados e Discussão

### 3.1. Modelo de Primeira Ordem

Parâmetros estimados:
- **K:** 1.00
- **$\tau$:** 462.50 s
- **RMSE:** 36.05

![Figura 1: Identificação de Sistema de Primeira Ordem](first_order_model_identification.png)

**Discussão:** Apesar de capturar a tendência geral da curva de nível (como também observado no projeto original), o modelo apresenta um erro significativo. Isso reforça a limitação das aproximações analíticas frente à natureza real do sistema.

### 3.2. Modelo ARX

Parâmetros estimados:
- **a:** -0.98888261
- **b:** 0.00794431
- **RMSE:** 3.45

![Figura 2: Identificação de Sistema com Modelo ARX](arx_model_identification.png)

**Discussão:** O modelo ARX demonstrou excelente capacidade de representar o sistema com base nos dados experimentais, superando em muito o modelo contínuo tradicional. Essa diferença revela o potencial da modelagem baseada em dados — especialmente útil quando se dispõe de registros históricos ou sensores operando em tempo real.

Além disso, a boa performance do ARX complementa os modelos do primeiro projeto, servindo como alternativa ou ferramenta de validação para os métodos clássicos de identificação via curva de reação.

## 4. Conclusão

Este estudo estende o trabalho realizado no projeto de controle de nível do tanque pulmão, aplicando métodos de identificação baseados em dados aos mesmos ensaios experimentais. A comparação entre o modelo de primeira ordem contínuo e o modelo ARX mostrou que este último apresenta desempenho superior, revelando a importância de métodos discretos em contextos com dados amostrados.

A integração entre os dois projetos evidencia a relevância de uma base experimental bem conduzida, permitindo análises complementares e maior aprofundamento técnico. Como próximo passo, sugere-se validar o modelo ARX no ambiente de simulação com controladores PID projetados no projeto original, ou ainda aplicá-lo em controle preditivo.

## 5. Referências

[1] L. Ljung, *System Identification: Theory for the User*. 2nd ed., Prentice Hall, 1999.

[2] K. Ogata, *Engenharia de Controle Moderno*. 5ª ed., Pearson Prentice Hall, 2010.

[3] G. Bastin and M. Gevers, "Stable adaptive observers for nonlinear time-varying systems," *IEEE Transactions on Automatic Control*, vol. 33, no. 7, pp. 650–658, 1988. DOI: [10.1109/9.1271](https://doi.org/10.1109/9.1271)

[4] IFSP – Campus São José dos Campos. *Controle de Nível em Tanque Pulmão*. Projeto de Laboratório CPSE7, 2025.

[5] IFSP – Campus São José dos Campos. *Atividade Avaliativa: Identificação de Sistemas Dinâmicos com Dados Reais de Laboratório*. 2025.

[6] `data55.csv` – Conjunto de dados experimentais obtido no ensaio de malha aberta com 55\% da velocidade da bomba centrífuga, realizado no Laboratório de Controle de Processos – IFSP/SJC, 2025.
