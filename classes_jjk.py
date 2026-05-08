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
        self.tipo = ""
        
        self.esta_encantada = False
        self.encantamento = ""
        self.marca_para_encantar = False
        
        self.dados = 1
        self.faces = 6
        self.bônus = 0
        
        self.tipo_dano = ""
        self._tipo_base = ""

    @property
    def ranque(self) -> str: 
        return RANKS.get(self.valor, str(self.valor))
    @property
    def icone(self) -> str: 
        return SUIT_ICONS.get(self.naipe, "?")

    def desc(self) -> str: ## Não gostei dessa
        if self.encantamento == "[Uno]": 
            return "Altera tipo de efeito no próximo uso."
        if self.encantamento == "[Mentira]": 
            return "Exige TR Astúcia. Falha = cópia de carta da mão."
        if "P&B" in self.encantamento: 
            return "Presidente: Sucesso auto. | Bobo: Falha auto."
        return f"{self.tipo}: {self.dados}d{self.faces} | Bônus: +{self.bônus}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "naipe": self.naipe, 
            "valor": self.valor, 
            "tipo": self.tipo,
            "esta_encantada": self.esta_encantada, 
            "encantamento": self.encantamento,
            "marca_para_encantar": self.marca_para_encantar,
            "dados": self.dados, 
            "faces": self.faces, 
            "bônus": self.bônus,
            "tipo_dano": self.tipo_dano, 
            "tipo_base": self._tipo_base
        }

    def resetar(self):
        self.esta_encantada = False
        self.encantamento = ""
        self.marca_para_encantar = False
        
        if self._tipo_base: 
            self.tipo = self._tipo_base
        self.dados, self.faces, self.bônus = 1, 6, 0

class Carta_Espadas(Carta):
    def __init__(self, valor: int):
        super().__init__("espadas", valor)
        self.tipo = "Dano"; 
        self._tipo_base = "Dano"
        self.faces = 8; 
        self.tipo_dano = "cortante"

class Carta_Copas(Carta):
    def __init__(self, valor: int):
        super().__init__("copas", valor)
        self.tipo = "Cura"; 
        self._tipo_base = "Cura"

class Carta_Ouros(Carta):
    def __init__(self, valor: int):
        super().__init__("ouros", valor)
        self.tipo = "Auxiliar"; 
        self._tipo_base = "Auxiliar"

class Carta_Paus(Carta):
    def __init__(self, valor: int):
        super().__init__("paus", valor)
        self.tipo = "Defesa"; 
        self._tipo_base = "Defesa"

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

    def to_dict(self) -> Dict[str, Any]:
        return {"cartas": [c.to_dict() for c in self.cartas]}

class Baralho:
    def __init__(self):
        self.cartas: List[Carta] = []
        self._inicializar()

    def _inicializar(self):
        self.cartas.clear()
        for v in range(1, 14):
            self.cartas.extend([Carta_Espadas(v), Carta_Copas(v), Carta_Ouros(v), Carta_Paus(v)])
        self.embaralhar()

    @property
    def qtd(self) -> int: 
        return len(self.cartas)
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

    def to_dict(self) -> Dict[str, Any]:
        return {"cartas": [c.to_dict() for c in self.cartas]}

# Fábrica para reconstruir objetos a partir de dicts (essencial para Streamlit)
def criar_carta(data: Dict[str, Any]) -> Carta:
    mapping = {"espadas": Carta_Espadas, "copas": Carta_Copas, "ouros": Carta_Ouros, "paus": Carta_Paus}
    carta = mapping[data["naipe"]](data["valor"])
    carta.__dict__.update(data)
    return carta