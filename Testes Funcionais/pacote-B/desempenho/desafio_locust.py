"""Novo desafio: complete as tarefas e as verificações conforme o roteiro.
Mistura exigida: 70% de listagem e 30% de detalhe em expectativa.
O peso define probabilidade, não uma proporção exata por execução.
"""
from locust import HttpUser, between

class Visitante(HttpUser):
    wait_time = between(0.2, 0.6)
    # TODO: duas tarefas com pesos 7 e 3 e verificações de conteúdo.
