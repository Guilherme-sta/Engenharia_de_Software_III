from ._base import Pagina


class LaboratoriosPage(Pagina):
    def abrir(self, url_api):
        self.navegador.get(f"{url_api}/web/#laboratorios")
        self.visivel("laboratorio-cadastro")

    def cadastrar(self, nome, capacidade):
        self.preencher("laboratorio-nome", nome)
        self.preencher("laboratorio-capacidade", capacidade)
        return self.enviar("laboratorio-cadastrar", "laboratorio-feedback")

    def consultar(self, laboratorio_id):
        self.preencher("laboratorio-id", laboratorio_id)
        return self.enviar("laboratorio-consultar", "laboratorio-feedback")

    def resultado(self):
        return self.campos_resultado("laboratorio-resultado", "id", "nome", "capacidade", "status")
