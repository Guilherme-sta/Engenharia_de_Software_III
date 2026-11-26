"""
Sistema-alvo da disciplina Engenharia de Software III - Testes Funcionais.

Dois módulos no mesmo servidor (tudo em memória, sem banco de dados):

  1) "Sabor Express" (lanchonete)  -> usado nos EXEMPLOS da aula e na
     SITUAÇÃO RESOLVIDA pelo professor.
  2) "Matrícula Acadêmica"         -> usado na SITUAÇÃO NOVA que os alunos
     devem resolver.

Como rodar:
    pip install -r requirements.txt
    python app.py              # sobe em http://localhost:5000

Usuários de teste:
    Lanchonete: usuário "aluno"      senha "123456"
    Matrícula : matrícula "20260001" senha "senha123"
                (também existem 20260002 ... 20260200 com a mesma senha)

ATENÇÃO: este sistema tem, de propósito, alguns pontos lentos e regras de
negócio para serem descobertos pelos testes. Não leia o código antes de
testar se quiser fazer o exercício "às cegas".
"""
import itertools
import threading
import time
from functools import wraps

from flask import (Flask, jsonify, redirect, render_template_string, request,
                   session, url_for, abort)

app = Flask(__name__)
app.secret_key = "es3-testes-funcionais"

# ---------------------------------------------------------------------------
# Dados em memória
# ---------------------------------------------------------------------------
CARDAPIO = [
    {"id": 1, "nome": "X-Burger", "preco": 22.90, "categoria": "lanche"},
    {"id": 2, "nome": "X-Salada", "preco": 24.50, "categoria": "lanche"},
    {"id": 3, "nome": "Cuscuz Recheado", "preco": 18.00, "categoria": "lanche"},
    {"id": 4, "nome": "Batata Frita", "preco": 14.00, "categoria": "acompanhamento"},
    {"id": 5, "nome": "Suco de Cajá", "preco": 9.00, "categoria": "bebida"},
    {"id": 6, "nome": "Refrigerante Lata", "preco": 6.50, "categoria": "bebida"},
]
ITENS = {p["id"]: p for p in CARDAPIO}

PEDIDOS = {}
_seq_pedido = itertools.count(1)
_lock_relatorio = threading.Lock()   # gargalo proposital

USUARIOS_LANCHONETE = {"aluno": "123456"}

DISCIPLINAS_BASE = [
    {"codigo": "ES3", "nome": "Engenharia de Software III", "horario": "SEG-19h", "vagas": 40},
    {"codigo": "BD2", "nome": "Banco de Dados II", "horario": "TER-19h", "vagas": 40},
    {"codigo": "PW2", "nome": "Programação Web II", "horario": "QUA-19h", "vagas": 35},
    {"codigo": "RED", "nome": "Redes de Computadores", "horario": "SEG-19h", "vagas": 30},
    {"codigo": "IHC", "nome": "Interação Humano-Computador", "horario": "QUI-19h", "vagas": 30},
    {"codigo": "EMP", "nome": "Empreendedorismo", "horario": "SEX-19h", "vagas": 50},
    {"codigo": "MOB", "nome": "Desenvolvimento Mobile", "horario": "QUA-21h", "vagas": 5},
]
DISCIPLINAS = {}
MATRICULAS = {}
_seq_matricula = itertools.count(1)
_lock_vagas = threading.Lock()
_lock_pdf = threading.Lock()      # gerador de PDF de instância única
ALUNOS = {f"2026{n:04d}": "senha123" for n in range(1, 201)}
MAX_DISCIPLINAS = 5


def reset_matricula():
    DISCIPLINAS.clear()
    for d in DISCIPLINAS_BASE:
        DISCIPLINAS[d["codigo"]] = dict(d)
    MATRICULAS.clear()


reset_matricula()

# ---------------------------------------------------------------------------
# Layout HTML (simples, com ids e data-testid para facilitar os localizadores)
# ---------------------------------------------------------------------------
BASE = """
<!doctype html><html lang="pt-br"><head><meta charset="utf-8">
<title>{{ titulo }}</title>
<style>
 body{font-family:Arial,sans-serif;max-width:820px;margin:24px auto;padding:0 16px;color:#222}
 header{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #ddd;padding-bottom:8px}
 .erro{background:#fde8e8;color:#9b1c1c;padding:10px;border-radius:6px}
 .ok{background:#e6f6ec;color:#14532d;padding:10px;border-radius:6px}
 table{border-collapse:collapse;width:100%} td,th{border-bottom:1px solid #eee;padding:8px;text-align:left}
 button,input[type=submit]{padding:6px 12px;cursor:pointer}
 label{display:block;margin-top:10px}
</style></head><body>
<header><strong>{{ sistema }}</strong><span id="usuario-logado">{{ usuario or "" }}</span></header>
{{ conteudo|safe }}
</body></html>
"""


