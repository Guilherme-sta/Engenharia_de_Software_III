# Laboratório de Testes de Software ES III

## Preparação
Python 3.11 ou superior. O aplicativo usa apenas a biblioteca padrão.
Os testes podem ser escritos em Python ou Java, independentemente da linguagem do aplicativo.
Em um terminal, na pasta extraída:

```sh
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip freeze > versoes_utilizadas.txt
python app.py
```
Abra http://127.0.0.1:8000. Use um segundo terminal com o mesmo ambiente ativado.
Chrome deve estar instalado para Selenium. Selenium Manager normalmente resolve o driver,
mas o primeiro uso pode exigir internet. Valide a instalação antes da aula.
Para driver local, configure CHROMEDRIVER. Para Chrome fora do caminho padrão, CHROME_BINARY.

## Demonstração de desempenho em Python
```sh
python -m locust -f desempenho/locustfile.py --host http://127.0.0.1:8000
```
Abra http://localhost:8089. Faça uma verificação com 1 usuário antes dos patamares.
Exemplo sem interface, duração total de 90 s, incluindo a rampa de 10 s:
```sh
python -m locust -f desempenho/locustfile.py --host http://127.0.0.1:8000 --headless -u 20 -r 2 -t 90s --stop-timeout 5s --csv carga20_r1 --html carga20_r1.html
```
Plano sugerido: 5 usuários (r=1), 20 (r=2), 50 (r=5), 100 (r=10), depois 20 (r=2)
para recuperação. Cada execução dura 90 s e contém rampa de até 10 s.
Meça patamar após a rampa usando stats_history.csv e informe separadamente o agregado.
Repita cada patamar três vezes. Guarde um prefixo por repetição.
O retorno 503 é deliberado acima da capacidade didática. Uma saída não zero do Locust
por falhas de requisição pode ser evidência do estresse, não erro do script.
Critério didático na carga nominal de 20 usuários: p95 <= 500 ms e falhas <= 1%.
O ambiente influencia os resultados. Não há promessa de um ponto exato de saturação.
Pause se a máquina ficar instável, se falhas > 20% por 10 s ou p95 > 2000 ms por 10 s.
Registre o último patamar concluído. Não é obrigatório fazer o sistema cair.

O servidor limita a 4 operações simultâneas de catálogo/cursos e acrescenta 30 ms
artificiais por chamada. Serve para estudar métricas, não para estimar capacidade real.
Nenhuma estatística de desempenho entregue com o material representa uma execução medida.

## Exemplo funcional resolvido em Python
```sh
python -m pytest funcionais/test_login.py -v --junitxml=resultado_login.xml
```
HEADLESS=1 ativa execução sem janela (Linux/macOS: `HEADLESS=1 python -m pytest ...`).
No PowerShell: `$env:HEADLESS="1"` antes do comando.
Os testes verificam sucesso e rejeição. Falhas de asserção geram screenshot em evidencias.
A tela de login é um simulador didático. O painel não implementa controle de sessão.
Não use esse aplicativo para estudar segurança/autorização.

## Desafios dos alunos
Desempenho: implementar scripts para GET /api/cursos (peso 7) e
GET /api/cursos/1 (peso 3). O material não contém a solução desses testes.
Funcional: testar /inscricoes conforme as regras do roteiro.
O formulário usa validação no servidor e exibe mensagens em #erro ou #sucesso.
Seletores: #nome, #email, #curso, #confirmar, #lista, [data-testid="cancelar-ID"].
Há 3 cursos com 2 vagas cada. Estado em memória é compartilhado.
POST /api/reset restaura as inscrições. Não execute testes de inscrições em paralelo.
Fixtures podem preparar dados por API. Fluxos avaliados devem agir e verificar pela interface.

## Regras do desafio de inscrições
Nome: aparar espaços nas extremidades, tamanho de 3 a 60 caracteres inclusive.
E-mail: aparar espaços e ignorar maiúsculas para duplicidade. Padrão didático:
uma parte antes de @, domínio com ponto e nenhuma ocorrência de espaço.
Curso: um dos IDs 1, 2, 3. Todos os campos são obrigatórios.
Duplicidade: mesmo e-mail normalizado e mesmo curso. O mesmo e-mail pode fazer outro curso.
Cada curso tem 2 vagas. Cancelamento remove a inscrição e libera uma vaga.
Mensagens: Inscrição realizada, Inscrição já existente, Curso sem vagas,
Nome deve ter de 3 a 60 caracteres, E-mail inválido, Curso obrigatório, Inscrição cancelada.

## Volume e extensões opcionais
Reinicie o servidor com DATA_SIZE=100, 10000 ou 100000 para variar o catálogo de livros.
Linux: `DATA_SIZE=10000 python app.py`. PowerShell: `$env:DATA_SIZE="10000"; python app.py`.
O catálogo filtra em memória e devolve apenas os primeiros 20 itens. Não simula um banco
de dados. Volume é a quantidade de dados, diferente do número de usuários.

## Java
Veja java/README.md. Inclui Selenium/JUnit e uma simulação Gatling equivalente para catálogo.

## Referências
https://docs.locust.io/en/stable/writing-a-locustfile.html
https://docs.locust.io/en/stable/running-without-web-ui.html
https://www.selenium.dev/documentation/webdriver/waits/
https://www.selenium.dev/documentation/selenium_manager/
https://docs.gatling.io/concepts/injection/
https://docs.gatling.io/concepts/assertions/
