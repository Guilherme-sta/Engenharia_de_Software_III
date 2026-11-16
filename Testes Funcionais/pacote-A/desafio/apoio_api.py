"""Preparação de dados pela API (só pré-condições; a ação avaliada é sempre pela tela).

Usa apenas a biblioteca padrão (urllib), para não exigir dependências extras.
"""
import json
import urllib.error
import urllib.request


def _post(url, corpo=None):
    dados = json.dumps(corpo or {}).encode("utf-8")
    req = urllib.request.Request(url, data=dados, method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as erro:  # 4xx/5xx também têm corpo JSON
        return erro.code, json.loads(erro.read() or b"{}")


def _get(url):
    with urllib.request.urlopen(url, timeout=5) as resp:
        return json.loads(resp.read())


def resetar(base_url):
    """POST /api/admin/reset: restaura vagas e apaga matrículas."""
    status, _ = _post(f"{base_url}/api/admin/reset")
    assert status == 200, "Não foi possível zerar o sistema. O app.py está rodando?"


def matricular(base_url, aluno, disciplinas):
    """POST /api/matriculas. Retorna (status_http, corpo)."""
    return _post(f"{base_url}/api/matriculas", {"aluno": aluno, "disciplinas": disciplinas})


def lotar_disciplina(base_url, codigo, primeiro_aluno=101):
    """Ocupa todas as vagas de uma disciplina com alunos 2026xxxx diferentes."""
    vagas = vagas_por_api(base_url)[codigo]
    for n in range(primeiro_aluno, primeiro_aluno + vagas):
        status, corpo = matricular(base_url, f"2026{n:04d}", [codigo])
        assert status == 201, f"Preparação falhou para o aluno {n}: {corpo}"


def vagas_por_api(base_url):
    """GET /api/disciplinas -> {codigo: vagas}."""
    return {d["codigo"]: d["vagas"] for d in _get(f"{base_url}/api/disciplinas")}
