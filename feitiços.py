import classes as cl

def Comprar_Carta(baralho, hand, qtd=5):
    if baralho.qtd_cartas_no_baralho < qtd:
        print("O baralho está vazio.")
        return
    elif hand.qtd_cartas_na_mão == 5:
        print("A mão está cheia.")
        return
    elif qtd <= 0:
        print("A quantidade deve ser positiva.")
        return
    elif hand.qtd_cartas_na_mão + qtd > 5:
        qtd = 5 - hand.qtd_cartas_na_mão
        print(f"A quantidade foi reduzida para {qtd}.")

    for i in range(qtd):
        baralho.comprar_carta(hand)

def Descartar_Carta(baralho, hand, indices):
    if type(indices) == int:
        indices = [indices]

    qtd = len(indices)
    if qtd == 0:
        print("Nenhuma carta foi descartada.")
        return
    elif qtd > 5:
        print("Não é possível descartar mais de 5 cartas.")
        return
    elif any(indice < 1 or indice > hand.qtd_cartas_na_mão for indice in indices):
        print("Posição da carta inválida.")
        return

    ocorrencias = []
    for i in indices:
        if i in ocorrencias:
            print("Não é possível descartar a mesma carta duas vezes.")
            return
        ocorrencias.append(i)

    indices.sort(reverse=True)

    for i in indices:
        baralho.descartar_carta(hand, i)

def Dissipar_Encantamento(hand, pos):
    if pos < 1 or pos > hand.qtd_cartas_na_mão:
        print("Posição da carta inválida.")
        return

    carta = hand.get_carta(pos)
    if not carta.esta_encantada:
        print("A carta não está encantada.")
        return

    carta.resetar()

def encontrar_poker(hand):
    if hand.qtd_cartas_na_mão != 5:
        print("A mão deve ter 5 cartas.")
        return None

    # Resetar flag de encantar
    for carta in hand.cartas:
        carta.marca_para_encantar = False

    carta_por_naipe = sorted(hand.cartas, key=lambda carta: carta.naipe)
    carta_por_valor = sorted(hand.cartas, key=lambda carta: carta.valor)

    naipes  = [carta.naipe for carta in carta_por_naipe]
    valores = [carta.valor for carta in carta_por_valor]

    ocorrencias = {}
    for valor in valores:
        ocorrencias[valor] = ocorrencias.get(valor, 0) + 1
    numero_de_ocorrencias = list(ocorrencias.values())

    def encantar_todas():
        for carta in hand.cartas:
            carta.marca_para_encantar = True

    royal = False
    straight = False
    flush = False

    if all(n == naipes[0] for n in naipes):
        flush = True

    if valores == [1, 10, 11, 12, 13]:
        royal = True
        straight = True
    else:
        straight = True
        for i in range(4):
            if valores[i + 1] - valores[i] != 1:
                straight = False
                break

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
            if ocorrencias.get(carta.valor, 0) == 4:
                carta.marca_para_encantar = True
        return "Quadra"
    elif 3 in numero_de_ocorrencias:
        if 2 in numero_de_ocorrencias:
            encantar_todas()
            return "Full House"
        else:
            for carta in hand.cartas:
                if ocorrencias.get(carta.valor, 0) == 3:
                    carta.marca_para_encantar = True
            return "Trinca"
    elif 2 in numero_de_ocorrencias:
        for carta in hand.cartas:
            if ocorrencias.get(carta.valor, 0) == 2:
                carta.marca_para_encantar = True
        if numero_de_ocorrencias.count(2) == 2:
            return "Dois Pares"
        else:
            return "Par"
    else:
        for carta in hand.cartas:
            if carta.valor == 1 or carta.valor == max(valores):
                carta.marca_para_encantar = True
                return "Carta Alta"

def Encantar_Pôquer(hand, nivel_feitico):
    if hand.qtd_cartas_na_mão != 5:
        print("A mão deve ter 5 cartas.")
        return

    nivel_mãos_poquer = [
        "Carta Alta", "Par", "Trinca", "Dois Pares",
        "Straight", "Flush", "Full House", "Quadra",
        "Straight Flush", "Royal Flush"
    ]
        

    encantamento = encontrar_poker(hand)
    if encantamento is None:
        return

    valor_de_aumento = nivel_mãos_poquer.index(encantamento) + nivel_feitico 

    for carta in hand.cartas:
        if carta.marca_para_encantar and not carta.esta_encantada:
            carta.esta_encantada = True
            carta.encantamento = "[Pôquer | " + encantamento + "]"
            carta.marca_para_encantar = False

            if isinstance(carta, (cl.Carta_Espadas, cl.Carta_Copas)):
                pq_bonus_dados = [0, 0, 2, 4, 8]
                carta.dados += valor_de_aumento + pq_bonus_dados[nivel_feitico-1]
            elif isinstance(carta, (cl.Carta_Ouros, cl.Carta_Paus)):
                carta.bônus += valor_de_aumento
        elif carta.esta_encantada:
            print(f"A carta {carta.ranque}{carta.icone} já está encantada.")
        else:
            print(f"A carta {carta.ranque}{carta.icone} não pode ser encantada.")

