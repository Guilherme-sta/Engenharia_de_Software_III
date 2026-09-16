from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def setup_function():
    for f in ['data/laboratorios.json', 'data/reservas.json']:
        with open(f, 'w') as fp:
            json.dump([], fp)

def _criar_lab(nome='Lab Teste', capacidade=20):
    return client.post('/laboratorios/',
                       json={'nome': nome, 'capacidade': capacidade}).json()

def test_solicitar_reserva_sucesso():
    lab = _criar_lab('Lab R1')
    r = client.post('/reservas/', json={
        'laboratorio_id': lab['id'], 'solicitante': 'Guilherme',
        'data': '2027-01-10', 'hora_inicio': '08:00', 'hora_fim': '10:00'
    })
    assert r.status_code == 201
    assert r.json()['status'] == 'pendente'

def test_solicitar_reserva_laboratorio_inexistente():
    r = client.post('/reservas/', json={
        'laboratorio_id': 'id-falso', 'solicitante': 'Guilherme',
        'data': '2027-01-11', 'hora_inicio': '08:00', 'hora_fim': '10:00'
    })
    assert r.status_code == 422

def test_aprovar_reserva():
    lab = _criar_lab('Lab R2')
    reserva = client.post('/reservas/', json={
        'laboratorio_id': lab['id'], 'solicitante': 'Nicolas',
        'data': '2027-01-12', 'hora_inicio': '09:00', 'hora_fim': '11:00'
    }).json()
    r = client.patch(f'/reservas/{reserva["id"]}/avaliar',
                     json={'acao': 'aprovar'})
    assert r.status_code == 200
    assert r.json()['status'] == 'aprovada'

def test_rejeitar_reserva_sem_justificativa():
    lab = _criar_lab('Lab R3')
    reserva = client.post('/reservas/', json={
        'laboratorio_id': lab['id'], 'solicitante': 'Marcos',
        'data': '2027-01-13', 'hora_inicio': '14:00', 'hora_fim': '16:00'
    }).json()
    r = client.patch(f'/reservas/{reserva["id"]}/avaliar',
                     json={'acao': 'rejeitar', 'justificativa': None})
    assert r.status_code == 422

def test_rejeitar_reserva_com_justificativa():
    lab = _criar_lab('Lab R4')
    reserva = client.post('/reservas/', json={
        'laboratorio_id': lab['id'], 'solicitante': 'Marcos',
        'data': '2027-01-14', 'hora_inicio': '14:00', 'hora_fim': '16:00'
    }).json()
    r = client.patch(f'/reservas/{reserva["id"]}/avaliar',
                     json={'acao': 'rejeitar', 'justificativa': 'Manutenção'})
    assert r.status_code == 200
    assert r.json()['status'] == 'rejeitada'

def test_conflito_de_horario():
    lab = _criar_lab('Lab R5')
    r1 = client.post('/reservas/', json={
        'laboratorio_id': lab['id'], 'solicitante': 'Nicolas',
        'data': '2027-01-15', 'hora_inicio': '09:00', 'hora_fim': '11:00'
    }).json()
    client.patch(f'/reservas/{r1["id"]}/avaliar', json={'acao': 'aprovar'})
    r = client.post('/reservas/', json={
        'laboratorio_id': lab['id'], 'solicitante': 'Marcos',
        'data': '2027-01-15', 'hora_inicio': '10:00', 'hora_fim': '12:00'
    })
    assert r.status_code == 422

def test_cancelar_reserva_sucesso():
    lab = _criar_lab('Lab R6')
    reserva = client.post('/reservas/', json={
        'laboratorio_id': lab['id'], 'solicitante': 'Guilherme',
        'data': '2027-01-16', 'hora_inicio': '14:00', 'hora_fim': '16:00'
    }).json()
    r = client.patch(f'/reservas/{reserva["id"]}/cancelar',
                     params={'solicitante': 'Guilherme'})
    assert r.status_code == 200
    assert r.json()['status'] == 'cancelada'
    assert r.json()['data_cancelamento'] is not None

def test_cancelar_reserva_solicitante_errado():
    lab = _criar_lab('Lab R7')
    reserva = client.post('/reservas/', json={
        'laboratorio_id': lab['id'], 'solicitante': 'Guilherme',
        'data': '2027-01-17', 'hora_inicio': '08:00', 'hora_fim': '10:00'
    }).json()
    r = client.patch(f'/reservas/{reserva["id"]}/cancelar',
                     params={'solicitante': 'Intruso'})
    assert r.status_code == 422