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
    nome = f"{carta.ranque}{carta.icone}"
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

    # 📊 Barra de status
    st.divider()
    col_status1, col_status2, col_status3 = st.columns(3)
    with col_status1:
        st.metric("📚 Cartas no Baralho", st.session_state.baralho.qtd)
    with col_status2:
        st.metric("🎴 Cartas na Mão", st.session_state.hand.qtd)
    with col_status3:
        cartas_encantadas = sum(1 for c in st.session_state.hand.cartas if c.esta_encantada)
        st.metric("✨ Encantadas", cartas_encantadas)
    st.divider()

    col_ctrl, col_fei, col_main = st.columns([1, 1, 2])
    
    # ⚔️ CONTROLES GERAIS (Comprar, Descartar, Dissipar)
    with col_ctrl:
        st.subheader("🎮 Ações")
        
        # ➕ COMPRAR
        if st.button("➕ Comprar (5)", use_container_width=True, type="secondary"):
            msg = capturar_saida(jjkfg.Comprar_Carta, st.session_state.baralho, st.session_state.hand, qtd=5)
            if msg: 
                st.warning(msg) if "vazio" in msg.lower() or "cheia" in msg.lower() else st.info(msg)
            st.rerun()
        
        # ➖ DESCARTAR
        if st.session_state.hand.qtd > 0:
            st.write("**Descartar Cartas:**")
            cartas_opcoes = [f"{i+1}. {c.ranque}{c.icone} {'✨' if c.esta_encantada else ''}" 
                           for i, c in enumerate(st.session_state.hand.cartas)]
            descartes = st.multiselect("Selecione as cartas:", 
                                      range(1, st.session_state.hand.qtd + 1),
                                      format_func=lambda x: cartas_opcoes[x-1],
                                      key="descartes")
            
            if st.button("🗑️ Descartar", use_container_width=True, type="secondary"):
                if descartes:
                    msg = capturar_saida(jjkfg.Descartar_Carta, st.session_state.baralho, 
                                        st.session_state.hand, descartes)
                    if msg:
                        st.info(msg)
                    st.rerun()
                else:
                    st.warning("Selecione pelo menos uma carta!")
        
        # 🌀 DISSIPAR ENCANTAMENTO
        cartas_encantadas = [i+1 for i, c in enumerate(st.session_state.hand.cartas) if c.esta_encantada]
        if cartas_encantadas:
            st.write("**Dissipar Encantamento:**")
            cartas_ench_opcoes = [f"{i}. {st.session_state.hand.cartas[i-1].ranque}{st.session_state.hand.cartas[i-1].icone} ({st.session_state.hand.cartas[i-1].encantamento})" 
                                 for i in cartas_encantadas]
            pos_dissipar = st.selectbox("Escolha a carta:", cartas_encantadas,
                                       format_func=lambda x: cartas_ench_opcoes[cartas_encantadas.index(x)],
                                       key="dissipar")
            
            if st.button("🌀 Dissipar", use_container_width=True, type="secondary"):
                msg = capturar_saida(jjkfg.Dissipar_Encantamento, st.session_state.hand, pos_dissipar)
                if msg:
                    st.info(msg)
                st.rerun()
        
        # 🔄 NOVA PARTIDA
        st.divider()
        if st.button("🔄 Nova Partida", use_container_width=True, type="secondary"):
            st.session_state.baralho = jjk.Baralho()
            st.session_state.hand = jjk.Mão()
            st.rerun()

    # 🔮 FEITIÇOS (Pôquer, Blackjack, Truco)
    with col_fei:
        st.subheader("🔮 Feitiços")
        
        if st.session_state.hand.qtd == 0:
            st.info("💡 Compre cartas para usar feitiços!")
        else:
            # Seletor de nível (compartilhado entre feitiços)
            nivel = st.slider("⚡ Nível:", 1, 10, 1, help="Aumenta o poder do feitiço")
            
            # 🎴 PÔQUER
            if st.button("🎴 Pôquer", use_container_width=True, type="secondary"):
                nivel = 1  # Nível padrão
                msg = capturar_saida(jjkfe.Encantar_Pôquer, st.session_state.hand, nivel)
                if msg:
                    st.success(msg)
                else:
                    st.info("Nenhuma combinação encontrada")
                st.rerun()
            
            # 🎰 BLACKJACK
            if st.button("🎰 Blackjack (21)", use_container_width=True, type="secondary"):
                nivel = 1  # Nível padrão
                msg = capturar_saida(jjkfe.Encantar_Blackjack, st.session_state.hand, nivel)
                if msg:
                    st.success(msg)
                else:
                    st.info("Soma não é 21")
                st.rerun()
            
            # 🃏 TRUCO
            if st.button("🃏 Truco", use_container_width=True, type="secondary"):
                if st.session_state.hand.qtd < 2:
                    st.warning("Precisa de 2+ cartas para Truco!")
                else:
                    nivel = 1  # Nível padrão
                    msg = capturar_saida(jjkfe.Encantar_Truco, st.session_state.hand, nivel)
                    if msg:
                        st.success(msg)
                    else:
                        st.info("Nenhuma manilha encontrada")
                    st.rerun()

    # 🎴 DISPLAY DA MÃO
    with col_main:
        st.subheader("🎴 Sua Mão")
        if st.session_state.hand.qtd > 0:
            cols = st.columns(min(st.session_state.hand.qtd, 5))
            for i, carta in enumerate(st.session_state.hand.cartas):
                with cols[i]:
                    render_carta(carta, i + 1)
        else:
            st.info("Sua mão está vazia. Compre cartas para começar!")

if __name__ == "__main__":
    main()
