from ._base import Pagina


class ReservasPage(Pagina):
    def abrir(self, url_api):
        self.navegador.get(f"{url_api}/web/#reservas")
        self.visivel("reserva-solicitacao")

    def solicitar(self, laboratorio_id, solicitante, data, hora_inicio, hora_fim):
        self.preencher("reserva-laboratorio-id", laboratorio_id)
        self.preencher("reserva-solicitante", solicitante)
        self._preencher_data_ou_hora("reserva-data", data)
        self._preencher_data_ou_hora("reserva-inicio", hora_inicio)
        self._preencher_data_ou_hora("reserva-fim", hora_fim)
        return self.enviar("reserva-solicitar", "reserva-feedback")

    def consultar(self, reserva_id):
        self.preencher("reserva-id", reserva_id)
        return self.enviar("reserva-consultar", "reserva-feedback")

    def cancelar(self, solicitante):
        self.preencher("cancelamento-solicitante", solicitante)
        return self.enviar("reserva-cancelar", "reserva-acao-feedback")

    def resultado(self):
        return self.campos_resultado(
            "reserva-resultado", "id", "laboratorio_id", "solicitante",
            "data", "hora_inicio", "hora_fim", "status",
        )

    def _preencher_data_ou_hora(self, testid, valor):
        campo = self.visivel(testid)
        # Valores ISO nos controles nativos independem do formato regional do Chrome.
        self.navegador.execute_script(
            """
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """,
            campo, valor,
        )
