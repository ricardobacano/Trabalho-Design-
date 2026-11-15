from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ConfirmacaoAbertura:
    chamado_id: int
    destinatario: str
    prioridade: str


class Notificador(ABC):
    @abstractmethod
    def confirmar_abertura(self, confirmacao: ConfirmacaoAbertura) -> None:
        """Envia ou registra a confirmação da abertura do chamado."""
