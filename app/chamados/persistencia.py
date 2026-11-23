from dataclasses import dataclass
from datetime import datetime

from app.banco import db
from app.catalogo.persistencia import CategoriaModel, EquipeModel
from app.chamados.dominio import Chamado, EventoHistorico


class ChamadoModel(db.Model):
    __tablename__ = "chamados"

    id = db.Column(db.Integer, primary_key=True)
    solicitante_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    equipe_id = db.Column(db.Integer, db.ForeignKey("equipes.id"), nullable=True)
    resumo = db.Column(db.String(160), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    impacto = db.Column(db.String(16), nullable=False)
    urgencia = db.Column(db.String(16), nullable=False)
    prioridade = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(24), nullable=False)
    criado_em = db.Column(db.DateTime(timezone=True), nullable=False)
    prazo_atendimento = db.Column(db.DateTime(timezone=True), nullable=False)

    categoria = db.relationship(CategoriaModel)
    equipe = db.relationship(EquipeModel)
    historico = db.relationship(
        "EventoHistoricoModel",
        back_populates="chamado",
        cascade="all, delete-orphan",
        order_by="EventoHistoricoModel.criado_em",
    )


class EventoHistoricoModel(db.Model):
    __tablename__ = "eventos_historico"

    id = db.Column(db.Integer, primary_key=True)
    chamado_id = db.Column(db.Integer, db.ForeignKey("chamados.id"), nullable=False)
    tipo = db.Column(db.String(40), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime(timezone=True), nullable=False)

    chamado = db.relationship(ChamadoModel, back_populates="historico")


@dataclass(frozen=True)
class ChamadoResumo:
    id: int
    resumo: str
    categoria: str
    equipe: str
    prioridade: str
    estado: str
    criado_em: datetime
    prazo_atendimento: datetime


@dataclass(frozen=True)
class HistoricoResumo:
    tipo: str
    descricao: str
    criado_em: datetime


@dataclass(frozen=True)
class ChamadoDetalhe(ChamadoResumo):
    descricao: str
    impacto: str
    urgencia: str
    historico: tuple[HistoricoResumo, ...]


def _resumo(registro: ChamadoModel) -> ChamadoResumo:
    if registro.equipe is not None:
        nome_equipe = registro.equipe.nome
    else:
        nome_equipe = "Triagem"

    return ChamadoResumo(
        id=registro.id,
        resumo=registro.resumo,
        categoria=registro.categoria.nome,
        equipe=nome_equipe,
        prioridade=registro.prioridade,
        estado=registro.estado,
        criado_em=registro.criado_em,
        prazo_atendimento=registro.prazo_atendimento,
    )


class ChamadoRepositorySQLAlchemy:
    def salvar_novo(self, chamado: Chamado, evento: EventoHistorico) -> int:
        registro = ChamadoModel(
            solicitante_id=chamado.solicitante_id,
            categoria_id=chamado.categoria_id,
            equipe_id=chamado.equipe_id,
            resumo=chamado.resumo,
            descricao=chamado.descricao,
            impacto=chamado.impacto.value,
            urgencia=chamado.urgencia.value,
            prioridade=chamado.prioridade.value,
            estado=chamado.estado.value,
            criado_em=chamado.criado_em,
            prazo_atendimento=chamado.prazo_atendimento,
        )
        try:
            db.session.add(registro)
            db.session.flush()
            db.session.add(
                EventoHistoricoModel(
                    chamado_id=registro.id,
                    tipo=evento.tipo,
                    descricao=evento.descricao,
                    criado_em=evento.criado_em,
                )
            )
            db.session.commit()
            return registro.id
        except Exception:
            db.session.rollback()
            raise

    def listar_por_solicitante(self, solicitante_id: int) -> list[ChamadoResumo]:
        registros = db.session.execute(
            db.select(ChamadoModel)
            .where(ChamadoModel.solicitante_id == solicitante_id)
            .order_by(ChamadoModel.criado_em.desc())
        ).scalars()
        chamados = []
        for registro in registros:
            resumo = _resumo(registro)
            chamados.append(resumo)

        return chamados

    def buscar_por_id_e_solicitante(
        self, chamado_id: int, solicitante_id: int
    ) -> ChamadoDetalhe | None:
        registro = db.session.execute(
            db.select(ChamadoModel).where(
                ChamadoModel.id == chamado_id,
                ChamadoModel.solicitante_id == solicitante_id,
            )
        ).scalar_one_or_none()
        if registro is None:
            return None
        else:
            resumo = _resumo(registro)

        eventos = []
        for evento in registro.historico:
            resumo_evento = HistoricoResumo(
                tipo=evento.tipo,
                descricao=evento.descricao,
                criado_em=evento.criado_em,
            )
            eventos.append(resumo_evento)

        detalhe = ChamadoDetalhe(
            **resumo.__dict__,
            descricao=registro.descricao,
            impacto=registro.impacto,
            urgencia=registro.urgencia,
            historico=tuple(eventos),
        )
        return detalhe
