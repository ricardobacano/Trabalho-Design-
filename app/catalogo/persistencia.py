from dataclasses import dataclass

from app.banco import db


class UsuarioModel(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), nullable=False, unique=True)


class EquipeModel(db.Model):
    __tablename__ = "equipes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False, unique=True)


class CategoriaModel(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False, unique=True)
    equipe_id = db.Column(db.Integer, db.ForeignKey("equipes.id"), nullable=True)
    equipe = db.relationship(EquipeModel)


@dataclass(frozen=True)
class CategoriaEncontrada:
    id: int
    nome: str
    equipe_id: int | None
    equipe_nome: str | None


@dataclass(frozen=True)
class UsuarioEncontrado:
    id: int
    nome: str
    email: str


class UsuarioRepositorySQLAlchemy:
    def buscar_por_id(self, usuario_id: int) -> UsuarioEncontrado | None:
        registro = db.session.get(UsuarioModel, usuario_id)
        if registro is None:
            return None
        else:
            usuario = UsuarioEncontrado(
                id=registro.id,
                nome=registro.nome,
                email=registro.email,
            )
            return usuario


class CategoriaRepositorySQLAlchemy:
    def buscar_por_id(self, categoria_id: int) -> CategoriaEncontrada | None:
        registro = db.session.get(CategoriaModel, categoria_id)
        if registro is None:
            return None
        else:
            if registro.equipe is not None:
                nome_equipe = registro.equipe.nome
            else:
                nome_equipe = None

            categoria = CategoriaEncontrada(
                id=registro.id,
                nome=registro.nome,
                equipe_id=registro.equipe_id,
                equipe_nome=nome_equipe,
            )
            return categoria

    def listar(self) -> list[CategoriaEncontrada]:
        registros = db.session.execute(
            db.select(CategoriaModel).order_by(CategoriaModel.nome)
        ).scalars()
        categorias = []
        for registro in registros:
            if registro.equipe is not None:
                nome_equipe = registro.equipe.nome
            else:
                nome_equipe = None

            categoria = CategoriaEncontrada(
                id=registro.id,
                nome=registro.nome,
                equipe_id=registro.equipe_id,
                equipe_nome=nome_equipe,
            )
            categorias.append(categoria)

        return categorias
