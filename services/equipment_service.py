import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional

DATA_PATH = Path(__file__).parent.parent / "data" / "equipamentos.json"

def _load():
    if not DATA_PATH.exists() or DATA_PATH.stat().st_size == 0:
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def listar_equipamentos():
    return _load()

def buscar_equipamento(eq_id):
    return next((e for e in _load() if e["id"] == eq_id), None)

def cadastrar_equipamento(dados):
    equipamentos = _load()
    novo = {
        "id": str(uuid.uuid4()),
        "criado_em": datetime.now().isoformat(),
        **dados
    }
    equipamentos.append(novo)
    _save(equipamentos)
    return novo

def atualizar_equipamento(eq_id, dados):
    equipamentos = _load()
    for i, e in enumerate(equipamentos):
        if e["id"] == eq_id:
            equipamentos[i] = {**e, **dados}
            _save(equipamentos)
            return equipamentos[i]
    return None