import streamlit as st
import pandas as pd

# ===============================
# PREMISSAS ESTÁTICAS DO MODELO
# ===============================
premissas_txt = """
PREMISSAS FIXAS - SIMULADOR D&H
--------------------------------------
Unidade: OTACILIO COSTA

Recursos Hoje:
- CM: 7
- Implementos: 7
- Motoristas: 9 (Turno A: 6 | Turno B: 3)

Perfil de Viagem:
- Todos motoristas saem de Lages
- Retornam ao fim do turno com container cheio

CM PÁTIO:
- Tempo médio estufagem (h): 3,5
- Tempo deslocamento interno (h): 2,1
- Motoristas: 1
- Turnos: 2
- Docas: 2
- Estufagens/dia: 6,8

CM DESLOCAMENTO:
- Distância (km ida e volta): 103
- Velocidade média (km/h): 50
- Tempo médio deslocamento: 2,1h
- Engate/Desengate: 0,5h
- Carga/Descarga: 0,5h
- Almoço + diversos: 1,6h (20% ociosidade)
- Motoristas: 2
- Turnos: 2
- Viagens/dia: 8,4

Demanda atual: 16,3 viagens/dia
Capacidade estimada D&H: 10 viagens/dia
Déficit: -6,3 (-39%)
"""

# ===============================
# INTERFACE STREAMLIT
# ===============================
st.set_page_config(page_title="Simulador Drop and Hook", layout="centered")

# --------- ABA 1 ---------
aba = st.sidebar.radio("Escolha a aba:", ["Simulador de Custos", "Histórico de Atendimentos"])

if aba == "Simulador de Custos":
    st.title("🚛 Simulador de Custos - Drop and Hook")

    with st.expander("📌 Premissas do Projeto"):
        st.code(premissas_txt)

    st.header("📥 Insira os custos unitários por viagem")

    col1, col2, col3 = st.columns(3)
    custo_frota = col1.number_input("Custo Frota Própria (R$)", min_value=0.0, value=1100.0, step=50.0)
    custo_spot = col2.number_input("Custo SPOT (R$)", min_value=0.0, value=1300.0, step=50.0)
    custo_terceiro = col3.number_input("Custo Terceiro (R$)", min_value=0.0, value=1500.0, step=50.0)

    st.divider()

    st.subheader("⚙️ Composição de Viagens por Modalidade (dia)")
    viagens_frota = st.number_input("Qtd. Viagens com Frota Própria", min_value=0, value=8)
    viagens_spot = st.number_input("Qtd. Viagens com SPOT", min_value=0, value=2)
    viagens_terceiro = st.number_input("Qtd. Viagens com Terceiro", min_value=0, value=6)

    viagens_total = viagens_frota + viagens_spot + viagens_terceiro

    if viagens_total == 0:
        st.warning("Insira pelo menos uma viagem para simular custos.")
        st.stop()

    # ===============================
    # CÁLCULOS
    # ===============================
    custo_total_dia = (
        viagens_frota * custo_frota +
        viagens_spot * custo_spot +
        viagens_terceiro * custo_terceiro
    )
    custo_total_mes = custo_total_dia * 30  # fixo para efeito de simulação

    # ===============================
    # RESULTADOS
    # ===============================
    st.subheader("💰 Resultado da Simulação")
    st.metric("Custo Diário Estimado", f"R$ {custo_total_dia:,.2f}")
    st.metric("Custo Mensal Estimado (30 dias)", f"R$ {custo_total_mes:,.2f}")

    st.divider()
    st.caption("Simulação baseada em parâmetros fornecidos manualmente. Para uso estratégico e tomada de decisão.")

# --------- ABA 2 ---------
elif aba == "Histórico de Atendimentos":
    st.title("📊 Histórico de Atendimento Atual")

    dados = {
        "Mês": ["dez/24", "jan/25", "fev/25", "mar/25", "abr/25"],
        "Frota": [40, 50, 90, 101, 128],
        "SPOT": [0, 10, 44, 36, 25],
        "Terceiro": [194, 193, 251, 257, 336],
        "Total": [234, 253, 385, 394, 489]
    }
    df_historico = pd.DataFrame(dados)
    st.dataframe(df_historico, use_container_width=True)
    st.caption("Esses dados podem ser atualizados mensalmente conforme evolui o atendimento.")
