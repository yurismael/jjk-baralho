import streamlit as st
import classes_jjk as jjk
import feitiços_encantar as jjkfe
import feitiços_geral as jjkfg
import io
import sys

st.set_page_config(page_title="JJK Baralho", layout="wide", page_icon="🃏")

# 🎨 CSS para Tooltip (Popup no Hover)
st.markdown("""
<style>
.card-wrapper { position: relative; display: inline-flex; flex-direction: column; align-items: center; cursor: pointer; margin: 8px; }
.card-visual { 
    background: linear-gradient(145deg, #2a2a2a, #111); border: 1px solid #555; border-radius: 12px; 
    padding: 14px; width: 130px; text-align: center; transition: all 0.2s ease;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}
.card-wrapper:hover .card-visual { transform: translateY(-5px); border-color: #f1c40f; box-shadow: 0 8px 16px rgba(241,196,15,0.2); }
.card-popup { 
    visibility: hidden; opacity: 0; position: absolute; bottom: 115%; left: 50%; transform: translateX(-50%); 
    width: 260px; background: #0a0a0a; color: #eee; padding: 12px; border-radius: 8px; 
    box-shadow: 0 6px 20px rgba(0,0,0,0.6); border: 1px solid #333; z-index: 1000; 
    transition: opacity 0.3s, visibility 0.3s; text-align: left; font-size: 0.85rem; pointer-events: none;
}
.card-wrapper:hover .card-popup { visibility: visible; opacity: 1; }
.popup-title { font-weight: bold; color: #f1c40f; margin-bottom: 5px; font-size: 1rem; }
.popup-stat { color: #aaa; margin: 3px 0; }
.popup-desc { color: #ccc; margin-top: 6px; line-height: 1.4; border-top: 1px solid #333; padding-top: 6px; }
</style>
""", unsafe_allow_html=True)

# 🔄 Estado Global (Persiste entre reruns)
if "baralho" not in st.session_state:
    st.session_state.baralho = jjk.Baralho()
if "hand" not in st.session_state:
    st.session_state.hand = jjk.Mão()

# 🛠️ Utilitário para capturar prints dos seus arquivos originais
def capturar_saida(func, *args, **kwargs):
    buf = io.StringIO()
    sys.stdout = buf
    try:
        func(*args, **kwargs)
    finally:
        sys.stdout = sys.__stdout__
    return buf.getvalue().strip()

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

    st.markdown(
        """<style>
        div[data-testid="stButton"] > button[kind="secondary"] {
            background: #1a1a1a; border: 1px solid #444; color: #f1c40f; font-weight: 500;
        }
        div[data-testid="stButton"] > button[kind="secondary"]:hover {
            background: #2a2a2a; border-color: #f1c40f; box-shadow: 0 0 12px rgba(241,196,15,0.15);
        }
        </style>""" , unsafe_allow_html=True
    )

# 🖥️ Interface Principal
def main():
    st.title("🃏 Gerenciador de Baralho JJK")
    st.caption("Conjure técnicas, encante cartas e gerencie sua mão.")

    col_ctrl, col_main = st.columns([1, 3])

    # --- CONTROLES (SIDEBAR) ---
    with col_ctrl:
        # COMPRAR
        if st.button("Comprar", use_container_width=True, type="secondary"):
            msg = capturar_saida(jjkfg.Comprar_Carta, st.session_state.baralho, st.session_state.hand, qtd=5)
            if msg: st.warning(msg)
            st.rerun()

        if st.session_state.hand.qtd_cartas_na_mão > 0:
            n = st.session_state.hand.qtd_cartas_na_mão

            # DESCARTE
            if st.button("Descartar", use_container_width=True, type="secondary"):
                if not sel_desc:
                    st.warning("Selecione ao menos uma posição.")
                else:
                    # Descartar_Carta já aceita lista de índices no seu código original
                    msg = capturar_saida(jjkfg.Descartar_Carta, st.session_state.baralho, st.session_state.hand, sel_desc)
                    if msg: st.warning(msg)
                    st.rerun()
            
            cols_desc = st.columns(n)
            sel_desc = []
            for i in range(n):
                if cols_desc[i].checkbox(str(i+1), key=f"desc_{i}_{n}"):
                    sel_desc.append(i+1)

            # DISSIPAR
            if st.button("Dissipar", use_container_width=True, type="secondary"):
                if not sel_disp:
                    st.warning("Selecione ao menos uma posição.")
                else:
                    # Dissipar_Encantamento original recebe 1 pos. Iteramos com segurança:
                    for p in sel_disp:
                        capturar_saida(jjkfg.Dissipar_Encantamento, st.session_state.hand, p)
                    st.success("Encantamentos dissipados!")
                    st.rerun()
            
            cols_disp = st.columns(n)
            sel_disp = []
            for i in range(n):
                # Adiciona ✨ se a carta já estiver encantada para facilitar a visualização
                carta = st.session_state.hand.cartas[i]
                label = f"{i+1} {'✨' if carta.esta_encantada else ''}"
                if cols_disp[i].checkbox(label, key=f"disp_{i}_{n}"):
                    sel_disp.append(i+1)

    # --- ÁREA PRINCIPAL ---
    with col_main:
        st.subheader("👋 Mão Atual")
        if st.session_state.hand.qtd_cartas_na_mão == 0:
            st.info("👐 Mão vazia. Use o menu lateral para comprar cartas.")
        else:
            cols = st.columns(min(st.session_state.hand.qtd_cartas_na_mão, 5))
            for i, carta in enumerate(st.session_state.hand.cartas):
                with cols[i]:
                    render_carta(carta, i + 1)

        st.divider()
        st.subheader("🔮 Conjurar Técnica")
        feitico = st.selectbox("Selecione:", [
            "Encantar Pôquer", "Encantar Blackjack", "Encantar Truco",
            "Encantar Uno", "Encantar Mentira", "Encantar Presidente & Bobo"
        ])

        c1, c2, c3 = st.columns([2, 1, 1])
        nivel = c2.number_input("Nível (1-10)", 1, 10, 1, key="nivel_feat")
        pos = c3.number_input("Posição (1-5)", 1, 5, 1, key="pos_feat")

        if c1.button("✨ Conjurar", type="primary", use_container_width=True):
            msg = ""
            try:
                if feitico == "Encantar Pôquer":
                    msg = capturar_saida(jjkfe.Encantar_Pôquer, st.session_state.hand, int(nivel))
                elif feitico == "Encantar Blackjack":
                    msg = capturar_saida(jjkfe.Encantar_Blackjack, st.session_state.hand, int(nivel))
                elif feitico == "Encantar Truco":
                    msg = capturar_saida(jjkfe.Encantar_Truco, st.session_state.hand, int(nivel))
                elif feitico == "Encantar Uno":
                    msg = capturar_saida(jjkfe.Encantar_Uno, st.session_state.hand)
                elif feitico == "Encantar Mentira":
                    msg = capturar_saida(jjkfe.Encantar_Mentira, st.session_state.hand, int(pos))
                elif feitico == "Encantar Presidente & Bobo":
                    msg = capturar_saida(jjkfe.Encantar_Presidente_Bobo, st.session_state.hand)
            except Exception as e:
                msg = f"⚠️ Erro interno: {e}"

            if msg:
                if any(x in msg.lower() for x in ["inválido", "não pode", "cheia", "vazio", "posição"]):
                    st.error(msg)
                else:
                    st.success(msg)
            st.rerun()

if __name__ == "__main__":
    main()