def contar_21(hand):
    if hand.qtd_cartas_na_mão < 1:
        print("Esse feitiço deve ser conjurado com ao menos uma carta na mão.")
        return None

    for carta in hand.cartas:
        carta.marca_para_encantar = False

    def valor_blackjack(valor):
        if valor == 1:
            return 11
        elif valor >= 10:
            return 10
        else:
            return valor

    soma = sum(valor_blackjack(c.valor) for c in hand.cartas)

    if soma == 21:
        for carta in hand.cartas:
            carta.marca_para_encantar = True
        return "Blackjack"

    return None

def Encantar_Blackjack(hand, nivel_feitico):
    if hand.qtd_cartas_na_mão < 1:
        print("Esse feitiço deve ser conjurado com ao menos uma carta na mão.")
        return

    encantamento = contar_21(hand)
    if encantamento != "Blackjack":
        print("A mão não forma Blackjack.")
        return

    valor_de_aumento = 6 + 2 * (nivel_feitico - 1)

    for carta in hand.cartas:
        if carta.marca_para_encantar and not carta.esta_encantada:
            carta.esta_encantada = True
            carta.encantamento = "[Blackjack]"
            carta.marca_para_encantar = False

            if isinstance(carta, (cl.Carta_Espadas, cl.Carta_Copas)):
                carta.dados += valor_de_aumento
            elif isinstance(carta, (cl.Carta_Ouros, cl.Carta_Paus)):
                carta.bônus += valor_de_aumento
        elif carta.esta_encantada:
            print(f"A carta {carta.ranque}{carta.icone} já está encantada.")
        else:
            print(f"A carta {carta.ranque}{carta.icone} não pode ser encantada.")

def manilha_vira(hand):
    if hand.qtd_cartas_na_mão < 2:
        print("Esse feitiço deve ser conjurado com ao menos duas cartas na mão.")
        return None

    for carta in hand.cartas:
        carta.marca_para_encantar = False

    sequencia_truco = [3, 2, 1, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4]

    # A última carta da mão é a "vira"
    vira_valor = hand.get_carta(hand.qtd_cartas_na_mão).valor
    indice_vira = sequencia_truco.index(vira_valor)

    # A manilha é a carta seguinte na sequência (circularmente)
    indice_manilha = (indice_vira + 1) % len(sequencia_truco)
    valor_manilha = sequencia_truco[indice_manilha]

    for carta in hand.cartas[:-1]:  # Não marca a vira
        if carta.valor == valor_manilha:
            carta.marca_para_encantar = True

    if any(carta.marca_para_encantar for carta in hand.cartas):
        return "Truco"

    return None

def Encantar_Truco(hand, nivel_feitico):
    if hand.qtd_cartas_na_mão < 2:
        print("Esse feitiço deve ser conjurado com ao menos duas cartas na mão.")
        return

    naipes_truco = ["paus", "copas", "espadas", "ouros"]

    encantamento = manilha_vira(hand)
    if encantamento != "Truco":
        print("Nenhuma manilha encontrada na mão.")
        return

    valor_de_aumento = 6 + 2*(nivel_feitico - 1)

    for carta in hand.cartas:
        if carta.marca_para_encantar and not carta.esta_encantada:
            carta.esta_encantada = True
            carta.encantamento = "[Truco]"
            carta.marca_para_encantar = False

            bonus_naipe = 1 - naipes_truco.index(carta.naipe) if carta.naipe in naipes_truco else 0

            if isinstance(carta, (cl.Carta_Espadas, cl.Carta_Copas)):
                carta.dados += valor_de_aumento + bonus_naipe
            elif isinstance(carta, (cl.Carta_Ouros, cl.Carta_Paus)):
                carta.bônus += valor_de_aumento + bonus_naipe
        elif carta.esta_encantada:
            print(f"A carta {carta.ranque}{carta.icone} já está encantada.")
        else:
            print(f"A carta {carta.ranque}{carta.icone} não pode ser encantada.")

def Encantar_Uno(hand):
    if hand.qtd_cartas_na_mão != 1:
        print("A mão deve ter apenas uma carta.")
        return

    carta = hand.get_carta(1)
    carta.esta_encantada = True
    carta.encantamento = "[Uno]"
    carta.tipo = "Especial"

def Encantar_Mentira(hand, pos):
    if pos < 1 or pos > hand.qtd_cartas_na_mão:
        print("Posição da carta inválida.")
        return

    carta = hand.get_carta(pos)
    carta.esta_encantada = True
    carta.encantamento = "[Mentira]"
    carta.tipo = "Especial"

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