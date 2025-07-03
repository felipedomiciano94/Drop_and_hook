
# Simulador de Custos - Drop and Hook (D&H)

Este projeto é um painel interativo desenvolvido com **Streamlit**, voltado à simulação de custos logísticos no modelo **Drop and Hook**, permitindo tomada de decisão com base em parâmetros operacionais reais e custos por tipo de transporte.

---

## 📌 Objetivo

Simular os custos logísticos diários e mensais de operações com:
- Frota própria
- SPOT
- Terceiros (agregados ou contratados)

O painel possibilita ajustes dinâmicos de:
- Quantidade de viagens por dia
- Dias úteis no mês
- Custos unitários de cada modalidade
- Premissas operacionais da unidade

---

## 🔧 Funcionalidades

### Aba 1 - **Simulador de Custos**
- Interface interativa para ajustar:
  - Quantidade de viagens por modalidade
  - Dias úteis
  - Custos unitários
- Calcula:
  - Custo diário estimado
  - Custo mensal estimado
  - Totalizadores por modalidade (Frota, SPOT, Terceiro)
- Expansão para visualizar premissas da unidade (tempo de estufagem, docas, turnos, distância, etc.)

### Aba 2 - **Histórico de Atendimentos**
- Exibe tabela com os últimos 5 meses de atendimento real
- Totaliza custos históricos com base nos mesmos custos unitários

---

## 📄 Premissas do Modelo

A unidade operada no projeto é Otacílio Costa. Algumas premissas embutidas:
- CM: 7 cavalos mecânicos
- Motoristas: 9 (dois turnos)
- Tempo médio de estufagem: 3,5h
- Distância por viagem: 103 km ida e volta
- Capacidade D&H estimada: 10 viagens/dia
- Demanda atual: 16,3 viagens/dia

Esses dados são exibidos na interface do painel e podem ser editados diretamente no código.

---

## ▶️ Como Executar

### 1. Instalar dependências:
```bash
pip install streamlit pandas
```

### 2. Rodar a aplicação:
```bash
streamlit run simulador_dh.py
```

---

## 🧠 Casos de Uso
- Planejamento mensal de operação
- Simulação de custos com diferentes composições de frota
- Avaliação do impacto de mudança de modal
- Identifica saving operacional

---

## 📅 Atualização de Custos

Os custos por modalidade (frota, spot, terceiro) são editáveis via **sidebar**. Basta informar os valores mais recentes para realizar a simulação com base em novos cenários.

---

## 📁 Estrutura de Arquivo
- `simulador_dh.py`: script principal
- `README.md`: documentação e orientações

---

## 📢 Contato
**Responsável:** Felipe Domiciano  
**Empresa:** MOVECTA
