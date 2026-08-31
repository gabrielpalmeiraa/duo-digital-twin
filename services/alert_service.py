"""
Serviço de Alertas e Inteligência Operacional
-----------------------------------------------
Camada responsável por transformar leituras de sensores em:
  - status operacional (NORMAL / ALERTA / CRÍTICO)
  - resumos textuais (stub de NLP)
  - recomendações de apoio à decisão

Esta camada é DESACOPLADA do front-end: as páginas Streamlit apenas
consomem `obter_alertas()`. Quando os modelos reais de ML/NLP estiverem
prontos, basta trocar a implementação interna destas funções (mantendo
a mesma assinatura) sem alterar nenhuma página.
"""

import random
from datetime import datetime
from typing import Optional

from services.data_generator import get_status, get_cor_status, LIMITES

STATUS_ORDEM = {"CRÍTICO": 3, "ALERTA": 2, "NORMAL": 1}

NOME_SENSOR = {
    "temperatura": "temperatura",
    "vibracao": "vibração",
    "corrente": "corrente",
}

# RNG isolado: `data_generator.gerar_historico()` chama `random.seed(hash(tag) % 9999)`
# a cada leitura, o que reseta o gerador GLOBAL do módulo `random` de forma determinística
# (mesma TAG => mesmo seed). Se usássemos `random` diretamente aqui, a "sorte" da anomalia
# ficaria sempre igual para o mesmo equipamento, travando o status. Por isso usamos uma
# instância própria de `random.Random()`, sem depender do estado global.
_rng = random.Random()


def _leitura_base_normal() -> dict:
    """
    Gera uma leitura de baseline dentro da faixa saudável, para servir de ponto
    de partida antes da camada de simulação de anomalia.

    Mantida separada de `data_generator.gerar_historico()` de propósito: aquele
    gerador embute uma tendência de degradação fixa nas últimas horas do
    histórico (para alimentar os gráficos da Sprint 2), o que faria a "leitura
    atual" já nascer sempre em ALERTA. Aqui, no Painel de Alertas, precisamos
    poder demonstrar a transição NORMAL → ALERTA/CRÍTICO, então o baseline é
    gerado de forma independente, sempre dentro da faixa segura.
    """
    return {
        "temperatura": round(_rng.uniform(35.0, 50.0), 1),
        "vibracao": round(_rng.uniform(1.5, 4.5), 2),
        "corrente": round(_rng.uniform(14.0, 18.0), 1),
    }


def _aplicar_anomalia_simulada(leitura: dict, forcar: bool = False) -> dict:
    """
    Camada de SIMULAÇÃO usada apenas para demonstração do painel.
    Representa, de forma simplificada, o resultado que futuramente virá
    do modelo analítico (ML) de detecção de desvios/anomalias.
    Isolada da leitura bruta para permitir substituição pelo modelo real
    sem impactar o front-end.
    """
    leitura = dict(leitura)
    if forcar or _rng.random() < 0.35:
        sensor = _rng.choice(list(LIMITES.keys()))
        lim = LIMITES[sensor]
        leitura[sensor] = round(_rng.uniform(lim["alerta"], lim["critico"] * 1.15), 1)
    return leitura


def _status_geral(leitura: dict) -> tuple[str, str]:
    """Retorna o pior status entre os sensores monitorados e qual sensor o causou."""
    avaliacoes = [(get_status(leitura[s], s), s) for s in LIMITES.keys()]
    avaliacoes.sort(key=lambda x: STATUS_ORDEM[x[0]], reverse=True)
    return avaliacoes[0]


def gerar_resumo_nlp(eq: dict, status: str, sensor: str, leitura: dict) -> str:
    """
    STUB de integração com o módulo de NLP.

    Quando o modelo de NLP estiver disponível, substituir o corpo desta
    função pela chamada real (ex.: request a um endpoint/pipeline), mantendo
    a mesma assinatura de entrada/saída para não impactar o front-end.
    """
    sensor_nome = NOME_SENSOR[sensor]
    valor = leitura[sensor]

    if status == "CRÍTICO":
        return (
            f"O equipamento {eq['tag']} apresenta {sensor_nome} em nível crítico "
            f"({valor}), acima do limite operacional seguro. O padrão de leitura "
            f"sugere degradação acelerada e risco iminente de falha."
        )
    if status == "ALERTA":
        return (
            f"O equipamento {eq['tag']} apresenta desvio no parâmetro de {sensor_nome} "
            f"({valor}), acima da faixa considerada normal. Recomenda-se acompanhamento "
            f"próximo nas próximas leituras."
        )
    return (
        f"O equipamento {eq['tag']} opera dentro da faixa esperada. Nenhum desvio "
        f"relevante foi identificado nos parâmetros monitorados."
    )


def gerar_recomendacao(status: str, sensor: str) -> dict:
    """Gera um card de apoio inicial à decisão para a equipe de manutenção."""
    tipo = {
        "temperatura": "térmica",
        "vibracao": "mecânica (vibração)",
        "corrente": "elétrica (corrente)",
    }[sensor]

    if status == "CRÍTICO":
        return {
            "titulo": "Ação imediata recomendada",
            "texto": f"Programar parada e inspeção {tipo} o quanto antes. Risco de dano ao ativo.",
            "prioridade": "alta",
        }
    if status == "ALERTA":
        return {
            "titulo": "Monitoramento reforçado",
            "texto": f"Agendar inspeção {tipo} preventiva e aumentar a frequência de leituras.",
            "prioridade": "media",
        }
    return {
        "titulo": "Sem ação necessária",
        "texto": "Manter a rotina normal de monitoramento.",
        "prioridade": "baixa",
    }


def avaliar_equipamento(eq: dict, forcar_anomalia: bool = False) -> dict:
    """Avalia um equipamento e monta o pacote completo de alerta."""
    leitura = _leitura_base_normal()
    leitura = _aplicar_anomalia_simulada(leitura, forcar=forcar_anomalia)
    status, sensor = _status_geral(leitura)

    return {
        "equipamento": eq,
        "leitura": leitura,
        "status": status,
        "sensor_critico": sensor,
        "cor": get_cor_status(status),
        "resumo_nlp": gerar_resumo_nlp(eq, status, sensor, leitura),
        "recomendacao": gerar_recomendacao(status, sensor),
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }


def obter_alertas(equipamentos: list, forcar_anomalia_em: Optional[str] = None) -> list:
    """
    Ponto único de consumo do front-end: retorna a lista de alertas de todos
    os equipamentos, ordenada do mais crítico para o mais saudável.
    """
    alertas = [
        avaliar_equipamento(eq, forcar_anomalia=(forcar_anomalia_em == eq["tag"]))
        for eq in equipamentos
    ]
    alertas.sort(key=lambda a: STATUS_ORDEM[a["status"]], reverse=True)
    return alertas
