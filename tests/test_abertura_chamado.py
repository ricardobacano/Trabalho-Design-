import pytest

from app.banco import db
from app.chamados.aplicacao import AbrirChamadoComando, AbrirChamadoService
from app.chamados.persistencia import ChamadoModel, EventoHistoricoModel
from app.notificacoes.fake import NotificadorFake


def _dados(categoria_id="1"):
    return {
        "resumo": "Sem acesso ao sistema acadêmico",
        "descricao": "A página apresenta erro ao entrar.",
        "categoria_id": categoria_id,
        "impacto": "ALTO",
        "urgencia": "ALTA",
    }


def test_abertura_persiste_chamado_historico_e_notifica(app, client):
    resposta = client.post("/chamados/novo", data=_dados(), follow_redirects=True)
    assert resposta.status_code == 200
    assert b"Chamado #1" in resposta.data

    with app.app_context():
        chamado = db.session.get(ChamadoModel, 1)
        evento = EventoHistoricoModel.query.one()
        assert chamado.prioridade == "P1_CRITICA"
        assert chamado.estado == "EM_FILA"
        assert chamado.equipe_id == 1
        assert evento.chamado_id == chamado.id
        assert len(app.extensions["notificador"].confirmacoes) == 1


def test_categoria_sem_equipe_encaminha_para_triagem(app, client):
    resposta = client.post("/chamados/novo", data=_dados("3"), follow_redirects=True)
    assert resposta.status_code == 200
    assert b"EM_TRIAGEM" in resposta.data
    assert b"Triagem" in resposta.data

    with app.app_context():
        chamado = ChamadoModel.query.one()
        assert chamado.equipe_id is None
        assert chamado.estado == "EM_TRIAGEM"


def test_resumo_obrigatorio_rejeita_abertura(app, client):
    dados = _dados()
    dados["resumo"] = "  "
    resposta = client.post("/chamados/novo", data=dados)
    assert resposta.status_code == 400
    with app.app_context():
        assert ChamadoModel.query.count() == 0
        assert EventoHistoricoModel.query.count() == 0


def test_falha_ao_gravar_historico_desfaz_todo_o_commit(app, monkeypatch):
    class EventoInvalido:
        def __init__(self, **dados):
            raise RuntimeError("falha simulada no histórico")

    with app.app_context():
        monkeypatch.setattr(
            "app.chamados.persistencia.EventoHistoricoModel", EventoInvalido
        )
        service = app.extensions["abrir_chamado_service"]

        with pytest.raises(RuntimeError, match="falha simulada"):
            service.executar(
                AbrirChamadoComando(
                    solicitante_id=1,
                    categoria_id=1,
                    resumo="Falha transacional",
                    descricao="A gravação do histórico será interrompida.",
                    impacto="BAIXO",
                    urgencia="BAIXA",
                )
            )

        assert ChamadoModel.query.count() == 0
        assert EventoHistoricoModel.query.count() == 0


def test_falha_de_notificacao_nao_desfaz_chamado(app):
    with app.app_context():
        service = AbrirChamadoService(
            usuario_repository=app.extensions["usuario_repository"],
            categoria_repository=app.extensions["categoria_repository"],
            chamado_repository=app.extensions["chamado_repository"],
            notificador=NotificadorFake(falhar=True),
        )
        resultado = service.executar(
            AbrirChamadoComando(
                solicitante_id=1,
                categoria_id=1,
                resumo="Impressora indisponível",
                descricao="A impressora não inicia.",
                impacto="MEDIO",
                urgencia="MEDIA",
            )
        )
        assert resultado.aviso_notificacao is not None
        assert ChamadoModel.query.count() == 1
        assert EventoHistoricoModel.query.count() == 1


def test_consulta_exibe_apenas_chamados_do_usuario_demo(app, client):
    client.post("/chamados/novo", data=_dados())
    with app.app_context():
        original = ChamadoModel.query.one()
        outro = ChamadoModel(
            solicitante_id=2,
            categoria_id=original.categoria_id,
            equipe_id=original.equipe_id,
            resumo="Chamado de outro usuário",
            descricao="Não deve aparecer na consulta da Ana.",
            impacto=original.impacto,
            urgencia=original.urgencia,
            prioridade=original.prioridade,
            estado=original.estado,
            criado_em=original.criado_em,
            prazo_atendimento=original.prazo_atendimento,
        )
        db.session.add(outro)
        db.session.commit()

    resposta = client.get("/chamados")
    assert resposta.status_code == 200
    assert b"Sem acesso ao sistema" in resposta.data
    assert b"Chamado de outro usu" not in resposta.data
