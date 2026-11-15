from app.banco import db
from app.catalogo.persistencia import CategoriaModel, EquipeModel, UsuarioModel


def carregar_dados_iniciais():
    if db.session.get(UsuarioModel, 1) is not None:
        return

    usuarios = [
        UsuarioModel(id=1, nome="Ana Solicitante", email="ana@campus.example"),
        UsuarioModel(id=2, nome="Bruno Solicitante", email="bruno@campus.example"),
    ]
    equipes = [
        EquipeModel(id=1, nome="Service Desk"),
        EquipeModel(id=2, nome="Infraestrutura"),
    ]
    categorias = [
        CategoriaModel(id=1, nome="Software", equipe_id=1),
        CategoriaModel(id=2, nome="Rede e conectividade", equipe_id=2),
        CategoriaModel(id=3, nome="Outros - requer triagem", equipe_id=None),
    ]
    db.session.add_all(usuarios + equipes + categorias)
    db.session.commit()

