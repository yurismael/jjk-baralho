import classes_jjk as cl

def encontrar_poker(hand):
    if hand.qtd_cartas_na_mão != 5:
        print("A mão deve ter 5 cartas.")
        return

    carta_por_naipe = sorted(hand.cartas, key=lambda carta: carta.naipe)
    carta_por_valor = sorted(hand.cartas, key=lambda carta: carta.valor)

    naipes =  [carta.naipe for carta in carta_por_naipe]
    valores = [carta.valor for carta in carta_por_valor]

    ocorrencias = {}
    for valor in valores:
        if valor in ocorrencias:
            ocorrencias[valor] += 1
        else:
            ocorrencias[valor] = 1
    numero_de_ocorrencias = list(ocorrencias.values())

    def encantar_todas():
        for carta in hand.cartas:
            carta.encantar = True

    royal = False
    straight = False
    flush = False

    if all(i == naipes[0] for i in naipes):
        flush = True
    for i in range(5):
        if valores == [1, 10, 11, 12, 13]:
            royal = True
            break
        elif valores[i+1] - valores[i] != 1:
            straight = False
            break
        straight = True
    if royal and flush:
        encantar_todas()
        return "Royal Flush"
    elif straight and flush:
        encantar_todas()
        return "Straight Flush"
    elif straight:
        encantar_todas()
        return "Straight"
    elif flush:
        encantar_todas()
        return "Flush"
    elif 4 in numero_de_ocorrencias:
        for carta in hand.cartas:
            if carta.valor in ocorrencias and ocorrencias[carta.valor] == 4:
                carta.encantar = True
        return "Quadra"
    elif 3 in numero_de_ocorrencias:
        if 2 in numero_de_ocorrencias:
            encantar_todas()
            return "Full House"
        else:
            for carta in hand.cartas:
                if carta.valor in ocorrencias and ocorrencias[carta.valor] == 3:
                    carta.encantar = True
            return "Trinca"
    elif 2 in numero_de_ocorrencias:
        for carta in hand.cartas:
            if carta.valor in ocorrencias and ocorrencias[carta.valor] == 2:
                carta.encantar = True
        if numero_de_ocorrencias.count(2) == 2:
            return "Dois Pares"
        else:
            return "Par"
    else:
        for carta in hand.cartas:
            if carta.valor == 1:
                carta.encantar = True
            elif carta.valor == max(valores):
                carta.encantar = True
        return "Carta Alta"

def Encantar_Pôquer(hand, nivel_feitico):
    if hand.qtd_cartas_na_mão != 5:
        print("A mão deve ter 5 cartas.")
        return

    nivel_mãos_poquer = ["Carta Alta", "Par", "Trinca", "Dois Pares", "Straight", "Flush", "Full House", "Quadra", "Straight Flush", "Royal Straight Flush"]

    encantamento = encontrar_poker(hand)
    valor_de_aumento = nivel_mãos_poquer.index(encantamento) + nivel_feitico

    for carta in hand.cartas:
        if carta.encantar and not carta.esta_encantada: ## Encanta apenas as cartas permitidas e que não possuem um encantamento
            carta.esta_encantada = True
            carta.encantamento = "[Pôquer | " + encantamento + "]"
            carta.encantar = False

            if isinstance(carta, cl.Carta_Espadas) or isinstance(carta, cl.Carta_Copas):
                carta.dados += valor_de_aumento
            elif isinstance(carta, cl.Carta_Ouros) or isinstance(carta, cl.Carta_Paus):
                carta.bônus += valor_de_aumento
            else:
                print("Tipo de carta inválido para encantar com esse feitiço.")
        elif carta.esta_encantada: ## Se a carta já estiver encantada
            print(f"A carta {carta.get_ranque()}{carta.icone} já está encantada.")
        else: ## Se a carta não deve ser encantada por algum motivo
            print(f"A carta {carta.get_ranque()}{carta.icone} não pode ser encantada.")
    hand.ver()

def contar_21(hand):
    if hand.qtd_cartas_na_mão < 1:
        print("Esse feitiço deve ser conjurado com ao menos uma carta na mão.")
        return

    cartas_por_valor = sorted(hand.cartas, key=lambda carta:carta.valor)
    valores = [carta.valor for carta in cartas_por_valor]

    def valor_blackjack(valor):
        if valor == 1:
            return 11
        elif valor >= 10:
            return 10
        else:
            return valor

    valores_blackjack = [valor_blackjack(valor) for valor in valores]
    soma = sum(valores_blackjack)

    if soma == 21:
        for carta in hand.cartas:
            carta.encantar = True
        return "Blackjack"

