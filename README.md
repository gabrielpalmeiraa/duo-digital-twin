# DUO — Gêmeo Digital para Beneficiamento do Café

**FIAP · Forzy Challenge · Sprint 2**

## Sobre o Projeto
Sistema de gêmeo digital para monitoramento do motor WEG W22 utilizado na linha de beneficiamento de café. Desenvolvido como parte do Forzy Challenge na FIAP.

## Funcionalidades — Sprint 1
- Cadastro técnico de equipamentos com ficha completa
- Consulta e visualização de equipamentos cadastrados
- Conversão de sinais brutos de sensores para unidades de engenharia (V, A, RPM, °C)
- Simulação de leituras dos sensores

## Funcionalidades — Sprint 2
- Navegação por Planta e Área com status visual dos equipamentos
- Dashboard de telemetria em tempo real (Temperatura, Vibração, Corrente)
- Gráficos de séries temporais com histórico de até 7 dias
- Alertas visuais com cores semânticas (verde/amarelo/vermelho)
- Exibição da placa do motor integrada aos dados via visão computacional

## Tecnologias
- Python 3.9
- Streamlit 1.50
- Pandas
- Plotly

## Estrutura do Projeto
duo/
├── app.py
├── pages/
│   ├── 01_consulta.py        # Tela de consulta
│   ├── 02_cadastro.py        # Formulário de cadastro
│   ├── 03_dados_brutos.py    # Visualização de dados brutos
│   ├── 04_plantas.py         # Navegação por planta/área
│   └── 05_dashboard.py       # Dashboard de telemetria
├── services/
│   ├── equipment_service.py  # CRUD de equipamentos
│   ├── data_converter.py     # Conversão de sinais
│   └── data_generator.py     # Gerador de dados históricos
└── data/
    └── equipamentos.json     # Armazenamento local

## Como Rodar
pip3 install streamlit pandas plotly
python3 -m streamlit run app.py