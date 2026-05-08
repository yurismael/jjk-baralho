import random

class Carta:
    def __init__(self, naipe, valor):
        self.naipe = naipe
        self.valor = valor
        self.tipo = ""

        self.esta_encantada = False
        self.encantamento = ""
        self.encantar = False

    def resetar(self):
        self.esta_encantada = False
        self.encantamento = ""
        self.encantar = False

    def simbolo(self):
        if "Pôquer" in self.encantamento:
            return "p"
        elif "Blackjack" in self.encantamento:
            return "b"
        elif "Truco" in self.encantamento:
            return "t"
        elif "Uno" in self.encantamento:
            return "u"
        elif "Mentira" in self.encantamento:
            return "m"
        elif "P&B" in self.encantamento:
            if "Presidente" in self.encantamento:
                return ">" 
            else: 
                return "<"
        else:
            return ""

    def desc(self):
        return

    def ver(self):
        string = []

        ranque = self.get_ranque()
        naipe = self.icone

        if self.esta_encantada:
            estrelinha = self.simbolo()
        else:
            estrelinha = ""

        string.append("┌")
        string.append("| Carta: " + estrelinha + ranque + naipe)
        string.append("| Tipo: " + self.tipo)

        if self.esta_encantada:
            string.append("| Encantamento: " + self.encantamento)

        string.append("| Descrição: " + self.desc())
        string.append("└")
        string = "\n".join(string)

        print(string)

    def get_ranque(self):
        if self.valor == 1:     return "A"
        elif self.valor == 11:  return "J"
        elif self.valor == 12:  return "Q"
        elif self.valor == 13:  return "K"
        else:                   return str(self.valor)

class Carta_Espadas(Carta):
    naipe = "espadas"
    icone = "♠"

    def __init__(self, valor):
        super().__init__("espadas", valor)

        self.tipo = "Dano"
        self.dados = 1
        self.faces = 8
        self.tipo_dano = "cortante"

    def desc(self):
        if "Uno" in self.encantamento:
            return "O próximo dano causado ou recebido será alterado para um tipo escolhido."
        elif "Mentira" in self.encantamento:
            return "Ao ser lançada deve ser resistida com um TR Astúcia para detectar a mentira. Se passar, a carta não tem efeito. Se falhar, o usuário pode escolher uma das cartas da mão para copiar."  
        elif "P&B" in self.encantamento:
            if "Presidente" in self.encantamento:
                return "Garante um sucesso automático no próximo teste de ataque, resistência ou perícia."
            else: 
                return "Garante uma falha automática no próximo teste de ataque, resistência ou perícia."
        
        return f"Causa {self.dados}d{self.faces} de dano {self.tipo_dano}."

    def resetar(self):
        self.esta_encantada = False
        self.encantamento = ""
        self.encantar = False

        if self.tipo == "Especial":
            self.tipo = "Dano"

        self.dados = 1
        self.faces = 8


class Carta_Copas(Carta):
    naipe = "copas"
    icone = "♥"

    def __init__(self, valor):
        super().__init__("copas", valor)

        self.tipo = "Cura"
        self.dados = 1
        self.faces = 6

    def desc(self):
        if "Uno" in self.encantamento:
            return "O próximo dano recebido se torna cura ou a próxima cura recebida se torna dano."
        elif "Mentira" in self.encantamento:
            return "Ao ser lançada deve ser resistida com um TR Astúcia para detectar a mentira. Se passar, a carta não tem efeito. Se falhar, o usuário pode escolher uma das cartas da mão para copiar."  
        elif "P&B" in self.encantamento:
            if "Presidente" in self.encantamento:
                return "Garante um sucesso automático no próximo teste de ataque, resistência ou perícia."
            else: 
                return "Garante uma falha automática no próximo teste de ataque, resistência ou perícia."
        
        return f"Cura {self.dados}d{self.faces} de HP temporário."

    def resetar(self):
        self.esta_encantada = False
        self.encantamento = ""
        self.encantar = False

        if self.tipo == "Especial":
            self.tipo = "Cura"

        self.dados = 1
        self.faces = 6

