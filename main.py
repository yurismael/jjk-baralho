import streamlit as st
import classes_jjk as jjk
import feitiços_encantar as jjkfe
import feitiços_geral as jjkfg

st.set_page_config(page_title="JJK Baralho", layout="wide", page_icon="🃏")

# 🔄 Estado Global (Persiste entre reruns)
if "baralho" not in st.session_state:
    st.session_state.baralho = jjk.Baralho()
if "hand" not in st.session_state:
    st.session_state.hand = jjk.Mão()


# 🃏 Renderizador de Carta com Hover
def render_carta(carta, pos):
    nome = f"{carta.get_ranque()}{carta.icone}"
    tipo = carta.tipo.strip()
    enc = carta.encantamento.strip() if carta.esta_encantada else "Nenhum"
    desc = carta.desc().strip()  # Usa a descrição original do seu código
    
    visual = f"{'✨' if carta.esta_encantada else ' '} {nome}"
    
    html = f"""
    <div class="card-wrapper">
        <div class="card-visual">
            <div style="font-size:1.6rem; font-weight:bold; margin-bottom:4px;">{visual}</div>
            <div style="font-size:0.75rem; color:#888;">Pos: {pos}</div>
        </div>
        <div class="card-popup">
            <div class="popup-title">{nome}</div>
            <div class="popup-stat">{tipo}</div>
            <div class="popup-stat">Encantamento: {enc}</div>
            <div class="popup-desc">{desc}</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def main():
    st.title("🃏 Gerenciador de Baralho JJK")
    st.caption("Conjure técnicas, encante cartas e gerencie sua mão.")

    col_ctrl, col_fei, col_main = st.columns([1, 1, 2])
    
    with col_ctrl:
        if st.button("Comprar", use_container_width=True, type="secondary"):
            st.write("a")

    with col_fei:
        st.write("a")
        
    with col_main:
        if st.session_state.hand.qtd_cartas_na_mão > 0:
            cols = st.columns(min(st.session_state.hand.qtd_cartas_na_mão, 5))
            for i, carta in enumerate(st.session_state.hand.cartas):
                with cols[i]:
                    render_carta(carta, i + 1)

if __name__ == "__main__":
    main()
