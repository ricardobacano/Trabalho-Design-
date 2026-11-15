from app.notificacoes.contrato import ConfirmacaoAbertura, Notificador


class NotificadorFake(Notificador):
    def __init__(self, falhar: bool = False):
        self.falhar = falhar
        self.confirmacoes: list[ConfirmacaoAbertura] = []

    def confirmar_abertura(self, confirmacao: ConfirmacaoAbertura) -> None:
        if self.falhar:
            raise RuntimeError("Falha simulada no serviço de notificação")
        self.confirmacoes.append(confirmacao)