def pagina(titulo, sistema, conteudo, usuario=None):
    return render_template_string(BASE, titulo=titulo, sistema=sistema,
                                  conteudo=conteudo, usuario=usuario)


@app.get("/")
def index():
    return pagina("Sistemas de Demonstração", "ES3 - Testes Funcionais", """
    <h1>Sistemas de demonstração</h1>
    <ul>
      <li><a id="link-lanchonete" href="/login">Sabor Express (lanchonete)</a></li>
      <li><a id="link-matricula" href="/matricula/login">Matrícula Acadêmica</a></li>
    </ul>""")


@app.get("/health")
def health():
    return jsonify(status="ok")


# ===========================================================================
# MÓDULO 1 - SABOR EXPRESS (web)
# ===========================================================================
def requer_login_lanchonete(f):
    @wraps(f)
    def wrapper(*a, **kw):
        if "usuario" not in session:
            return redirect(url_for("login"))
        return f(*a, **kw)
    return wrapper


@app.route("/login", methods=["GET", "POST"])
def login():
    erro = ""
    if request.method == "POST":
        u = request.form.get("usuario", "").strip()
        s = request.form.get("senha", "")
        if not u or not s:
            erro = "Informe usuário e senha."
        elif USUARIOS_LANCHONETE.get(u) != s:
            erro = "Usuário ou senha inválidos."
        else:
            session.clear()
            session["usuario"] = u
            session["carrinho"] = {}
            return redirect(url_for("cardapio"))
    msg = f'<p class="erro" id="mensagem-erro" data-testid="erro">{erro}</p>' if erro else ""
    return pagina("Login - Sabor Express", "Sabor Express", f"""
    <h1>Entrar</h1>{msg}
    <form method="post" id="form-login">
      <label>Usuário <input id="usuario" name="usuario"></label>
      <label>Senha <input id="senha" name="senha" type="password"></label>
      <p><button id="btn-entrar" type="submit">Entrar</button></p>
    </form>""")


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.get("/cardapio")
@requer_login_lanchonete
def cardapio():
    linhas = "".join(
        f"""<tr data-testid="item-{p['id']}"><td class="nome">{p['nome']}</td>
        <td class="preco">R$ {p['preco']:.2f}</td>
        <td><form method="post" action="/carrinho/adicionar/{p['id']}">
        <button id="add-{p['id']}" type="submit">Adicionar</button></form></td></tr>"""
        for p in CARDAPIO)
    qtd = sum(session.get("carrinho", {}).values())
    return pagina("Cardápio - Sabor Express", "Sabor Express", f"""
    <h1>Cardápio</h1>
    <p><a id="link-carrinho" href="/carrinho">Carrinho (<span id="qtd-carrinho">{qtd}</span>)</a>
       | <a id="link-sair" href="/logout">Sair</a></p>
    <table id="tabela-cardapio"><tr><th>Item</th><th>Preço</th><th></th></tr>{linhas}</table>""",
                  session["usuario"])


@app.post("/carrinho/adicionar/<int:item_id>")
@requer_login_lanchonete
def adicionar(item_id):
    if item_id not in ITENS:
        abort(404)
    carrinho = session.get("carrinho", {})
    carrinho[str(item_id)] = carrinho.get(str(item_id), 0) + 1
    session["carrinho"] = carrinho
    return redirect(url_for("cardapio"))


def _total(carrinho):
    return round(sum(ITENS[int(i)]["preco"] * q for i, q in carrinho.items()), 2)


@app.get("/carrinho")
@requer_login_lanchonete
def ver_carrinho():
    carrinho = session.get("carrinho", {})
    if not carrinho:
        corpo = '<p id="carrinho-vazio">Seu carrinho está vazio.</p>'
    else:
        linhas = "".join(
            f'<tr><td>{ITENS[int(i)]["nome"]}</td><td class="qtd">{q}</td>'
            f'<td>R$ {ITENS[int(i)]["preco"] * q:.2f}</td></tr>'
            for i, q in carrinho.items())
        corpo = f"""<table id="tabela-carrinho"><tr><th>Item</th><th>Qtd</th><th>Subtotal</th></tr>{linhas}</table>
        <p>Total: <strong id="total">R$ {_total(carrinho):.2f}</strong></p>
        <form method="post" action="/pedido/finalizar" id="form-finalizar">
          <label>Endereço de entrega <input id="endereco" name="endereco"></label>
          <label>Pagamento
            <select id="pagamento" name="pagamento">
              <option value="">Selecione...</option><option value="pix">PIX</option>
              <option value="cartao">Cartão</option><option value="dinheiro">Dinheiro</option>
            </select></label>
          <p><button id="btn-finalizar" type="submit">Finalizar pedido</button></p>
        </form>"""
    erro = session.pop("erro_pedido", "")
    msg = f'<p class="erro" id="mensagem-erro" data-testid="erro">{erro}</p>' if erro else ""
    return pagina("Carrinho - Sabor Express", "Sabor Express",
                  f'<h1>Carrinho</h1>{msg}{corpo}<p><a href="/cardapio">Voltar ao cardápio</a></p>',
                  session["usuario"])


