from fastapi.testclient import TestClient
from app.main import app
import json, os

client = TestClient(app)

def setup_function():
    for f in ['data/laboratorios.json', 'data/reservas.json']:
        with open(f, 'w') as fp:
            json.dump([], fp)

def test_cadastrar_laboratorio_sucesso():
    r = client.post('/laboratorios/', json={'nome': 'Lab A', 'capacidade': 20})
    assert r.status_code == 201
    assert r.json()['nome'] == 'Lab A'
    assert r.json()['status'] == 'ativo'

def test_cadastrar_nome_duplicado():
    client.post('/laboratorios/', json={'nome': 'Lab B', 'capacidade': 10})
    r = client.post('/laboratorios/', json={'nome': 'Lab B', 'capacidade': 15})
    assert r.status_code == 409

def test_listar_laboratorios():
    client.post('/laboratorios/', json={'nome': 'Lab C', 'capacidade': 30})
    r = client.get('/laboratorios/')
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 1

def test_buscar_laboratorio_por_id():
    lab = client.post('/laboratorios/',
                      json={'nome': 'Lab D', 'capacidade': 25}).json()
    r = client.get(f'/laboratorios/{lab["id"]}')
    assert r.status_code == 200
    assert r.json()['id'] == lab['id']

def test_buscar_laboratorio_inexistente():
    r = client.get('/laboratorios/id-inexistente')
    assert r.status_code == 404

def test_atualizar_laboratorio():
    lab = client.post('/laboratorios/',
                      json={'nome': 'Lab E', 'capacidade': 20}).json()
    r = client.put(f'/laboratorios/{lab["id"]}',
                   json={'nome': 'Lab E Atualizado', 'capacidade': 35})
    assert r.status_code == 200
    assert r.json()['nome'] == 'Lab E Atualizado'
    assert r.json()['capacidade'] == 35