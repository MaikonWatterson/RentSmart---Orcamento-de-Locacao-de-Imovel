import csv

class Imovel:
    def __init__(self, tipo: str, vaga_garagem: bool = False, num_vagas_extra: int = 0):
        self.tipo = tipo.lower()
        self.vaga_garagem = vaga_garagem
        self.num_vagas_extra = num_vagas_extra
        self.aluguel_base = self._calcular_aluguel_base()

    def _calcular_aluguel_base(self) -> float:
        if self.tipo == "apartamento 1 quarto":
            return 700.0
        elif self.tipo == "apartamento 2 quartos":
            return 700.0 + 200.0  
        elif self.tipo == "casa 1 quarto":
            return 900.0        
        elif self.tipo == "casa 2 quartos":
            return 900.0 + 250.0  
        elif self.tipo == "casa 3 quartos":
            return 1150.0 + 250.0 
        elif self.tipo == "estúdio":
            return 1200.0
        else:
            raise ValueError(f"Tipo de imóvel inválido: {self.tipo}")

    def calcular_pacote_inicial_garagem(self) -> float:
        """Retorna o valor do pacote inicial de garagem."""
        if self.tipo == "estúdio":
            return 250.0 if self.vaga_garagem else 0.0
        else:
            return 300.0 if self.vaga_garagem else 0.0

    def calcular_vagas_extras(self) -> float:
        """Retorna o valor apenas das vagas extras (somente para estúdio)."""
        if self.tipo == "estúdio" and self.vaga_garagem:
            return self.num_vagas_extra * 60.0
        return 0.0

    def calcular_adicional_garagem_total(self) -> float:
        """Soma o pacote inicial e as vagas extras."""
        return self.calcular_pacote_inicial_garagem() + self.calcular_vagas_extras()


class Orcamento:
    TAXA_CONTRATUAL_TOTAL = 2000.0

    def __init__(self, cliente_nome: str, imovel: Imovel, sem_criancas: bool = False, parcelas_taxa: int = 1):
        if not (1 <= parcelas_taxa <= 5):
            raise ValueError("O número de parcelas da taxa contratual deve ser entre 1 e 5.")
        
        self.cliente_nome = cliente_nome
        self.imovel = imovel
        self.sem_criancas = sem_criancas
        self.parcelas_taxa = parcelas_taxa

    def calcular_desconto(self, subtotal_aluguel: float) -> float:
        if "apartamento" in self.imovel.tipo and self.sem_criancas:
            return subtotal_aluguel * 0.05
        return 0.0

    def calcular_aluguel_mensal_final(self) -> tuple[float, float, float]:
        subtotal = self.imovel.aluguel_base + self.imovel.calcular_adicional_garagem_total()
        desconto = self.calcular_desconto(subtotal)
        aluguel_final = subtotal - desconto
        return subtotal, desconto, aluguel_final

    def calcular_parcela_taxa(self) -> float:
        return self.TAXA_CONTRATUAL_TOTAL / self.parcelas_taxa

    def gerar_projecao_12_meses(self) -> list[dict]:
        subtotal, desconto, aluguel_mensal = self.calcular_aluguel_mensal_final()
        valor_parcela_taxa = self.calcular_parcela_taxa()
        
        projecao = []
        for mes in range(1, 13):
            taxa_mes = valor_parcela_taxa if mes <= self.parcelas_taxa else 0.0
            total_mes = aluguel_mensal + taxa_mes
            projecao.append({
                "Mês": mes,
                "Aluguel Base (R$)": f"{self.imovel.aluguel_base:.2f}",
                "Pacote Inicial Garagem (R$)": f"{self.imovel.calcular_pacote_inicial_garagem():.2f}",
                "Vagas Extras (R$)": f"{self.imovel.calcular_vagas_extras():.2f}",
                "Desconto (R$)": f"{desconto:.2f}",
                "Aluguel Mensal Líquido (R$)": f"{aluguel_mensal:.2f}",
                "Parcela Taxa Contratual (R$)": f"{taxa_mes:.2f}",
                "Total a Pagar no Mês (R$)": f"{total_mes:.2f}"
            })
        return projecao

    def exportar_csv(self, filename: str = "projecao_locacao.csv"):
        projecao = self.gerar_projecao_12_meses()
        fieldnames = list(projecao[0].keys())
        
        with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(projecao)
        print(f"\n[SUCESSO] Arquivo '{filename}' gerado com sucesso!")


