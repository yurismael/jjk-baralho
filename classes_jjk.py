import random
from typing import List, Dict, Any, Optional

# Constantes centralizadas (fácil manutenção)
MAX_HAND = 5
SUIT_ICONS = {"espadas": "♠", "copas": "♥", "ouros": "♦", "paus": "♣"}
RANKS = {1: "A", 11: "J", 12: "Q", 13: "K"}

class Carta:
    def __init__(self, naipe: str, valor: int):
        self.naipe = naipe
        self.valor = valor
        
        self.esta_encantada = False
        self.encantamento = ""
        self.marca_para_encantar = False
        
        self.tipo = ""
        self.tipo_original = ""

    @property
    def ranque(self) -> str: 
        return RANKS.get(self.valor, str(self.valor))
    @property
    def icone(self) -> str: 
        return SUIT_ICONS.get(self.naipe, "?")

    def desc_especial(self):
        if "Mentira" in self.encantamento:
            return "Pode escolher uma das cartas da mão para copiar (TR Astúcia para anular)."
        elif "P&B" in self.encantamento:
            if "Presidente" in self.encantamento:
                return "Garante um sucesso automático no próximo teste de ataque, resistência ou perícia."
            else:
                return "Garante uma falha automática no próximo teste de ataque, resistência ou perícia."
        else:
            return "Erro!"

    def resetar(self):
        self.esta_encantada = False
        self.encantamento = ""
        self.marca_para_encantar = False
        
        if self._tipo_base: 
            self.tipo = self._tipo_base

class Carta_Espadas(Carta):
    def __init__(self, valor: int):
        super().__init__("espadas", valor)
        
        self.tipo = "Ofensivo"; 
        self._tipo_base = "Ofensivo"
        
        self.dados, self.faces = 1, 8
        self.tipo_dano = "cortante"
    
    def desc(self):
        if self.tipo == "Ofensivo":
            return f"Causa {self.dados}d{self.faces} de dano {self.tipo_dano}."
        elif self.encantamento == "[Uno]":
            return "O próximo dano causado ou recebido será alterado para um tipo escolhido."
        else: 
            return super.desc_especial()
    
    def resetar(self):
        super.resetar()
        self.dados, self.faces = 1, 8
        self.tipo_dano = "cortante"

class Carta_Copas(Carta):
    def __init__(self, valor: int):
        super().__init__("copas", valor)
        
        self.tipo = "Curativo"; 
        self._tipo_base = "Curativo"
        
        self.dados, self.faces = 1, 6
    
    def desc(self):
        if self.tipo == "Curativo":
            return f"Cura {self.dados}d{self.faces} de HP temporário."
        elif self.encantamento == "[Uno]":
            return "O próximo dano recebido se torna cura ou a próxima cura recebida se torna dano."
        else: 
            return super.desc_especial()
        
    def resetar(self):
        super.resetar()
        self.dados, self.faces = 1, 6

class Carta_Ouros(Carta):
    def __init__(self, valor: int):
        super().__init__("ouros", valor)
        
        self.tipo = "Auxiliar"; 
        self._tipo_base = "Auxiliar"
        
        self.bônus = 1
    
    def desc(self):
        if self.tipo == "Auxiliar":
            return f"Recebe +{self.bônus} no próximo teste de perícia, ataque ou resistência."
        elif self.encantamento == "[Uno]":
            return "O próximo ataque receberá +4 de margem de crítico."
        else: 
            return super.desc_especial()

    def resetar(self):
        super.resetar()
        self.bônus = 1

class Carta_Paus(Carta):
    def __init__(self, valor: int):
        super().__init__("paus", valor)
        
        self.tipo = "Defensivo"; 
        self._tipo_base = "Defensivo"
        
        self.bônus = 1
    
    def desc(self):
        if self.tipo == "Auxiliar":
            return f"Recebe +{self.bônus} no próximo teste de perícia, ataque ou resistência."
        elif self.encantamento == "[Uno]":
            return "Bloqueia uma técnica amaldiçoada por 1 rodada."
        else: 
            return super.desc_especial()

    def resetar(self):
        super.resetar()
        self.bônus = 1

class Mão:
    def __init__(self): 
        self.cartas: List[Carta] = []
    
    @property
    def qtd(self) -> int: 
        return len(self.cartas)

    def adicionar(self, carta: Carta) -> str:
        if self.qtd >= MAX_HAND: 
            return "A mão está cheia."
        self.cartas.append(carta); 
        return "Carta adicionada."

    def remover(self, pos: int) -> str:
        if not (1 <= pos <= self.qtd): 
            return "Posição inválida."
        self.cartas.pop(pos - 1); 
        return "Carta removida."

    def pegar(self, pos: int) -> Optional[Carta]:
        return self.cartas[pos - 1] if 1 <= pos <= self.qtd else None

class Baralho:
    def __init__(self):
        self.cartas: List[Carta] = []
        self._inicializar()

    def _inicializar(self):
        self.cartas.clear()
        for v in range(1, 14):
            self.cartas.extend([Carta_Espadas(v), Carta_Copas(v), Carta_Ouros(v), Carta_Paus(v)])
        self.embaralhar()

    def embaralhar(self): 
        random.shuffle(self.cartas)

    def comprar_carta(self, hand: Mão) -> str:
        if self.qtd == 0: 
            return "Baralho vazio."
        carta = self.cartas.pop()
        return hand.adicionar(carta)

    def descartar_carta(self, hand: Mão, pos: int) -> str:
        carta = hand.pegar(pos) 
        if not carta: 
            return "Posição inválida."
        hand.remover(pos)
        carta.resetar()
        
        self.cartas.append(carta)
        self.embaralhar()
        return "Carta descartada e reembaralhada."