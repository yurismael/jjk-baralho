import streamlit as st
import classes_jjk as cl
import feitiços_encantar as fe
import feitiços_geral as fg

if 'baralho' not in st.session_state:
    st.session_state.baralho = cl.Baralho()
if 'hand' not in st.session_state:
    st.session_state.hand = cl.Mão()

st.set_page_config(layout="wide")
st.title("Gerenciador do Baralho")

def display_hand_streamlit():
    st.write("### Mão Atual:")
    if st.session_state.hand.qtd_cartas_na_mão == 0:
        st.write("A mão está vazia.")
        return

    string = []
    for carta in st.session_state.hand.cartas:
        ranque = carta.get_ranque()
        naipe = carta.icone

        if carta.esta_encantada:
            estrelinha = carta.simbolo()
        else:
            estrelinha = ""

        string.append(f"{estrelinha}{ranque}{naipe}")

    string_output = " | ".join(string)
    st.markdown(f"**| {string_output} |**")

# Display the current hand initially
display_hand_streamlit()
st.markdown("--- Feltros dos Feitiços ---")

# --- Spell Sections ---

# Comprar_Carta
st.subheader("Comprar Carta 🛍️")
col1, col2 = st.columns([1, 2])
with col1:
    qtd_comprar = st.number_input("Quantidade para comprar", min_value=1, max_value=5 - st.session_state.hand.qtd_cartas_na_mão, value=1, key="qtd_comprar")
with col2:
    if st.button("Comprar Carta", key="btn_comprar", help="Adiciona uma ou mais cartas à sua mão."):
        if qtd_comprar > 0:
            fg.Comprar_Carta(st.session_state.baralho, st.session_state.hand, qtd_comprar)
        display_hand_streamlit()

st.markdown("---")

# Descartar_Carta
st.subheader("Descartar Carta 🗑️")
col1, col2 = st.columns([1, 2])
with col1:
    max_pos = st.session_state.hand.qtd_cartas_na_mão if st.session_state.hand.qtd_cartas_na_mão > 0 else 1
    pos_descartar = st.number_input("Posição da carta para descartar (1-5)", min_value=1, max_value=max_pos, value=1, key="pos_descartar")
with col2:
    if st.button("Descartar Carta", key="btn_descartar", help="Remove uma carta da sua mão e a retorna ao baralho."):
        if 1 <= pos_descartar <= st.session_state.hand.qtd_cartas_na_mão:
            fg.Descartar_Carta(st.session_state.baralho, st.session_state.hand, pos_descartar)
        else:
            st.warning("Posição inválida para descartar.")
        display_hand_streamlit()

st.markdown("---")

# Dissipar_Encantamento
st.subheader("Dissipar Encantamento ✨")
col1, col2 = st.columns([1, 2])
with col1:
    max_pos = st.session_state.hand.qtd_cartas_na_mão if st.session_state.hand.qtd_cartas_na_mão > 0 else 1
    pos_dissipar = st.number_input("Posição da carta para dissipar (1-5)", min_value=1, max_value=max_pos, value=1, key="pos_dissipar")
with col2:
    if st.button("Dissipar Encantamento", key="btn_dissipar", help="Remove qualquer encantamento de uma carta."):
        if 1 <= pos_dissipar <= st.session_state.hand.qtd_cartas_na_mão:
            fg.Dissipar_Encantamento(st.session_state.hand, pos_dissipar)
        else:
            st.warning("Posição inválida para dissipar.")
        display_hand_streamlit()

st.markdown("---")

# Encantar_Pôquer
st.subheader("Encantar Pôquer ♠️♥️♦️♣️")
col1, col2 = st.columns([1, 2])
with col1:
    nivel_poker = st.number_input("Nível do Feitiço Pôquer", min_value=0, value=1, key="nivel_poker")
with col2:
    if st.button("Encantar Pôquer", key="btn_poker", help="Encanta cartas com base em combinações de pôquer na mão."):
        fe.Encantar_Pôquer(st.session_state.hand, nivel_poker)
        display_hand_streamlit()

st.markdown("---")

# Encantar_Blackjack
st.subheader("Encantar Blackjack 2️⃣1️⃣")
col1, col2 = st.columns([1, 2])
with col1:
    nivel_blackjack = st.number_input("Nível do Feitiço Blackjack", min_value=0, value=1, key="nivel_blackjack")
with col2:
    if st.button("Encantar Blackjack", key="btn_blackjack", help="Encanta cartas se a soma total se aproximar de 21."):
        fe.Encantar_Blackjack(st.session_state.hand, nivel_blackjack)
        display_hand_streamlit()

st.markdown("---")

# Encantar_Truco
st.subheader("Encantar Truco 💪")
col1, col2 = st.columns([1, 2])
with col1:
    nivel_truco = st.number_input("Nível do Feitiço Truco", min_value=0, value=1, key="nivel_truco")
with col2:
    if st.button("Encantar Truco", key="btn_truco", help="Encanta cartas com base nas regras do truco."):
        fe.Encantar_Truco(st.session_state.hand, nivel_truco)
        display_hand_streamlit()

st.markdown("---")

# Encantar_Uno
st.subheader("Encantar Uno 🌈")
if st.button("Encantar Uno", key="btn_uno", help="Encanta a única carta na mão com o feitiço Uno."):
    fe.Encantar_Uno(st.session_state.hand)
    display_hand_streamlit()

st.markdown("---")

# Encantar_Mentira
st.subheader("Encantar Mentira 🤥")
col1, col2 = st.columns([1, 2])
with col1:
    max_pos = st.session_state.hand.qtd_cartas_na_mão if st.session_state.hand.qtd_cartas_na_mão > 0 else 1
    pos_mentira = st.number_input("Posição da carta para Mentira (1-5)", min_value=1, max_value=max_pos, value=1, key="pos_mentira")
with col2:
    if st.button("Encantar Mentira", key="btn_mentira", help="Encanta uma carta para o feitiço Mentira."):
        if 1 <= pos_mentira <= st.session_state.hand.qtd_cartas_na_mão:
            fe.Encantar_Mentira(st.session_state.hand, pos_mentira)
        else:
            st.warning("Posição inválida para Encantar Mentira.")
        display_hand_streamlit()

st.markdown("---")

# Encantar_Presidente_Bobo
st.subheader("Encantar Presidente Bobo 👑🤡")
if st.button("Encantar Presidente Bobo", key="btn_pb", help="Encanta duas cartas com os feitiços Presidente e Bobo."):
    fe.Encantar_Presidente_Bobo(st.session_state.hand)
    display_hand_streamlit()

st.markdown("--- Fim dos Feitiços ---")