def menu_interativo():
    cliente = input("Qual o seu nome? ").strip()

    print()
    print(f"Bem Vindo {cliente}, ao nosso Sistema de Orçamento de Locação")
    print()
    
    print("┌====================================================┐")
    print("|====================================================|")
    print("|=== RENTSMART - SISTEMA DE ORÇAMENTO R.M IMÓVEIS ===|")
    print("|====================================================|")
    print("|                                                    |")
    print("|Selecione o tipo de imóvel:                         |")
    print("|1 - Apartamento 1 Quarto (R$ 700,00)                |")
    print("|2 - Apartamento 2 Quartos (R$ 900,00)               |")
    print("|3 - Casa 1 Quarto (R$ 900,00)                       |")
    print("|4 - Casa 2 Quartos (R$ 1.150,00)                    |")
    print("|5 - Casa 3 Quartos (R$ 1.400,00)                    |")
    print("|6 - Estúdio (R$ 1.200,00)                           |")
    print("|                                                    |")
    print("└====================================================┘")

    opcao = input("Opção (1-6): ").strip()
    mapa_imoveis = {
        "1": "apartamento 1 quarto",
        "2": "apartamento 2 quartos",
        "3": "casa 1 quarto",
        "4": "casa 2 quartos",
        "5": "casa 3 quartos",
        "6": "estúdio"
    }

    tipo_escolhido = mapa_imoveis.get(opcao, "apartamento 1 quarto")

    vaga_garagem = False
    vagas_extra = 0
    if tipo_escolhido == "estúdio":
        op_garagem = input("Deseja o pacote inicial de garagem (2 vagas por R$ 250,00)? (s/n): ").strip().lower()
        if op_garagem == 's':
            vaga_garagem = True
            ve = input("Deseja vagas adicionais (R$ 60,00 cada)? Informe a quantidade (0 se nenhuma): ").strip()
            vagas_extra = int(ve) if ve.isdigit() else 0
    else:
        op_garagem = input("Deseja vaga de garagem (R$ 300,00/mês)? (s/n): ").strip().lower()
        vaga_garagem = (op_garagem == 's')

    sem_criancas = False
    if "apartamento" in tipo_escolhido:
        op_criancas = input("O imóvel terá crianças? (s/n): ").strip().lower()
        sem_criancas = (op_criancas == 'n')

    print("\nA taxa contratual total é de R$ 2.000,00.")
    parcelas = input("Em quantas parcelas deseja pagar a taxa contratual? (1 a 5): ").strip()
    num_parcelas = int(parcelas) if parcelas.isdigit() and 1 <= int(parcelas) <= 5 else 1

    imovel_obj = Imovel(tipo=tipo_escolhido, vaga_garagem=vaga_garagem, num_vagas_extra=vagas_extra)
    orcamento = Orcamento(cliente_nome=cliente, imovel=imovel_obj, sem_criancas=sem_criancas, parcelas_taxa=num_parcelas)

    subtotal, desconto, aluguel_mensal = orcamento.calcular_aluguel_mensal_final()
    parcela_taxa = orcamento.calcular_parcela_taxa()

    print()
    print("=======================================================")
    print("                   RESUMO DO ORÇAMENTO")
    print("=======================================================")
    print(f"Cliente: {cliente}")
    print(f"Imóvel Selecionado: {tipo_escolhido.title()}")
    print(f"Aluguel Base: R$ {imovel_obj.aluguel_base:.2f}")
    print(f"Pacote Inicial Garagem: R$ {imovel_obj.calcular_pacote_inicial_garagem():.2f}")
    print(f"Vagas Extras: R$ {imovel_obj.calcular_vagas_extras():.2f}")
    if "apartamento" in tipo_escolhido:
        print(f"Desconto Crianças (5%): - R$ {desconto:.2f}")
    print(f"--> ALUGUEL MENSAL LÍQUIDO: R$ {aluguel_mensal:.2f}")
    print()
    print("-" * 55)
    print()
    print(f"Taxa Contratual Total: R$ {Orcamento.TAXA_CONTRATUAL_TOTAL:.2f}")
    print(f"Forma de Pagamento Taxa: {num_parcelas}x de R$ {parcela_taxa:.2f}")
    print()
    print("=======================================================")
    print()
    
    orcamento.exportar_csv("projecao_locacao.csv")

if __name__ == "__main__":
    menu_interativo()
