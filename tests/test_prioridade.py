from datetime import datetime, timedelta, timezone

import pytest

from app.chamados.dominio import (
    Impacto,
    MatrizPrioridade,
    PoliticaPrazo,
    Prioridade,
    Urgencia,
)


@pytest.mark.parametrize(
    ("impacto", "urgencia", "esperada"),
    [
        (Impacto.ALTO, Urgencia.ALTA, Prioridade.P1_CRITICA),
        (Impacto.ALTO, Urgencia.MEDIA, Prioridade.P2_ALTA),
        (Impacto.ALTO, Urgencia.BAIXA, Prioridade.P3_MEDIA),
        (Impacto.MEDIO, Urgencia.ALTA, Prioridade.P2_ALTA),
        (Impacto.MEDIO, Urgencia.MEDIA, Prioridade.P3_MEDIA),
        (Impacto.MEDIO, Urgencia.BAIXA, Prioridade.P4_BAIXA),
        (Impacto.BAIXO, Urgencia.ALTA, Prioridade.P3_MEDIA),
        (Impacto.BAIXO, Urgencia.MEDIA, Prioridade.P4_BAIXA),
        (Impacto.BAIXO, Urgencia.BAIXA, Prioridade.P4_BAIXA),
    ],
)
def test_matriz_de_prioridade(impacto, urgencia, esperada):
    assert MatrizPrioridade.calcular(impacto, urgencia) == esperada


@pytest.mark.parametrize(
    ("prioridade", "horas"),
    [
        (Prioridade.P1_CRITICA, 4),
        (Prioridade.P2_ALTA, 8),
        (Prioridade.P3_MEDIA, 48),
        (Prioridade.P4_BAIXA, 120),
    ],
)
def test_politica_de_prazo(prioridade, horas):
    criado_em = datetime(2026, 11, 15, 12, tzinfo=timezone.utc)
    assert PoliticaPrazo.calcular_prazo(prioridade, criado_em) == (
        criado_em + timedelta(hours=horas)
    )
