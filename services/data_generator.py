import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

PLANTAS = {
    "Planta Sul — MG": ["Área de Beneficiamento", "Área de Secagem"],
    "Planta Norte — MG": ["Área de Triagem", "Área de Embalagem"],
}

LIMITES = {
    "temperatura": {"alerta": 55.0, "critico": 70.0},
    "vibracao":    {"alerta": 6.0,  "critico": 8.0},
    "corrente":    {"alerta": 20.0, "critico": 25.0},
}

def get_status(valor: float, sensor: str) -> str:
    lim = LIMITES[sensor]
    if valor >= lim["critico"]:
        return "CRÍTICO"
    elif valor >= lim["alerta"]:
        return "ALERTA"
    return "NORMAL"

def get_cor_status(status: str) -> str:
    return {"NORMAL": "#2ecc71", "ALERTA": "#f39c12", "CRÍTICO": "#e74c3c"}[status]

def gerar_historico(tag: str, dias: int = 7) -> pd.DataFrame:
    """Gera série temporal simulada de 'dias' dias com leituras a cada 10 min."""
    random.seed(hash(tag) % 9999)
    now = datetime.now()
    total_leituras = dias * 24 * 6  # 6 leituras por hora
    registros = []
    for i in range(total_leituras):
        ts = now - timedelta(minutes=10 * (total_leituras - i))
        # Simula tendência de degradação nas últimas 8 horas
        fator = 1.0 + (0.25 if i > total_leituras - 48 else 0.0)
        registros.append({
            "timestamp":   ts,
            "temperatura": round(max(20, random.gauss(45, 7) * fator), 1),
            "vibracao":    round(max(0,  random.gauss(3.8, 1.2) * fator), 2),
            "corrente":    round(max(0,  random.gauss(17, 2.5) * fator), 1),
        })
    return pd.DataFrame(registros)

def get_leitura_atual(tag: str) -> dict:
    """Retorna a leitura mais recente (última linha do histórico de 1 dia)."""
    df = gerar_historico(tag, dias=1)
    ultima = df.iloc[-1]
    return {
        "temperatura": ultima["temperatura"],
        "vibracao":    ultima["vibracao"],
        "corrente":    ultima["corrente"],
        "timestamp":   ultima["timestamp"].strftime("%d/%m/%Y %H:%M"),
    }