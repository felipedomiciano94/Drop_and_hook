
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
st.set_page_config(page_title="Simulador Drop and Hook", layout="wide")

def init_session_state():
    default_values = {
        'custo_frota': 1100.0,
        'custo_spot': 606.41,
        'custo_terceiro': 606.41,
        'viagens_frota': 8,
        'viagens_spot': 2,
        'viagens_terceiro': 6,
        'dias_uteis': 22
    }
    for key, val in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()

# Sidebar
st.sidebar.header("💲 Custos por Modalidade")
custo_frota = st.sidebar.number_input("Custo Frota Própria (R$)", min_value=0.0, value=st.session_state.custo_frota, step=50.0)
custo_spot = st.sidebar.number_input("Custo SPOT (R$)", min_value=0.0, value=st.session_state.custo_spot, step=50.0)
custo_terceiro = st.sidebar.number_input("Custo Terceiro (R$)", min_value=0.0, value=st.session_state.custo_terceiro, step=50.0)

aba = st.sidebar.radio("Escolha a aba:", ["Simulador de Custos", "Histórico de Atendimentos", "Utilização de Recursos x Custos"])

# --------- ABA 1 ---------
if aba == "Simulador de Custos":
    st.title("🚛 Simulador de Custos - Drop and Hook")
    with st.expander("📌 Premissas do Projeto"):
        st.code(premissas_txt)

    st.header("🔧 Composição de Viagens por Modalidade (dia)")
    viagens_frota = st.number_input("Qtd. Viagens com Frota Própria", min_value=0, value=st.session_state.viagens_frota, key="vf")
    viagens_spot = st.number_input("Qtd. Viagens com SPOT", min_value=0, value=st.session_state.viagens_spot, key="vs")
    viagens_terceiro = st.number_input("Qtd. Viagens com Terceiro", min_value=0, value=st.session_state.viagens_terceiro, key="vt")
    dias_uteis = st.number_input("Qtd. Dias Úteis no Mês", min_value=1, max_value=31, value=st.session_state.dias_uteis, key="dias")

    st.session_state.viagens_frota = viagens_frota
    st.session_state.viagens_spot = viagens_spot
    st.session_state.viagens_terceiro = viagens_terceiro
    st.session_state.dias_uteis = dias_uteis
    st.session_state.custo_frota = custo_frota
    st.session_state.custo_spot = custo_spot
    st.session_state.custo_terceiro = custo_terceiro

    viagens_total = viagens_frota + viagens_spot + viagens_terceiro
    if viagens_total == 0:
        st.warning("Insira pelo menos uma viagem para simular custos.")
        st.stop()

    custo_total_frota = viagens_frota * custo_frota
    custo_total_spot = viagens_spot * custo_spot
    custo_total_terceiro = viagens_terceiro * custo_terceiro

    custo_total_dia = custo_total_frota + custo_total_spot + custo_total_terceiro
    custo_total_mes = custo_total_dia * dias_uteis

    st.subheader("💰 Resultado da Simulação")
    st.metric("Custo Diário Estimado", f"R$ {custo_total_dia:,.2f}")
    st.metric(f"Custo Mensal Estimado ({dias_uteis} dias)", f"R$ {custo_total_mes:,.2f}")

    with st.expander("✅ Totalizadores por Modalidade"):
        st.write(f"Custo Frota Própria (R$/dia): R$ {custo_total_frota:,.2f}")
        st.write(f"Custo SPOT (R$/dia): R$ {custo_total_spot:,.2f}")
        st.write(f"Custo Terceiro (R$/dia): R$ {custo_total_terceiro:,.2f}")

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
    st.subheader("🗓️ Custos Totais por Modalidade (base histórica)")
    st.write(f"Custo Total Frota: R$ {df_historico['Frota'].sum() * custo_frota:,.2f}")
    st.write(f"Custo Total SPOT: R$ {df_historico['SPOT'].sum() * custo_spot:,.2f}")
    st.write(f"Custo Total Terceiro: R$ {df_historico['Terceiro'].sum() * custo_terceiro:,.2f}")
    st.dataframe(df_historico, use_container_width=True)
    st.caption("Esses dados podem ser atualizados mensalmente conforme evolui o atendimento.")

# --------- ABA 3 ---------
elif aba == "Utilização de Recursos x Custos":
    st.title("📈 Utilização de Recursos x Custos")

    dados = {
        "Mês": ["dez/24", "jan/25", "fev/25", "mar/25", "abr/25"],
        "Frota": [40, 50, 90, 101, 128],
        "SPOT": [0, 10, 44, 36, 25],
        "Terceiro": [194, 193, 251, 257, 336]
    }
    df_historico = pd.DataFrame(dados)

    st.subheader("🚚 Quantidade de Veículos por Modalidade (mensal)")
    fig1, ax1 = plt.subplots()
    for modalidade in ["Frota", "SPOT", "Terceiro"]:
        ax1.plot(df_historico["Mês"], df_historico[modalidade], marker="o", label=modalidade)
        for i, valor in enumerate(df_historico[modalidade]):
            ax1.text(i, valor + 2, str(valor), ha="center", fontsize=8)
    ax1.set_ylabel("Qtd. Veículos")
    ax1.set_xlabel("Mês")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    st.subheader("💵 Custos por Modalidade (mensal)")
    df_historico["Custo Frota"] = df_historico["Frota"] * custo_frota
    df_historico["Custo SPOT"] = df_historico["SPOT"] * custo_spot
    df_historico["Custo Terceiro"] = df_historico["Terceiro"] * custo_terceiro

    fig2, ax2 = plt.subplots()
    for coluna, label in zip(["Custo Frota", "Custo SPOT", "Custo Terceiro"],
                              ["Frota", "SPOT", "Terceiro"]):
        ax2.plot(df_historico["Mês"], df_historico[coluna], marker="o", label=label)
        for i, valor in enumerate(df_historico[coluna]):
            ax2.text(i, valor, f"R$ {valor:,.2f}", ha="center", fontsize=8)
    ax2.set_ylabel("Custo Total (R$)")
    ax2.set_xlabel("Mês")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)
