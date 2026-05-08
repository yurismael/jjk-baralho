import streamlit as st
import classes_jjk as jjkcl
import feitiços_encantar as jjkfe
import feitiços_geral as jjkfg
import io
import sys

st.set_page_config(page_title="JJK Card Manager", layout="wide", page_icon="🃏")

# --- Inicialização do Estado ---
if 'baralho' not in st.session_state:
    st.session_state.baralho = jjkcl.Baralho()
if 'hand' not in st.session_state:
    st.session_state.hand = jjkcl.Mão()

# --- Utilitários ---
def capturar_saida(func, *args, **kwargs):
    """Executa função e captura prints para exibir no Streamlit"""
    captured = io.StringIO()
    sys.stdout = captured
    try:
        func(*args, **kwargs)
    finally:
        sys.stdout = sys.__stdout__
    return captured.getvalue().strip()

def renderizar_mao(hand):
    if hand.qtd_cartas_na_mão == 0:
        st.info("👐 Mão vazia. Compre cartas no menu lateral.")
        return
    
    cols = st.columns(min(hand.qtd_cartas_na_mão, 5))
    for i, carta in enumerate(hand.cartas):
        with cols[i]:
            with st.container(border=True):
                titulo = f"{'✨' if carta.esta_encantada else ''} {carta.get_ranque()}{carta.icone}"
                st.markdown(f"### {titulo}")
                st.markdown(f"**Tipo:** `{carta.tipo}`")
                
                if carta.esta_encantada:
                    st.success(f"**Encantamento:** `{carta.encantamento.strip()}`")
                if hasattr(carta, 'dados'):
                    st.text(f"Dano: {carta.dados}d{carta.faces}")
                if hasattr(carta, 'bônus'):
                    st.text(f"Bônus: +{carta.bônus}")

# --- Interface Principal ---
def main():
    st.title("🃏 Gerenciador de Baralho JJK")
    st.caption("Sistema de encantamentos baseado em regras de cartas.")

    col_sidebar, col_main = st.columns([1, 3])

    # SIDEBAR: Gestão do Baralho
    with col_sidebar:
        st.header("📦 Baralho")
        st.metric("Cartas no Baralho", st.session_state.baralho.qtd_cartas_no_baralho)
        st.metric("Cartas na Mão", st.session_state.hand.qtd_cartas_na_mão)
        
        st.divider()
        st.subheader("⚡ Ações Rápidas")
        
        if st.button("🔀 Embaralhar"):
            st.session_state.baralho.embaralhar()
            st.success("Baralho embaralhado!")
            st.rerun()

        if st.button("🎴 Comprar 1 Carta"):
            msg = capturar_saida(jjkfg.Comprar_Carta, st.session_state.baralho, st.session_state.hand, qtd=1)
            if msg: st.warning(msg)
            st.rerun()

        if st.session_state.hand.qtd_cartas_na_mão > 0:
            st.subheader("🗑️ Descarte")
            pos_desc = st.number_input("Posição para descartar:", min_value=1, max_value=st.session_state.hand.qtd_cartas_na_mão, step=1)
            if st.button("Descartar Carta"):
                msg = capturar_saida(jjkfg.Descartar_Carta, st.session_state.baralho, st.session_state.hand, pos_desc)
                if msg: st.warning(msg)
                st.rerun()

            st.subheader("💫 Dissipar")
            pos_disp = st.number_input("Posição para dissipar:", min_value=1, max_value=st.session_state.hand.qtd_cartas_na_mão, step=1)
            if st.button("Dissipar Encantamento"):
                msg = capturar_saida(jjkfg.Dissipar_Encantamento, st.session_state.hand, pos_disp)
                if msg: st.warning(msg)
                st.rerun()

    # MAIN: Mão & Feitiços
    with col_main:
        st.subheader("👋 Visualização da Mão")
        renderizar_mao(st.session_state.hand)

        st.divider()
        st.subheader("🔮 Conjurar Feitiço")
        feitico = st.selectbox("Selecione a Técnica:", [
            "Encantar Pôquer", "Encantar Blackjack", "Encantar Truco",
            "Encantar Uno", "Encantar Mentira", "Encantar Presidente & Bobo"
        ])

        col_btn, col_nivel, col_pos = st.columns([2, 1, 1])
        nivel = col_nivel.number_input("Nível (1-10)", min_value=1, max_value=10, value=1, key="nivel_feat")
        pos = col_pos.number_input("Posição (1-5)", min_value=1, max_value=5, value=1, key="pos_feat")

        with col_btn:
            st.write("") # Espaçador visual
            if st.button("✨ Conjurar", type="primary", use_container_width=True):
                msg = ""
                if feitico == "Encantar Pôquer":
                    msg = capturar_saida(jjkfe.Encantar_Pôquer, st.session_state.hand, nivel)
                elif feitico == "Encantar Blackjack":
                    msg = capturar_saida(jjkfe.Encantar_Blackjack, st.session_state.hand, nivel)
                elif feitico == "Encantar Truco":
                    msg = capturar_saida(jjkfe.Encantar_Truco, st.session_state.hand, nivel)
                elif feitico == "Encantar Uno":
                    msg = capturar_saida(jjkfe.Encantar_Uno, st.session_state.hand)
                elif feitico == "Encantar Mentira":
                    msg = capturar_saida(jjkfe.Encantar_Mentira, st.session_state.hand, pos)
                elif feitico == "Encantar Presidente & Bobo":
                    msg = capturar_saida(jjkfe.Encantar_Presidente_Bobo, st.session_state.hand)

                if msg:
                    if "inválido" in msg.lower() or "não pode" in msg.lower() or "cheia" in msg.lower():
                        st.error(msg)
                    else:
                        st.success(msg)
                st.rerun()

if __name__ == "__main__":
    main()