@app.post("/pedido/finalizar")
@requer_login_lanchonete
def finalizar():
    carrinho = session.get("carrinho", {})
    endereco = request.form.get("endereco", "").strip()
    pagamento = request.form.get("pagamento", "")
    if not carrinho:
        session["erro_pedido"] = "Carrinho vazio."
    elif len(endereco) < 5:
        session["erro_pedido"] = "Informe um endereço de entrega válido."
    elif pagamento not in ("pix", "cartao", "dinheiro"):
        session["erro_pedido"] = "Selecione a forma de pagamento."
    else:
        pid = _criar_pedido(session["usuario"],
                            [{"id": int(i), "qtd": q} for i, q in carrinho.items()],
                            endereco, pagamento)
        session["carrinho"] = {}
        return redirect(url_for("confirmacao", pid=pid))
    return redirect(url_for("ver_carrinho"))


@app.get("/pedido/<int:pid>")
@requer_login_lanchonete
def confirmacao(pid):
    p = PEDIDOS.get(pid) or abort(404)
    return pagina("Pedido confirmado", "Sabor Express", f"""
    <p class="ok" id="mensagem-sucesso" data-testid="sucesso">Pedido #{pid} confirmado!</p>
    <p>Total: <strong id="total-pedido">R$ {p['total']:.2f}</strong></p>
    <p><a href="/cardapio">Fazer outro pedido</a></p>""", session["usuario"])


# ===========================================================================
# MÓDULO 1 - SABOR EXPRESS (API REST) - alvo dos testes de carga
# ===========================================================================
def _criar_pedido(cliente, itens, endereco, pagamento):
    pid = next(_seq_pedido)
    total = round(sum(ITENS[i["id"]]["preco"] * i["qtd"] for i in itens), 2)
    PEDIDOS[pid] = {"id": pid, "cliente": cliente, "itens": itens,
                    "endereco": endereco, "pagamento": pagamento,
                    "total": total, "status": "recebido"}
    return pid


@app.get("/api/cardapio")
def api_cardapio():
    time.sleep(0.01)  # simula acesso a banco
    return jsonify(CARDAPIO)


@app.post("/api/pedidos")
def api_criar_pedido():
    dados = request.get_json(silent=True) or {}
    itens = dados.get("itens") or []
    if not itens or any(i.get("id") not in ITENS or int(i.get("qtd", 0)) < 1 for i in itens):
        return jsonify(erro="Itens inválidos"), 400
    if not dados.get("cliente"):
        return jsonify(erro="Cliente obrigatório"), 400
    time.sleep(0.03)  # simula gravação
    pid = _criar_pedido(dados["cliente"], itens, dados.get("endereco", "balcão"),
                        dados.get("pagamento", "pix"))
    return jsonify(PEDIDOS[pid]), 201


@app.get("/api/pedidos/<int:pid>")
def api_pedido(pid):
    p = PEDIDOS.get(pid)
    if not p:
        return jsonify(erro="Pedido não encontrado"), 404
    return jsonify(p)


@app.get("/api/relatorio/vendas")
def api_relatorio():
    # GARGALO PROPOSITAL: trava global + custo cresce com o nº de pedidos.
    with _lock_relatorio:
        time.sleep(0.05 + 0.0002 * len(PEDIDOS))
        total = round(sum(p["total"] for p in list(PEDIDOS.values())), 2)
    return jsonify(qtd_pedidos=len(PEDIDOS), faturamento=total)


# ===========================================================================
# MÓDULO 2 - MATRÍCULA ACADÊMICA (situação nova para os alunos)
# ===========================================================================
def _validar_matricula(aluno, codigos):
    """Regras de negócio. Retorna (http_status, mensagem) em caso de erro."""
    if not codigos:
        return 422, "Selecione ao menos uma disciplina."
    if len(codigos) > MAX_DISCIPLINAS:
        return 422, f"Máximo de {MAX_DISCIPLINAS} disciplinas por semestre."
    if any(c not in DISCIPLINAS for c in codigos):
        return 422, "Disciplina inexistente."
    horarios = [DISCIPLINAS[c]["horario"] for c in codigos]
    if len(set(horarios)) != len(horarios):
        return 422, "Choque de horário entre disciplinas selecionadas."
    if any(m["aluno"] == aluno for m in MATRICULAS.values()):
        return 409, "Aluno já possui matrícula neste semestre."
    return None


