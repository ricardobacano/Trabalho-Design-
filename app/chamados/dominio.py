from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum


class RegraNegocioError(ValueError):
    pass


class Impacto(str, Enum):
    BAIXO = "BAIXO"
    MEDIO = "MEDIO"
    ALTO = "ALTO"


class Urgencia(str, Enum):
    BAIXA = "BAIXA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"


class Prioridade(str, Enum):
    P1_CRITICA = "P1_CRITICA"
    P2_ALTA = "P2_ALTA"
    P3_MEDIA = "P3_MEDIA"
    P4_BAIXA = "P4_BAIXA"


class EstadoChamado(str, Enum):
    EM_FILA = "EM_FILA"
    EM_TRIAGEM = "EM_TRIAGEM"
    EM_ATENDIMENTO = "EM_ATENDIMENTO"
    RESOLVIDO = "RESOLVIDO"
    FECHADO = "FECHADO"


class MatrizPrioridade:
    _matriz = {
        (Impacto.ALTO, Urgencia.ALTA): Prioridade.P1_CRITICA,
        (Impacto.ALTO, Urgencia.MEDIA): Prioridade.P2_ALTA,
        (Impacto.ALTO, Urgencia.BAIXA): Prioridade.P3_MEDIA,
        (Impacto.MEDIO, Urgencia.ALTA): Prioridade.P2_ALTA,
        (Impacto.MEDIO, Urgencia.MEDIA): Prioridade.P3_MEDIA,
        (Impacto.MEDIO, Urgencia.BAIXA): Prioridade.P4_BAIXA,
        (Impacto.BAIXO, Urgencia.ALTA): Prioridade.P3_MEDIA,
        (Impacto.BAIXO, Urgencia.MEDIA): Prioridade.P4_BAIXA,
        (Impacto.BAIXO, Urgencia.BAIXA): Prioridade.P4_BAIXA,
    }

    @classmethod
    def calcular(cls, impacto: Impacto, urgencia: Urgencia) -> Prioridade:
        combinacao = (impacto, urgencia)
        prioridade = cls._matriz[combinacao]
        return prioridade


class PoliticaPrazo:
    _horas_por_prioridade = {
        Prioridade.P1_CRITICA: 4,
        Prioridade.P2_ALTA: 8,
        Prioridade.P3_MEDIA: 48,
        Prioridade.P4_BAIXA: 120,
    }

    @classmethod
    def calcular_prazo(cls, prioridade: Prioridade, criado_em: datetime) -> datetime:
        quantidade_horas = cls._horas_por_prioridade[prioridade]
        prazo = criado_em + timedelta(hours=quantidade_horas)
        return prazo


@dataclass(frozen=True)
class Chamado:
    solicitante_id: int
    categoria_id: int
    equipe_id: int | None
    resumo: str
    descricao: str
    impacto: Impacto
    urgencia: Urgencia
    prioridade: Prioridade
    estado: EstadoChamado
    criado_em: datetime
    prazo_atendimento: datetime

    @classmethod
    def abrir(
        cls,
        solicitante_id: int,
        categoria_id: int,
        equipe_id: int | None,
        resumo: str,
        descricao: str,
        impacto: Impacto,
        urgencia: Urgencia,
        criado_em: datetime | None = None,
    ) -> "Chamado":
        resumo_limpo = resumo.strip()
        descricao_limpa = descricao.strip()
        if not resumo_limpo:
            raise RegraNegocioError("O resumo é obrigatório.")
        else:
            if not descricao_limpa:
                raise RegraNegocioError("A descrição é obrigatória.")

        if criado_em is None:
            instante = datetime.now(timezone.utc)
        else:
            instante = criado_em

        prioridade = MatrizPrioridade.calcular(impacto, urgencia)
        if equipe_id is not None:
            estado = EstadoChamado.EM_FILA
        else:
            estado = EstadoChamado.EM_TRIAGEM

        prazo_atendimento = PoliticaPrazo.calcular_prazo(prioridade, instante)
        chamado = cls(
            solicitante_id=solicitante_id,
            categoria_id=categoria_id,
            equipe_id=equipe_id,
            resumo=resumo_limpo,
            descricao=descricao_limpa,
            impacto=impacto,
            urgencia=urgencia,
            prioridade=prioridade,
            estado=estado,
            criado_em=instante,
            prazo_atendimento=prazo_atendimento,
        )
        return chamado


@dataclass(frozen=True)
class EventoHistorico:
    tipo: str
    descricao: str
    criado_em: datetime

    @classmethod
    def abertura(cls, chamado: Chamado, categoria_nome: str, equipe_nome: str | None):
        if equipe_nome:
            destino = equipe_nome
        else:
            destino = "fila de triagem"
        evento = cls(
            tipo="CHAMADO_ABERTO",
            descricao=(
                f"Chamado aberto na categoria {categoria_nome}; "
                f"prioridade {chamado.prioridade.value}; destino {destino}."
            ),
            criado_em=chamado.criado_em,
        )
        return evento
