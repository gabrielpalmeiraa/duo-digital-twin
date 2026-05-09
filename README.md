# DUO — Gêmeo Digital para Beneficiamento do Café

**FIAP · Forzy Challenge · Sprint 1**

## Sobre o Projeto
Sistema de gêmeo digital para monitoramento do motor WEG W22 utilizado na linha de beneficiamento de café. Desenvolvido como parte do Forzy Challenge na FIAP.

## Funcionalidades — Sprint 1
- Cadastro técnico de equipamentos com ficha completa
- Consulta e visualização de equipamentos cadastrados
- Conversão de sinais brutos de sensores para unidades de engenharia (V, A, RPM, °C)
- Simulação de leituras dos sensores

## Tecnologias
- Python 3.9
- Streamlit 1.50
- Pandas

## Estrutura do Projeto

duo/
├── app.py                    # Entry point
├── pages/
│   ├── 01_consulta.py        # Tela de consulta
│   ├── 02_cadastro.py        # Formulário de cadastro
│   └── 03_dados_brutos.py    # Visualização de dados
├── services/
│   ├── equipment_service.py  # CRUD de equipamentos
│   └── data_converter.py     # Conversão de sinais
└── data/
└── equipamentos.json     # Armazenamento local

## Como Rodar
```bash
pip install streamlit pandas
python3 -m streamlit run app.py
```

## Próximas Sprints
- Integração com sensores reais via ESP32
- Modelo preditivo de anomalias
- Dashboard de monitoramento em tempo real