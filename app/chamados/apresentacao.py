from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for

from app.chamados.aplicacao import AbrirChamadoComando
from app.chamados.dominio import Impacto, RegraNegocioError, Urgencia


chamados_bp = Blueprint("chamados", __name__)


def _usuario_id() -> int:
    return current_app.config["USUARIO_DEMONSTRACAO_ID"]


def _usuario_demo():
    usuario = current_app.extensions["usuario_repository"].buscar_por_id(_usuario_id())
    if usuario is None:
        abort(404)
    return usuario


@chamados_bp.get("/")
def inicio():
    return redirect(url_for("chamados.listar"))


@chamados_bp.get("/chamados")
def listar():
    usuario = _usuario_demo()
    chamados = current_app.extensions[
        "consultar_chamados_service"
    ].listar_do_solicitante(usuario.id)
    return render_template("chamados/lista.html", usuario=usuario, chamados=chamados)


@chamados_bp.route("/chamados/novo", methods=["GET", "POST"])
def novo():
    categoria_repository = current_app.extensions["categoria_repository"]
    categorias = categoria_repository.listar()
    usuario = _usuario_demo()

    if request.method == "POST":
        try:
            categoria_id = int(request.form.get("categoria_id", ""))
            comando = AbrirChamadoComando(
                solicitante_id=usuario.id,
                categoria_id=categoria_id,
                resumo=request.form.get("resumo", ""),
                descricao=request.form.get("descricao", ""),
                impacto=request.form.get("impacto", ""),
                urgencia=request.form.get("urgencia", ""),
            )
            resultado = current_app.extensions["abrir_chamado_service"].executar(comando)
            flash(
                f"Chamado #{resultado.chamado_id} criado com prioridade "
                f"{resultado.prioridade}.",
                "sucesso",
            )
            if resultado.aviso_notificacao:
                flash(resultado.aviso_notificacao, "aviso")
            return redirect(url_for("chamados.detalhar", chamado_id=resultado.chamado_id))
        except (ValueError, RegraNegocioError) as erro:
            flash(str(erro) or "Preencha todos os campos obrigatórios.", "erro")
            return (
                render_template(
                    "chamados/novo.html",
                    usuario=usuario,
                    categorias=categorias,
                    impactos=Impacto,
                    urgencias=Urgencia,
                    dados=request.form,
                ),
                400,
            )

    return render_template(
        "chamados/novo.html",
        usuario=usuario,
        categorias=categorias,
        impactos=Impacto,
        urgencias=Urgencia,
        dados={},
    )


@chamados_bp.get("/chamados/<int:chamado_id>")
def detalhar(chamado_id: int):
    usuario = _usuario_demo()
    chamado = current_app.extensions[
        "consultar_chamados_service"
    ].detalhar_do_solicitante(chamado_id, usuario.id)
    if chamado is None:
        abort(404)
    return render_template("chamados/detalhe.html", usuario=usuario, chamado=chamado)
