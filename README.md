# DUO — Gêmeo Digital

**FIAP · Forzy Challenge · Sprint 3
**

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

## Funcionalidades — Sprint 3
- Painel de Alertas e Estados como nova tela inicial da aplicação
- Resumos textuais dos alertas (stub de integração com NLP, pronto para plugar o modelo real)
- Cards de recomendação com apoio inicial à decisão para a equipe de manutenção
- Atualização manual (botão) e automática (timer de 15s) do painel
- Simulação de anomalias e notificação de novos alertas (via `st.toast`)
- Histórico de eventos com as últimas mudanças de estado dos equipamentos
- Componentes de UI reutilizáveis para os cards de alerta e histórico

## Tecnologias
- Python 3.9
- Streamlit 1.50
- Pandas
- Plotly

## Estrutura do Projeto
duo/
├── app.py
├── pages/
│   ├── 00_painel_alertas.py  # Painel de Alertas e Estados (tela inicial)
│   ├── 01_consulta.py        # Tela de consulta
│   ├── 02_cadastro.py        # Formulário de cadastro
│   ├── 03_dados_brutos.py    # Visualização de dados brutos
│   ├── 04_plantas.py         # Navegação por planta/área
│   └── 05_dashboard.py       # Dashboard de telemetria
├── components/
│   └── alert_components.py   # Cards reutilizáveis (alerta, recomendação, histórico)
├── services/
│   ├── equipment_service.py  # CRUD de equipamentos
│   ├── data_converter.py     # Conversão de sinais
│   ├── data_generator.py     # Gerador de dados históricos
│   └── alert_service.py      # Camada de alertas: status, stub de NLP e recomendações
└── data/
    └── equipamentos.json     # Armazenamento local

## Como Rodar
pip3 install streamlit pandas plotly
python3 -m streamlit run app.py
