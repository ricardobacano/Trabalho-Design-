from dataclasses import dataclass

from app.catalogo.persistencia import (
    CategoriaRepositorySQLAlchemy,
    UsuarioRepositorySQLAlchemy,
)
from app.chamados.dominio import (
    Chamado,
    EventoHistorico,
    Impacto,
    RegraNegocioError,
    Urgencia,
)
from app.chamados.persistencia import ChamadoRepositorySQLAlchemy
from app.notificacoes.contrato import ConfirmacaoAbertura, Notificador


@dataclass(frozen=True)
class AbrirChamadoComando:
    solicitante_id: int
    categoria_id: int
    resumo: str
    descricao: str
    impacto: str
    urgencia: str


@dataclass(frozen=True)
class ResultadoAbertura:
    chamado_id: int
    prioridade: str
    estado: str
    aviso_notificacao: str | None = None


class AbrirChamadoService:
    """Controller GRASP do caso de uso de abertura de chamado."""

    def __init__(
        self,
        usuario_repository: UsuarioRepositorySQLAlchemy,
        categoria_repository: CategoriaRepositorySQLAlchemy,
        chamado_repository: ChamadoRepositorySQLAlchemy,
        notificador: Notificador,
    ):
        self.usuario_repository = usuario_repository
        self.categoria_repository = categoria_repository
        self.chamado_repository = chamado_repository
        self.notificador = notificador

    def executar(self, comando: AbrirChamadoComando) -> ResultadoAbertura:
        solicitante = self.usuario_repository.buscar_por_id(comando.solicitante_id)
        if solicitante is None:
            raise RegraNegocioError("O solicitante informado não existe.")
        else:
            categoria = self.categoria_repository.buscar_por_id(comando.categoria_id)

        if categoria is None:
            raise RegraNegocioError("A categoria informada não existe.")
        else:
            try:
                impacto = Impacto(comando.impacto)
                urgencia = Urgencia(comando.urgencia)
            except ValueError as erro:
                raise RegraNegocioError("Impacto ou urgência inválidos.") from erro

        chamado = Chamado.abrir(
            solicitante_id=comando.solicitante_id,
            categoria_id=categoria.id,
            equipe_id=categoria.equipe_id,
            resumo=comando.resumo,
            descricao=comando.descricao,
            impacto=impacto,
            urgencia=urgencia,
        )
        evento = EventoHistorico.abertura(chamado, categoria.nome, categoria.equipe_nome)
        chamado_id = self.chamado_repository.salvar_novo(chamado, evento)

        try:
            confirmacao = ConfirmacaoAbertura(
                chamado_id=chamado_id,
                destinatario=solicitante.email,
                prioridade=chamado.prioridade.value,
            )
            self.notificador.confirmar_abertura(confirmacao)
        except Exception:
            # O chamado já foi persistido; a falha secundária não desfaz a operação.
            aviso = "Chamado criado, mas a confirmação não pôde ser enviada."
        else:
            aviso = None

        resultado = ResultadoAbertura(
            chamado_id=chamado_id,
            prioridade=chamado.prioridade.value,
            estado=chamado.estado.value,
            aviso_notificacao=aviso,
        )
        return resultado


class ConsultarChamadosService:
    """Coordena as consultas permitidas ao solicitante."""

    def __init__(self, chamado_repository: ChamadoRepositorySQLAlchemy):
        self.chamado_repository = chamado_repository

    def listar_do_solicitante(self, solicitante_id: int):
        chamados = self.chamado_repository.listar_por_solicitante(solicitante_id)
        return chamados

    def detalhar_do_solicitante(self, chamado_id: int, solicitante_id: int):
        chamado = self.chamado_repository.buscar_por_id_e_solicitante(
            chamado_id, solicitante_id
        )
        return chamado
