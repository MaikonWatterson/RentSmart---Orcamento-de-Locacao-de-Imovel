# RentSmart — Sistema de Orçamento de Locação

Sistema desenvolvido em **Python** utilizando **Programação Orientada a Objetos (POO)** para automatizar o cálculo de orçamentos de locação da imobiliária **R.M Imóveis**, reduzindo o tempo de atendimento e evitando erros manuais na aplicação de regras comerciais, adicionais e descontos.

## 🚀 Funcionalidades

* **Múltiplas Categorias de Imóveis:** Suporte a apartamentos (1 e 2 quartos), casas (1, 2 e 3 quartos) e estúdios.
* **Gestão de Garagens Flexível:** 
  * Para casas e apartamentos: Adicional opcional por vaga tradicional.
  * Para estúdios: Pacote inicial de 2 vagas e cálculo automatizado de vagas extras.
* **Desconto Comercial:** Aplicação automática de 5% de desconto para apartamentos cujos inquilinos não possuem crianças.
* **Separação de Custos:** Tratamento individualizado do aluguel mensal líquido e da taxa contratual fixa (R$ 2.000,00), com opção de parcelamento em até 5 vezes.
* **Projeção de 12 Meses:** Geração automática de um arquivo **CSV** (`projecao_locacao.csv`) detalhando a previsão financeira do primeiro ano de contrato mês a mês.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* Módulo nativo `csv` para exportação de dados.

---

## 📂 Estrutura do Código

O sistema foi estruturado com foco na separação de responsabilidades e encapsulamento:

1. **Classe `Imovel`**: Responsável por armazenar o tipo de imóvel, gerenciar o cálculo do aluguel-base e computar os custos de garagem (pacote inicial e vagas extras).
2. **Classe `Orcamento`**: Responsável por associar o cliente ao imóvel, calcular regras de desconto, processar o valor final do aluguel mensal, gerenciar o parcelamento da taxa contratual e exportar a planilha CSV.
3. **Função `menu_interativo()`**: Interface de terminal amigável para captação de dados, validação de entradas e exibição formatada do resumo do orçamento.

---

## ▶️ Como Executar

1. Certifique-se de ter o **Python** instalado em sua máquina.
2. Baixe ou copie o código fonte em um arquivo chamado `main.py`.
3. Abra o terminal na pasta do arquivo e execute o comando:

bash
python main.py

## Ou simplesmente Execute no próprio Ambiente Python  de sua preferência.