def _efetivar_matricula(aluno, codigos):
    erro = _validar_matricula(aluno, codigos)
    if erro:
        return erro
    with _lock_vagas:
        esgotadas = [c for c in codigos if DISCIPLINAS[c]["vagas"] <= 0]
        if esgotadas:
            return 409, f"Vagas esgotadas: {', '.join(esgotadas)}."
        for c in codigos:
            DISCIPLINAS[c]["vagas"] -= 1
        mid = next(_seq_matricula)
        MATRICULAS[mid] = {"id": mid, "aluno": aluno, "disciplinas": codigos,
                           "comprovante": f"COMP-{mid:06d}"}
    return 201, MATRICULAS[mid]


@app.route("/matricula/login", methods=["GET", "POST"])
def mat_login():
    erro = ""
    if request.method == "POST":
        m = request.form.get("matricula", "").strip()
        s = request.form.get("senha", "")
        if ALUNOS.get(m) != s:
            erro = "Matrícula ou senha inválidas."
        else:
            session.clear()
            session["aluno"] = m
            return redirect("/matricula/disciplinas")
    msg = f'<p class="erro" id="mensagem-erro">{erro}</p>' if erro else ""
    return pagina("Login - Matrícula", "Matrícula Acadêmica", f"""
    <h1>Portal do Aluno</h1>{msg}
    <form method="post"><label>Matrícula <input id="matricula" name="matricula"></label>
    <label>Senha <input id="senha" name="senha" type="password"></label>
    <p><button id="btn-entrar" type="submit">Entrar</button></p></form>""")


@app.get("/matricula/disciplinas")
def mat_disciplinas():
    if "aluno" not in session:
        return redirect("/matricula/login")
    linhas = "".join(
        f"""<tr data-testid="disc-{d['codigo']}"><td><input type="checkbox" name="disciplinas"
        value="{d['codigo']}" id="chk-{d['codigo']}"></td><td>{d['codigo']}</td><td>{d['nome']}</td>
        <td>{d['horario']}</td><td class="vagas">{d['vagas']}</td></tr>"""
        for d in DISCIPLINAS.values())
    erro = session.pop("erro_mat", "")
    msg = f'<p class="erro" id="mensagem-erro">{erro}</p>' if erro else ""
    return pagina("Disciplinas - Matrícula", "Matrícula Acadêmica", f"""
    <h1>Oferta de disciplinas 2026.2</h1>{msg}
    <form method="post" action="/matricula/confirmar" id="form-matricula">
    <table id="tabela-disciplinas"><tr><th></th><th>Código</th><th>Disciplina</th><th>Horário</th><th>Vagas</th></tr>
    {linhas}</table>
    <p><button id="btn-confirmar" type="submit">Confirmar matrícula</button></p></form>""",
                  session["aluno"])


@app.post("/matricula/confirmar")
def mat_confirmar():
    if "aluno" not in session:
        return redirect("/matricula/login")
    codigos = request.form.getlist("disciplinas")
    status, resp = _efetivar_matricula(session["aluno"], codigos)
    if status != 201:
        session["erro_mat"] = resp
        return redirect("/matricula/disciplinas")
    return pagina("Comprovante", "Matrícula Acadêmica", f"""
    <p class="ok" id="mensagem-sucesso">Matrícula realizada com sucesso!</p>
    <p>Comprovante: <strong id="comprovante">{resp['comprovante']}</strong></p>
    <p>Disciplinas: <span id="disciplinas-matriculadas">{', '.join(resp['disciplinas'])}</span></p>""",
                  session["aluno"])


@app.get("/api/disciplinas")
def api_disciplinas():
    time.sleep(0.02)
    return jsonify(list(DISCIPLINAS.values()))


@app.post("/api/matriculas")
def api_matricular():
    dados = request.get_json(silent=True) or {}
    aluno = dados.get("aluno")
    if aluno not in ALUNOS:
        return jsonify(erro="Aluno inválido"), 401
    time.sleep(0.05)
    status, resp = _efetivar_matricula(aluno, dados.get("disciplinas") or [])
    if status != 201:
        return jsonify(erro=resp), status
    return jsonify(resp), 201


@app.get("/api/matriculas/<int:mid>/comprovante")
def api_comprovante(mid):
    m = MATRICULAS.get(mid)
    if not m:
        return jsonify(erro="Matrícula não encontrada"), 404
    with _lock_pdf:
        time.sleep(0.25)  # simula geração de PDF (ponto lento)
    return jsonify(m)


@app.post("/api/admin/reset")
def api_reset():
    """Restaura vagas e apaga matrículas e pedidos (use antes de cada execução)."""
    reset_matricula()
    PEDIDOS.clear()
    return jsonify(status="resetado")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
