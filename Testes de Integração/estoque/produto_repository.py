from produto import Produto


class ProdutoRepository:
    def __init__(self, conexao):
        self.conexao = conexao

    def salvar(self, produto):
        self.conexao.execute(
            "INSERT INTO produtos (id, nome, quantidade) VALUES (?, ?, ?)",
            (produto.id, produto.nome, produto.quantidade),
        )
        self.conexao.commit()

    def buscar_por_id(self, produto_id):
        cursor = self.conexao.execute(
            "SELECT id, nome, quantidade FROM produtos WHERE id = ?", (produto_id,)
        )
        linha = cursor.fetchone()
        if linha is None:
            return None
        return Produto(*linha)

    def atualizar_quantidade(self, produto_id, nova_quantidade):
        self.conexao.execute(
            "UPDATE produtos SET quantidade = ? WHERE id = ?",
            (nova_quantidade, produto_id),
        )
        self.conexao.commit()