def Encantar_Blackjack(hand, nivel_feitico):
    if hand.qtd_cartas_na_mão < 1:
        print("Esse feitiço deve ser conjurado com ao menos uma carta na mão.")
        return

    encantamento = contar_21(hand)
    valor_de_aumento = 6 + nivel_feitico - 1

    if encantamento == "Blackjack":
        for carta in hand.cartas:
            if carta.encantar and not carta.esta_encantada: ## Encanta apenas as cartas habilitadas e que não possuem um encantamento anterior
                carta.esta_encantada = True
                carta.encantamento = "[Blackjack]"
                carta.encantar = False

                if isinstance(carta, cl.Carta_Espadas) or isinstance(carta, cl.Carta_Copas):
                    carta.dados += valor_de_aumento
                elif isinstance(carta, cl.Carta_Ouros) or isinstance(carta, cl.Carta_Paus):
                    carta.bônus += valor_de_aumento
                else:
                    print("Tipo de carta inválido para encantar com esse feitiço.")
            elif carta.esta_encantada: ## Se a carta já estiver encantada
                print(f"A carta {carta.get_ranque()}{carta.icone} já está encantada.")
            else: ## Se a carta não deve ser encantada por algum motivo
                print(f"A carta {carta.get_ranque()}{carta.icone} não pode ser encantada.")
    hand.ver()

def manilha_vira(hand):
    if hand.qtd_cartas_na_mão < 2:
        print("Esse feitiço deve ser conjurado com ao menos duas cartas na mão.")
        return

    sequencia_truco = [3, 2, 1, 13, 11, 12, 10, 9, 8, 7, 6, 5, 4]
    naipes_truco = ["paus", "copas", "espadas", "ouros"]

    manilha = hand.get_carta(hand.qtd_cartas_na_mão).valor
    indice_manilha = sequencia_truco.index(manilha)

    for carta in hand.cartas:
        if indice_manilha == 0:
            if carta.valor == sequencia_truco[-1]:
                carta.encantar = True
        elif carta.valor == sequencia_truco[indice_manilha-1]:
            carta.encantar = True

    if any(carta.encantar for carta in hand.cartas):
        return "Truco"

def Encantar_Truco(hand, nivel_feitico):
    if hand.qtd_cartas_na_mão < 2:
        print("Esse feitiço deve ser conjurado com ao menos duas cartas na mão.")
        return

    naipes_truco = ["paus", "copas", "espadas", "ouros"]

    encantamento = manilha_vira(hand)
    valor_de_aumento = 6 + nivel_feitico - 1

    if encantamento == "Truco":
        for carta in hand.cartas:
            if carta.encantar and not carta.esta_encantada: ## Encanta apenas as cartas
                carta.esta_encantada = True
                carta.encantamento = encantamento
                carta.encantar = False

                if isinstance(carta, cl.Carta_Espadas) or isinstance(carta, cl.Carta_Copas):
                    carta.dados += valor_de_aumento + (3 - naipes_truco.index(carta.naipe))
                elif isinstance(carta, cl.Carta_Ouros) or isinstance(carta, cl.Carta_Paus):
                    carta.bônus += valor_de_aumento + (3 - naipes_truco.index(carta.naipe))
                else:
                    print("Tipo de carta inválido para encantar com esse feitiço.")
            elif carta.esta_encantada: ## Se a carta já estiver encantada
                print(f"A carta {carta.get_ranque()}{carta.icone} já está encantada.")
            else:
                print(f"A carta {carta.get_ranque()}{carta.icone} não pode ser encantada.")
    hand.ver()

def Encantar_Uno(hand):
    if hand.qtd_cartas_na_mão != 1:
        print("A mão deve ter apenas uma carta.")
        return

    carta = hand.get_carta(1)

    carta.esta_encantada = True
    carta.encantamento = "[Uno]"
    
    carta.tipo = "Especial"

    hand.ver()

def Encantar_Mentira(hand, pos):
    if pos < 1 or pos > hand.qtd_cartas_na_mão:
        print("Posição da carta inválida.")
        return

    carta = hand.get_carta(pos)

    carta.esta_encantada = True
    carta.encantamento = "[Mentira]"
    
    carta.tipo = "Especial"

    hand.ver()

def Encantar_Presidente_Bobo(hand):
    if hand.qtd_cartas_na_mão != 2:
        print("A mão deve ter duas cartas.")
        return

    carta1 = hand.get_carta(1)
    carta2 = hand.get_carta(2)

    carta1.esta_encantada = True
    carta1.encantamento = "[P&B | Presidente]"
    
    carta1.tipo = "Especial"

    carta2.esta_encantada = True
    carta2.encantamento = "[P&B | Bobo]"
    
    carta2.tipo = "Especial"

    hand.ver()