class Carta_Ouros(Carta):
    naipe = "ouros"
    icone = "♦"

    def __init__(self, valor):
        super().__init__("ouros", valor)

        self.tipo = "Auxiliar"
        self.bônus = 1

    def desc(self):
        if "Uno" in self.encantamento:
            return "O próximo ataque receberá +4 de margem de crítico."
        elif "Mentira" in self.encantamento:
            return "Ao ser lançada deve ser resistida com um TR Astúcia para detectar a mentira. Se passar, a carta não tem efeito. Se falhar, o usuário pode escolher uma das cartas da mão para copiar."  
        elif "P&B" in self.encantamento:
            if "Presidente" in self.encantamento:
                return "Garante um sucesso automático no próximo teste de ataque, resistência ou perícia."
            else: 
                return "Garante uma falha automática no próximo teste de ataque, resistência ou perícia."
        
        return f"Recebe +{self.bônus} no próximo teste de perícia, ataque ou resistência."

    def resetar(self):
        self.esta_encantada = False
        self.encantamento = ""
        self.encantar = False

        if self.tipo == "Especial":
            self.tipo = "Auxiliar"

        self.bônus = 1

class Carta_Paus(Carta):
    naipe = "paus"
    icone = "♣"

    def __init__(self, valor):
        super().__init__("paus", valor)

        self.tipo = "Defesa"
        self.bônus = 1

    def desc(self):
        if "Uno" in self.encantamento:
            return "O inimigo não poderá ativar sua técnica amaldiçoada nessa rodada."
        elif "Mentira" in self.encantamento:
            return "Ao ser lançada deve ser resistida com um TR Astúcia para detectar a mentira. Se passar, a carta não tem efeito. Se falhar, o usuário pode escolher uma das cartas da mão para copiar."  
        elif "P&B" in self.encantamento:
            if "Presidente" in self.encantamento:
                return "Garante um sucesso automático no próximo teste de ataque, resistência ou perícia."
            else: 
                return "Garante uma falha automática no próximo teste de ataque, resistência ou perícia."
        
        return f"Recebe +{self.bônus} de defesa durante o próximo ataque recebido."

    def resetar(self):
        self.esta_encantada = False
        self.encantamento = ""
        self.encantar = False

        if self.tipo == "Especial":
            self.tipo = "Defesa"

        self.bônus = 1

class Mão:
    def __init__(self):
        self.cartas = []
        self.qtd_cartas_na_mão = 0

    def inserir_carta(self, carta):
        if self.qtd_cartas_na_mão == 5: ## Limite padrão de quantas cartas o usuário pode ter na mão
            print("A mão está cheia.")
            return
        self.cartas.append(carta)
        self.qtd_cartas_na_mão += 1

    def remover_carta(self, carta):
        if carta not in self.cartas:
            print("A carta não está na mão.")
            return
        self.cartas.remove(carta)
        self.qtd_cartas_na_mão -= 1

    def get_carta(self, posicao): ## A referenciação está sendo feita a partir do índice 1
        if posicao < 1 or posicao > self.qtd_cartas_na_mão:
            print("Posição da carta inválida.")
            return
        return self.cartas[posicao-1]

    def ver(self):
        if self.qtd_cartas_na_mão == 0:
            print("A mão está vazia.")
            return

        string = []

        for carta in self.cartas:
            ranque = carta.get_ranque()
            naipe = carta.icone

            if carta.esta_encantada:
                estrelinha = carta.simbolo()
            else:
                estrelinha = ""

            string.append(estrelinha)
            string.append(f"{ranque}{naipe}")
            string.append(" | ")

        string = "".join(string)
        string = "| " + string

        print(string)

class Baralho:
    def __init__(self):
        self.cartas = []
        self.qtd_cartas_no_baralho = 0

        for i in range(13):
            self.cartas.append(Carta_Espadas(i+1))
            self.cartas.append(Carta_Copas(i+1))
            self.cartas.append(Carta_Ouros(i+1))
            self.cartas.append(Carta_Paus(i+1))

            self.qtd_cartas_no_baralho += 4

        self.embaralhar()

    def embaralhar(self):
        random.shuffle(self.cartas)

    def comprar_carta(self, hand):
        if self.qtd_cartas_no_baralho <= 0:
            print("O baralho está vazio.")
            return
        carta = self.cartas.pop()
        hand.inserir_carta(carta)
        self.qtd_cartas_no_baralho -= 1

    def descartar_carta(self, hand, pos):
        if pos < 1 or pos > hand.qtd_cartas_na_mão:
            print("Posição da carta inválida.")
            return
        carta = hand.get_carta(pos)
        hand.remover_carta(carta)

        carta.resetar()

        self.cartas.append(carta)
        self.qtd_cartas_no_baralho += 1
        self.embaralhar()
