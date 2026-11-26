from locust import HttpUser, task, between

class Leitor(HttpUser):
    # Modelo fechado: usuários repetem a operação e aguardam entre tarefas.
    wait_time = between(0.2, 0.6)

    @task
    def buscar_livros(self):
        with self.client.get('/api/livros?q=software', name='catalogo',
                             catch_response=True, timeout=5) as r:
            if r.status_code != 200:
                r.failure(f'HTTP {r.status_code}')
                return
            try:
                d = r.json()
                if d['total'] < 1 or not d['itens']:
                    r.failure('Catálogo vazio ou incoerente')
            except (ValueError, KeyError, TypeError):
                r.failure('Resposta inválida')
