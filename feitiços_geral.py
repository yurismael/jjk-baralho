def Comprar_Carta(baralho, hand, qtd=5):
    if baralho.qtd_cartas_no_baralho < qtd: ## Se o baralho estiver vazio
        print("O baralho está vazio.")
        return
    elif hand.qtd_cartas_na_mão == 5: ## Se a mão já estiver cheia
        print("A mão está cheia.")
        return
    elif qtd <= 0: ## Se a quantidade for negativa ou zero
        print("A quantidade deve ser positiva.")
        return
    elif hand.qtd_cartas_na_mão + qtd > 5: ## Se a quantidade somada a quantidade de cartas na mão for maior que o limite
        qtd = 5 - hand.qtd_cartas_na_mão
        print(f"A quantidade foi reduzida para {qtd}.")

    for i in range(qtd):
        baralho.comprar_carta(hand)
    hand.ver()

def Descartar_Carta(baralho, hand, indices):
    if type(indices) == int:
        indices = [indices]

    qtd = len(indices)
    if qtd == 0: ## Não pode nenhuma
        print("Nenhuma carta foi descartada.")
        return
    elif qtd > 5: ## Não pode mais cartas que tem na mão
        print("Não é possível descartar mais de 5 cartas.")
        return
    elif any(indice < 1 or indice > hand.qtd_cartas_na_mão for indice in indices): ## Não pode descartar alguma carta fora das posições válidas
        print("Posição da carta inválida.")
        return

    ocorrencias = []
    for i in indices:
        if i in ocorrencias: ## Não pode descartar a mesma carta duas vezes
            print("Não é possível descartar a mesma carta duas vezes.")
            return
        ocorrencias.append(i)

    indices.sort(reverse=True)

    for i in indices:
        baralho.descartar_carta(hand, i)
    hand.ver()

def Dissipar_Encantamento(hand, pos):
    if pos < 1 or pos > hand.qtd_cartas_na_mão:
        print("Posição da carta inválida.")
        return

    carta = hand.get_carta(pos)
    if not carta.esta_encantada:
        print("A carta não está encantada.")
        return

    carta.resetar()
    hand.ver()