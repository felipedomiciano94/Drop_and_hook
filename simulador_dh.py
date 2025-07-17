
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
        'custo_spot': 2650.0,
        'custo_terceiro': 606.41,
        'viagens_frota': 7,
        'viagens_spot': 2,
        'viagens_terceiro': 6,
        'dias_uteis': 22
    }
    for key, val in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()

st.sidebar.header("💲 Custos por Modalidade")
custo_frota = st.sidebar.number_input("Custo Frota Própria (R$)", min_value=0.0, value=st.session_state.custo_frota, step=50.0)
custo_spot = st.sidebar.number_input("Custo SPOT (R$)", min_value=0.0, value=st.session_state.custo_spot, step=50.0)
custo_terceiro = st.sidebar.number_input("Custo Terceiro (R$)", min_value=0.0, value=st.session_state.custo_terceiro, step=50.0)

aba = st.sidebar.radio("Escolha a aba:", [
    "Simulador de Custos", 
    "Histórico de Atendimentos", 
    "Utilização de Recursos x Custos", 
    "Cálculo de Tempos Úteis"
])

# ABA 1
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

    total_dia = viagens_frota * custo_frota + viagens_spot * custo_spot + viagens_terceiro * custo_terceiro
    total_mes = total_dia * dias_uteis

    st.subheader("💰 Resultado da Simulação")
    st.metric("Custo Diário Estimado", f"R$ {total_dia:,.2f}")
    st.metric(f"Custo Mensal Estimado ({dias_uteis} dias)", f"R$ {total_mes:,.2f}")

    with st.expander("✅ Totalizadores por Modalidade"):
        st.write(f"Custo Frota Própria (R$/dia): R$ {viagens_frota * custo_frota:,.2f}")
        st.write(f"Custo SPOT (R$/dia): R$ {viagens_spot * custo_spot:,.2f}")
        st.write(f"Custo Terceiro (R$/dia): R$ {viagens_terceiro * custo_terceiro:,.2f}")

    st.divider()
    st.caption("Simulação baseada em parâmetros fornecidos manualmente.")

# ABA 2
elif aba == "Histórico de Atendimentos":
    st.title("📊 Histórico de Atendimento Atual")
    dados = {
        "Mês": ["dez/24", "jan/25", "fev/25", "mar/25", "abr/25", "mai/25", "jun/25"],
        "Frota": [40, 50, 90, 101, 128, 107, 57],
        "SPOT": [0, 10, 44, 36, 25, 54, 9],
        "Terceiro": [194, 193, 251, 257, 336, 288, 211],
        "Total": [234, 253, 385, 394, 489, 449, 277]
    }
    df_historico = pd.DataFrame(dados)
    st.write(f"Custo Total Frota: R$ {df_historico['Frota'].sum() * custo_frota:,.2f}")
    st.write(f"Custo Total SPOT: R$ {df_historico['SPOT'].sum() * custo_spot:,.2f}")
    st.write(f"Custo Total Terceiro: R$ {df_historico['Terceiro'].sum() * custo_terceiro:,.2f}")
    st.dataframe(df_historico, use_container_width=True)

# ABA 3
elif aba == "Utilização de Recursos x Custos":
    st.title("📈 Utilização de Recursos x Custos")
    df_historico = pd.DataFrame({
        "Mês": ["dez/24", "jan/25", "fev/25", "mar/25", "abr/25", "mai/25", "jun/25"],
        "Frota": [40, 50, 90, 101, 128, 107, 57],
        "SPOT": [0, 10, 44, 36, 25, 54, 9],
        "Terceiro": [194, 193, 251, 257, 336, 288, 211],
    })
    df_historico["Custo Frota"] = df_historico["Frota"] * custo_frota
    df_historico["Custo SPOT"] = df_historico["SPOT"] * custo_spot
    df_historico["Custo Terceiro"] = df_historico["Terceiro"] * custo_terceiro
    st.subheader("📊 Quantidade de Veículos por Modalidade")
    st.line_chart(df_historico.set_index("Mês")[["Frota", "SPOT", "Terceiro"]])
    st.subheader("💲 Custos por Modalidade")
    st.line_chart(df_historico.set_index("Mês")[["Custo Frota", "Custo SPOT", "Custo Terceiro"]])

# ABA 4
elif aba == "Cálculo de Tempos Úteis":
    st.title("⏱️ Análise de Tempos Úteis x Capacidade Operacional")
    tempo_viagem = {
        "Deslocamento": 2.1,
        "Engate/Desengate": 0.5,
        "Carga/Descarga": 0.5,
        "Almoço + Ociosidade": 1.6
    }
    tempo_total_por_viagem = sum(tempo_viagem.values())
    motoristas = 9
    turnos = 2
    jornada = 4
    tempo_util = motoristas * jornada * turnos
    viagens_dia = tempo_util / tempo_total_por_viagem

    st.metric("⏳ Tempo Útil Diário dos Motoristas", f"{tempo_util:.1f} horas", help="Motoristas × Turnos × Jornada")
    st.metric("🚚 Viagens Possíveis/dia", f"{viagens_dia:.1f}", help="Tempo Útil / Tempo por viagem")
    st.write("### 📌 Tempos Médios por Etapa")
    for k, v in tempo_viagem.items():
        st.write(f"- {k}: {v} horas")
    st.success(f"🧮 Tempo médio total por viagem: {tempo_total_por_viagem:.2f} horas")
    st.divider()

    st.write("### 🔮 Simulação de Cenários Futuros (aumento de motoristas)")
    cenarios = []
    for m in range(9, 16):
        t_util = m * jornada * turnos
        v_dia = t_util / tempo_total_por_viagem
        cenarios.append({"Motoristas": m, "Tempo Útil (h)": t_util, "Viagens Possíveis": round(v_dia, 1)})
    df_cenarios = pd.DataFrame(cenarios)
    st.dataframe(df_cenarios, use_container_width=True)
