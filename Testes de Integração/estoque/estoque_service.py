class EstoqueInsuficienteError(Exception):
    pass


class EstoqueService:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def adicionar_estoque(self, produto_id, quantidade):
        produto = self.repositorio.buscar_por_id(produto_id)
        nova_quantidade = produto.quantidade + quantidade
        self.repositorio.atualizar_quantidade(produto_id, nova_quantidade)

    def vender_produto(self, produto_id, quantidade):
        # Validação adicionada para o desafio extra: o código fornecido aceitava
        # vender 0 (não fazia nada) ou um valor negativo (que AUMENTAVA o estoque).
        if quantidade <= 0:
            raise ValueError(
                f"Quantidade de venda deve ser positiva (recebido: {quantidade})"
            )
        produto = self.repositorio.buscar_por_id(produto_id)
        if quantidade > produto.quantidade:
            raise EstoqueInsuficienteError(
                f"Estoque insuficiente para o produto {produto_id}"
            )
        self.repositorio.atualizar_quantidade(
            produto_id, produto.quantidade - quantidade
        )
