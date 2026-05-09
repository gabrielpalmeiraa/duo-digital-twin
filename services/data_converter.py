def raw_to_volts(raw: float, vref: float = 5.0, bits: int = 12) -> float:
    return round(raw * vref / (2**bits - 1), 3)

def raw_to_amperes(raw: float, sensitivity: float = 0.185) -> float:
    vcc = 2.5
    volts = raw_to_volts(raw)
    return round((volts - vcc) / sensitivity, 3)

def raw_to_rpm(pulses: int, ppr: int = 1, interval_s: float = 1.0) -> float:
    return round((pulses / ppr) * (60.0 / interval_s), 1)

def raw_to_temperature(raw: float, vref: float = 5.0, bits: int = 12) -> float:
    volts = raw_to_volts(raw, vref, bits)
    return round(volts * 100, 1)

CONVERSORES = {
    "Tensão (V)":       lambda r: f"{raw_to_volts(r)} V",
    "Corrente (A)":     lambda r: f"{raw_to_amperes(r)} A",
    "Rotação (RPM)":    lambda r: f"{raw_to_rpm(int(r))} RPM",
    "Temperatura (°C)": lambda r: f"{raw_to_temperature(r)} °C",
}