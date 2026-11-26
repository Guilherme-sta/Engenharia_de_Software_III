import json
from urllib.error import URLError
from urllib.request import Request, urlopen


def post(base_url, caminho, status_esperado, dados=None):
    requisicao = Request(
        f"{base_url}{caminho}",
        data=json.dumps(dados or {}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(requisicao, timeout=5) as resposta:
            assert resposta.status == status_esperado, (
                f"POST {caminho}: esperado HTTP {status_esperado}, recebido {resposta.status}"
            )
    except URLError as erro:
        raise AssertionError(f"Falha no preparo: POST {caminho}: {erro}") from erro
