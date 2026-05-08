import streamlit as st
import classes as cl
import feitiços as fe

# ─── Configuração da página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Técnica Amaldiçoada — Baralho",
    page_icon="🃏",
    layout="wide",
)

# ─── CSS global ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Cinzel:wght@400;600&family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap');

/* Reset e base */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d0d12 !important;
    color: #e8dfc8 !important;
}
[data-testid="stSidebar"] { display: none; }
[data-testid="stHeader"] { background: transparent !important; }

/* Tipografia geral */
* { font-family: 'EB Garamond', Georgia, serif; }
h1, h2, h3 { font-family: 'Cinzel Decorative', serif; }

/* Título principal */
.titulo-principal {
    font-family: 'Cinzel Decorative', serif;
    font-size: 2rem;
    font-weight: 700;
    text-align: center;
    color: #c9a84c;
    text-shadow: 0 0 24px #c9a84c88, 0 2px 4px #000;
    letter-spacing: 0.1em;
    margin-bottom: 0.2rem;
}
.subtitulo {
    font-family: 'Cinzel', serif;
    font-size: 0.85rem;
    text-align: center;
    color: #7a6a4a;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}
.divider {
    border: none;
    border-top: 1px solid #2a2420;
    margin: 0.5rem 0 1.2rem 0;
}

/* Seção de feitiços */
.secao-titulo {
    font-family: 'Cinzel', serif;
    font-size: 0.7rem;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #7a6a4a;
    margin-bottom: 0.6rem;
}
.feitico-box {
    background: #13111a;
    border: 1px solid #2c2435;
    border-radius: 6px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.75rem;
}
.feitico-nome {
    font-family: 'Cinzel', serif;
    font-size: 0.95rem;
    color: #c9a84c;
    margin-bottom: 0.3rem;
}
.feitico-desc {
    font-size: 0.82rem;
    color: #9a8e78;
    margin-bottom: 0.7rem;
    font-style: italic;
    line-height: 1.4;
}

/* Cartas */
.carta-grid {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    justify-content: flex-start;
}

.carta {
    width: 110px;
    min-height: 160px;
    border-radius: 10px;
    padding: 10px 8px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    border: 1.5px solid #2a2420;
    background: #161318;
    box-shadow: 0 4px 20px #00000088;
    transition: transform 0.15s, box-shadow 0.15s;
    cursor: default;
}
.carta:hover { transform: translateY(-4px); box-shadow: 0 8px 28px #00000099; }

.carta-espadas { border-color: #3a4a6a; }
.carta-copas   { border-color: #6a2a3a; }
.carta-ouros   { border-color: #6a5a1a; }
.carta-paus    { border-color: #2a5a3a; }

.carta-encantada { box-shadow: 0 0 12px #c9a84c66, 0 4px 20px #00000088 !important; }

.carta-valor-topo {
    font-family: 'Cinzel', serif;
    font-size: 1.1rem;
    font-weight: 600;
    line-height: 1;
}
.carta-icone-centro {
    text-align: center;
    font-size: 2rem;
    line-height: 1;
    opacity: 0.85;
}
.carta-valor-base {
    font-family: 'Cinzel', serif;
    font-size: 1.1rem;
    font-weight: 600;
    text-align: right;
    line-height: 1;
    transform: rotate(180deg);
}

.cor-espadas { color: #7ba3d8; }
.cor-copas   { color: #d87b8a; }
.cor-ouros   { color: #d8b84c; }
.cor-paus    { color: #7bd8a0; }

.carta-tipo {
    font-size: 0.55rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    text-align: center;
    padding: 2px 4px;
    border-radius: 3px;
    margin-top: 4px;
    background: #1e1b2a;
    color: #7a6a4a;
}
.carta-encantamento {
    font-size: 0.5rem;
    letter-spacing: 0.1em;
    text-align: center;
    color: #c9a84c;
    margin-top: 2px;
    font-style: italic;
}
.carta-desc {
    font-size: 0.58rem;
    color: #7a6a4a;
    text-align: center;
    margin-top: 4px;
    line-height: 1.3;
    font-style: italic;
}

/* Info do baralho */
.baralho-info {
    font-family: 'Cinzel', serif;
    font-size: 0.75rem;
    color: #7a6a4a;
    letter-spacing: 0.15em;
    text-align: center;
    padding: 0.5rem;
    border: 1px solid #1e1b1a;
    border-radius: 6px;
    background: #100e14;
    margin-bottom: 1rem;
}

/* Mensagens */
.msg-ok    { color: #7dd89a; font-size: 0.82rem; padding: 0.3rem 0; }
.msg-erro  { color: #d87b7b; font-size: 0.82rem; padding: 0.3rem 0; }
.msg-aviso { color: #d8b84c; font-size: 0.82rem; padding: 0.3rem 0; }

/* Mão vazia */
.mao-vazia {
    color: #3a3430;
    font-style: italic;
    font-size: 0.88rem;
    text-align: center;
    padding: 2rem 0;
}

/* Streamlit overrides */
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label,
div[data-testid="stTextInput"] label {
    font-family: 'EB Garamond', serif !important;
    font-size: 0.82rem !important;
    color: #9a8e78 !important;
}
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background: #13111a !important;
    border: 1px solid #2c2435 !important;
    color: #e8dfc8 !important;
    border-radius: 4px !important;
}
div[data-testid="stSelectbox"] > div,
div[data-testid="stMultiSelect"] > div {
    background: #13111a !important;
    border: 1px solid #2c2435 !important;
    color: #e8dfc8 !important;
    border-radius: 4px !important;
}
button[kind="primary"], button[kind="secondary"] {
    font-family: 'Cinzel', serif !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.1em !important;
    border-radius: 4px !important;
    border: 1px solid #2c2435 !important;
    background: #1a1625 !important;
    color: #c9a84c !important;
    transition: all 0.15s !important;
    padding: 0.3rem 0.7rem !important;
}
button[kind="primary"]:hover, button[kind="secondary"]:hover {
    background: #231e30 !important;
    border-color: #c9a84c !important;
}
.stExpander > details {
    background: #13111a !important;
    border: 1px solid #2c2435 !important;
    border-radius: 6px !important;
}
.stExpander summary {
    font-family: 'Cinzel', serif !important;
    font-size: 0.82rem !important;
    color: #c9a84c !important;
}
.carta-wrapper {
    position: relative;
    display: inline-block;
    width: 110px;
}
.carta {
    cursor: pointer;
}
.carta-tooltip {
    visibility: hidden;
    opacity: 0;
    position: fixed;        /* <-- fixed ao invés de absolute */
    background: #1a1625;
    border: 1px solid #c9a84c55;
    border-radius: 8px;
    padding: 0.7rem 0.9rem;
    width: 160px;
    z-index: 99999;
    transition: opacity 0.2s ease, visibility 0.2s ease;
    pointer-events: none;
    box-shadow: 0 8px 24px #00000099;
}
.carta-wrapper:hover .carta-tooltip {
    visibility: visible;
    opacity: 1;
}
.carta-tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 6px solid transparent;
    border-top-color: #c9a84c55;
}
.carta-wrapper:hover .carta-tooltip {
    visibility: visible;
    opacity: 1;
}

.tooltip-tipo {
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7a6a4a;
    margin-bottom: 0.4rem;
}
.tooltip-encantamento {
    font-size: 0.75rem;
    color: #c9a84c;
    font-style: italic;
    margin-bottom: 0.3rem;
    font-family: 'Cinzel', serif;
}
.tooltip-desc {
    font-size: 0.72rem;
    color: #9a8e78;
    line-height: 1.4;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

# ─── Estado da sessão ─────────────────────────────────────────────────────────
if "baralho" not in st.session_state:
    st.session_state.baralho = cl.Baralho()
if "hand" not in st.session_state:
    st.session_state.hand = cl.Mão()
if "log" not in st.session_state:
    st.session_state.log = []

baralho = st.session_state.baralho
hand    = st.session_state.hand

def log(msg: str, tipo: str = "ok"):
    st.session_state.log.insert(0, (msg, tipo))
    if len(st.session_state.log) > 6:
        st.session_state.log.pop()

# ─── Título ───────────────────────────────────────────────────────────────────
st.markdown('<p class="titulo-principal">⚜ Técnica Amaldiçoada ⚜</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo">Baralho Amaldiçoado Aleatório</p>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─── Layout principal: feitiços | cartas ─────────────────────────────────────
col_feiticos, col_cartas = st.columns([1.05, 1.95], gap="large")

# ═══════════════════════════════════════════════════════════════════════════════
# COLUNA ESQUERDA — Feitiços
# ═══════════════════════════════════════════════════════════════════════════════
with col_feiticos:
    st.markdown('<p class="secao-titulo">⚒ Ações do Baralho</p>', unsafe_allow_html=True)

    # — Comprar Carta ──────────────────────────────────────────────────────────
    with st.expander("Comprar Carta", expanded=True):
        qtd_compra = st.number_input("Quantidade", min_value=1, max_value=5, value=1, key="qtd_compra")
        if st.button("Comprar", key="btn_comprar"):
            espacos = 5 - hand.qtd
            if espacos == 0:
                log("A mão está cheia.", "erro")
            elif baralho.qtd == 0:
                log("O baralho está vazio.", "erro")
            else:
                n = min(int(qtd_compra), espacos, baralho.qtd)
                fe.Comprar_Carta(baralho, hand, n)
                log(f"{n} carta(s) comprada(s).", "ok")

    # — Descartar Carta ────────────────────────────────────────────────────────
    with st.expander("Descartar Carta"):
        if hand.qtd == 0:
            st.markdown('<p class="mao-vazia">Nenhuma carta na mão.</p>', unsafe_allow_html=True)
        else:
            opcoes = [f"{i+1}. {c.ranque}{c.icone}" for i, c in enumerate(hand.cartas)]
            sel_descartar = st.multiselect("Selecione as cartas", opcoes, key="sel_descartar")
            if st.button("Descartar", key="btn_descartar"):
                if not sel_descartar:
                    log("Nenhuma carta selecionada.", "aviso")
                else:
                    indices = sorted([opcoes.index(s) + 1 for s in sel_descartar], reverse=True)
                    fe.Descartar_Carta(baralho, hand, indices)
                    log(f"{len(indices)} carta(s) descartada(s).", "ok")

    # — Reiniciar Baralho ──────────────────────────────────────────────────────
    with st.expander("Reiniciar Baralho"):
        st.markdown('<p class="feitico-desc">Volta o baralho ao estado inicial (52 cartas), descartando a mão.</p>', unsafe_allow_html=True)
        if st.button("Reiniciar", key="btn_reiniciar"):
            st.session_state.baralho = cl.Baralho()
            st.session_state.hand    = cl.Mão()
            baralho = st.session_state.baralho
            hand    = st.session_state.hand
            log("Baralho reiniciado.", "ok")
            st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<p class="secao-titulo">✦ Feitiços</p>', unsafe_allow_html=True)

    # — Feitiço: Dissipar Encantamento ────────────────────────────────────────
    with st.expander("Dissipar Encantamento"):
        st.markdown('<p class="feitico-desc">Remove o encantamento de uma carta.</p>', unsafe_allow_html=True)
        if hand.qtd == 0:
            st.markdown('<p class="mao-vazia">Nenhuma carta na mão.</p>', unsafe_allow_html=True)
        else:
            opcoes_e = [f"{i+1}. {c.ranque}{c.icone}" for i, c in enumerate(hand.cartas)]
            sel_dissipar = st.selectbox("Carta", opcoes_e, key="sel_dissipar")
            if st.button("Dissipar", key="btn_dissipar"):
                pos = opcoes_e.index(sel_dissipar) + 1
                carta = hand.get_carta(pos)
                if not carta.esta_encantada:
                    log(f"{carta.ranque}{carta.icone} não está encantada.", "aviso")
                else:
                    fe.Dissipar_Encantamento(hand, pos)
                    log(f"Encantamento dissipado de {carta.ranque}{carta.icone}.", "ok")

    # — Feitiço: Pôquer ────────────────────────────────────────────────────────
    with st.expander("Encantar Pôquer"):
        st.markdown('<p class="feitico-desc">Encanta cartas da mão (necessita 5 cartas) baseado na melhor mão de pôquer formada. Requer nível do feitiço.</p>', unsafe_allow_html=True)
        nivel_poquer = st.number_input("Nível do feitiço", min_value=1, max_value=10, value=1, key="nivel_poquer")
        if st.button("Encantar Pôquer", key="btn_poquer"):
            if hand.qtd != 5:
                log("Pôquer requer exatamente 5 cartas na mão.", "erro")
            else:
                encantamento = fe.encontrar_poker(hand)
                fe.Encantar_Pôquer(hand, int(nivel_poquer))
                log(f"Pôquer encantado: {encantamento}.", "ok")

    # — Feitiço: Blackjack ─────────────────────────────────────────────────────
    with st.expander("Encantar Blackjack"):
        st.markdown('<p class="feitico-desc">Encanta toda a mão se a soma dos valores das cartas for 21 (regras de Blackjack). Requer nível do feitiço.</p>', unsafe_allow_html=True)
        nivel_blackjack = st.number_input("Nível do feitiço", min_value=1, max_value=10, value=1, key="nivel_bj")
        if st.button("Encantar Blackjack", key="btn_bj"):
            if hand.qtd < 1:
                log("Blackjack requer ao menos 1 carta na mão.", "erro")
            else:
                resultado = fe.contar_21(hand)
                if resultado != "Blackjack":
                    soma = sum(
                        11 if c.valor == 1 else (10 if c.valor >= 10 else c.valor)
                        for c in hand.cartas
                    )
                    log(f"Soma atual: {soma}. Precisa ser 21 para Blackjack.", "aviso")
                else:
                    fe.Encantar_Blackjack(hand, int(nivel_blackjack))
                    log("Blackjack encantado!", "ok")

    # — Feitiço: Truco ─────────────────────────────────────────────────────────
    with st.expander("Encantar Truco"):
        st.markdown('<p class="feitico-desc">A última carta da mão é a "vira". Cartas com valor de manilha são encantadas. O bônus varia pelo naipe (Paus > Copas > Espadas > Ouros).</p>', unsafe_allow_html=True)
        nivel_truco = st.number_input("Nível do feitiço", min_value=1, max_value=10, value=1, key="nivel_truco")
        if st.button("Encantar Truco", key="btn_truco"):
            if hand.qtd < 2:
                log("Truco requer ao menos 2 cartas na mão.", "erro")
            else:
                resultado = fe.manilha_vira(hand)
                if resultado != "Truco":
                    log("Nenhuma manilha encontrada na mão.", "aviso")
                else:
                    fe.Encantar_Truco(hand, int(nivel_truco))
                    log("Truco encantado!", "ok")

    # — Feitiço: Uno ───────────────────────────────────────────────────────────
    with st.expander("Encantar Uno"):
        st.markdown('<p class="feitico-desc">A mão deve ter apenas uma carta. Encanta essa carta com o efeito Uno.</p>', unsafe_allow_html=True)
        if st.button("Encantar Uno", key="btn_uno"):
            if hand.qtd != 1:
                log("Uno requer exatamente 1 carta na mão.", "erro")
            else:
                fe.Encantar_Uno(hand)
                log("Uno encantado!", "ok")

    # — Feitiço: Mentira ───────────────────────────────────────────────────────
    with st.expander("Encantar Mentira"):
        st.markdown('<p class="feitico-desc">Encanta uma carta escolhida com o efeito Mentira.</p>', unsafe_allow_html=True)
        if hand.qtd == 0:
            st.markdown('<p class="mao-vazia">Nenhuma carta na mão.</p>', unsafe_allow_html=True)
        else:
            opcoes_m = [f"{i+1}. {c.ranque}{c.icone}" for i, c in enumerate(hand.cartas)]
            sel_mentira = st.selectbox("Carta", opcoes_m, key="sel_mentira")
            if st.button("Encantar Mentira", key="btn_mentira"):
                pos = opcoes_m.index(sel_mentira) + 1
                fe.Encantar_Mentira(hand, pos)
                log("Mentira encantada!", "ok")

    # — Feitiço: Presidente & Bobo ─────────────────────────────────────────────
    with st.expander("Encantar Presidente & Bobo"):
        st.markdown('<p class="feitico-desc">A mão deve ter exatamente 2 cartas. A 1ª recebe "Presidente" e a 2ª recebe "Bobo".</p>', unsafe_allow_html=True)
        if st.button("Encantar P&B", key="btn_pb"):
            if hand.qtd != 2:
                log("Presidente & Bobo requer exatamente 2 cartas na mão.", "erro")
            else:
                fe.Encantar_Presidente_Bobo(hand)
                log("Presidente & Bobo encantados!", "ok")

    # — Log de ações ───────────────────────────────────────────────────────────
    if st.session_state.log:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<p class="secao-titulo">◈ Log</p>', unsafe_allow_html=True)
        for msg, tipo in st.session_state.log:
            st.markdown(f'<p class="msg-{tipo}">› {msg}</p>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# COLUNA DIREITA — Cartas
# ═══════════════════════════════════════════════════════════════════════════════
with col_cartas:
    # Info do baralho
    st.markdown(
        f'<div class="baralho-info">🂠 Cartas no baralho: <strong>{baralho.qtd}</strong> &nbsp;|&nbsp; ✋ Cartas na mão: <strong>{hand.qtd}</strong> / 5</div>',
        unsafe_allow_html=True
    )

    st.markdown('<p class="secao-titulo">✦ Mão Atual</p>', unsafe_allow_html=True)

    if hand.qtd == 0:
        st.markdown('<p class="mao-vazia">A mão está vazia. Compre cartas para começar.</p>', unsafe_allow_html=True)
    else:
        # Renderizar cartas horizontalmente usando colunas
        cols = st.columns(min(hand.qtd, 5))
        for idx, carta in enumerate(hand.cartas):
            naipe_cls = {
                "espadas": "carta-espadas cor-espadas",
                "copas":   "carta-copas   cor-copas",
                "ouros":   "carta-ouros   cor-ouros",
                "paus":    "carta-paus    cor-paus",
            }.get(carta.naipe, "")

            cor_cls = {
                "espadas": "cor-espadas",
                "copas":   "cor-copas",
                "ouros":   "cor-ouros",
                "paus":    "cor-paus",
            }.get(carta.naipe, "")

            encantada_cls = "carta-encantada" if carta.esta_encantada else ""

            desc_txt = (carta.desc() or "") if hasattr(carta, "desc") else ""

            enc_html = ""
            if carta.esta_encantada:
                enc_html = f'<div class="carta-encantamento">{carta.encantamento}</div>'

            with cols[idx]:
                st.markdown(f"""
                <div class="carta-wrapper">
                    <div class="carta {naipe_cls} {encantada_cls}">
                        <div class="{cor_cls}" style="display:flex; justify-content:space-between; align-items:flex-start;">
                            <span class="carta-valor-topo">{carta.ranque}</span>
                            <span style="font-size:0.9rem">{carta.icone}</span>
                        </div>
                        <div class="carta-icone-centro {cor_cls}">{carta.icone}</div>
                        <div class="{cor_cls}" style="display:flex; justify-content:space-between; align-items:flex-end;">
                            <span style="font-size:0.9rem; transform:rotate(180deg); display:inline-block">{carta.icone}</span>
                            <span class="carta-valor-base">{carta.ranque}</span>
                        </div>
                    </div>

                    <div class="carta-tooltip">
                        <div class="tooltip-tipo">{carta.tipo}</div>
                        {f'<div class="tooltip-encantamento">✦ {carta.encantamento}</div>' if carta.esta_encantada else ''}
                        {f'<div class="tooltip-desc">{desc_txt}</div>' if desc_txt else ''}
                    </div>
                </div>
                <div style="text-align:center; margin-top:0.3rem; font-family:'Cinzel',serif; font-size:0.65rem; color:#4a3f30">#{idx+1}</div>
                """, unsafe_allow_html=True)
            st.markdown("""<script>
                document.querySelectorAll('.carta-wrapper').forEach(wrapper => {
                    const tooltip = wrapper.querySelector('.carta-tooltip');
                    if (!tooltip) return;

                    wrapper.addEventListener('mouseenter', e => {
                        const rect = wrapper.getBoundingClientRect();
                        tooltip.style.left = (rect.left + rect.width / 2 - 80) + 'px';
                        tooltip.style.top  = (rect.top - tooltip.offsetHeight - 12) + 'px';
                    });

                    // Ajusta se sair da tela pelo topo
                    wrapper.addEventListener('mouseenter', () => {
                        requestAnimationFrame(() => {
                            const rect    = wrapper.getBoundingClientRect();
                            const ttRect  = tooltip.getBoundingClientRect();
                            if (ttRect.top < 8) {
                                tooltip.style.top = (rect.bottom + 12) + 'px';
                            }
                        });
                    });
                });
                </script>""", unsafe_allow_html=True)

    # — Blackjack soma ─────────────────────────────────────────────────────────
    if hand.qtd > 0:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<p class="secao-titulo">◈ Referências</p>', unsafe_allow_html=True)

        def bj_val(v):
            return 11 if v == 1 else (10 if v >= 10 else v)

        soma_bj = sum(bj_val(c.valor) for c in hand.cartas)
        cor_soma = "#7dd89a" if soma_bj == 21 else ("#d8b84c" if soma_bj < 21 else "#d87b7b")

        st.markdown(f"""
        <div style="display:flex; gap:1.5rem; flex-wrap:wrap;">
            <div style="background:#13111a; border:1px solid #2c2435; border-radius:6px; padding:0.7rem 1.1rem;">
                <div class="secao-titulo" style="margin-bottom:0.3rem">Soma Blackjack</div>
                <div style="font-family:'Cinzel',serif; font-size:1.4rem; color:{cor_soma}">{soma_bj}</div>
                <div style="font-size:0.7rem; color:#5a5040; margin-top:2px">{'✦ Blackjack!' if soma_bj == 21 else ('Abaixo de 21' if soma_bj < 21 else 'Acima de 21')}</div>
            </div>
            <div style="background:#13111a; border:1px solid #2c2435; border-radius:6px; padding:0.7rem 1.1rem;">
                <div class="secao-titulo" style="margin-bottom:0.3rem">Cartas Encantadas</div>
                <div style="font-family:'Cinzel',serif; font-size:1.4rem; color:#c9a84c">{sum(1 for c in hand.cartas if c.esta_encantada)}</div>
                <div style="font-size:0.7rem; color:#5a5040; margin-top:2px">de {hand.qtd} na mão</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Tabela de mãos de pôquer se tiver 5 cartas
        if hand.qtd == 5:
            encantamento_poquer = fe.encontrar_poker(hand)
            nivel_mãos = [
                "Carta Alta", "Par", "Trinca", "Dois Pares",
                "Straight", "Flush", "Full House", "Quadra",
                "Straight Flush", "Royal Flush"
            ]
            idx_mao = nivel_mãos.index(encantamento_poquer) if encantamento_poquer in nivel_mãos else -1
            st.markdown(f"""
            <div style="background:#13111a; border:1px solid #2c2435; border-radius:6px; padding:0.7rem 1.1rem; margin-top:0.75rem">
                <div class="secao-titulo" style="margin-bottom:0.5rem">Mão de Pôquer Detectada</div>
                <div style="font-family:'Cinzel',serif; font-size:1.1rem; color:#c9a84c">{encantamento_poquer or '—'}</div>
                {'<div style="font-size:0.7rem; color:#5a5040; margin-top:2px">Nível ' + str(idx_mao) + ' de 9</div>' if idx_mao >= 0 else ''}
            </div>
            """, unsafe_allow_html=True)