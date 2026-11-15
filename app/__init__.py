from pathlib import Path

from flask import Flask

from app.banco import db


def create_app(configuracao=None):
    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    app.config.from_mapping(
        SECRET_KEY="desenvolvimento-local",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(app.instance_path) / 'chamados.db'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        USUARIO_DEMONSTRACAO_ID=1,
        CRIAR_BANCO=True,
        CARREGAR_DADOS_INICIAIS=True,
        NOTIFICADOR_FALHAR=False,
    )
    if configuracao:
        app.config.update(configuracao)

    db.init_app(app)

    # Os imports registram os modelos no metadata do SQLAlchemy.
    from app.catalogo.persistencia import (
        CategoriaRepositorySQLAlchemy,
        UsuarioRepositorySQLAlchemy,
    )
    from app.chamados.aplicacao import AbrirChamadoService, ConsultarChamadosService
    from app.chamados.persistencia import ChamadoRepositorySQLAlchemy
    from app.notificacoes.fake import NotificadorFake

    with app.app_context():
        if app.config["CRIAR_BANCO"]:
            db.create_all()
        if app.config["CARREGAR_DADOS_INICIAIS"]:
            from app.dados_iniciais import carregar_dados_iniciais

            carregar_dados_iniciais()

    usuario_repository = UsuarioRepositorySQLAlchemy()
    categoria_repository = CategoriaRepositorySQLAlchemy()
    chamado_repository = ChamadoRepositorySQLAlchemy()
    notificador = NotificadorFake(falhar=app.config["NOTIFICADOR_FALHAR"])
    abrir_chamado_service = AbrirChamadoService(
        usuario_repository=usuario_repository,
        categoria_repository=categoria_repository,
        chamado_repository=chamado_repository,
        notificador=notificador,
    )
    consultar_chamados_service = ConsultarChamadosService(chamado_repository)

    app.extensions["usuario_repository"] = usuario_repository
    app.extensions["categoria_repository"] = categoria_repository
    app.extensions["chamado_repository"] = chamado_repository
    app.extensions["notificador"] = notificador
    app.extensions["abrir_chamado_service"] = abrir_chamado_service
    app.extensions["consultar_chamados_service"] = consultar_chamados_service

    from app.chamados.apresentacao import chamados_bp

    app.register_blueprint(chamados_bp)
    return app

