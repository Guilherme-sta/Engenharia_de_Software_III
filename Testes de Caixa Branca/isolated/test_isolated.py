import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from conflito_unit import verificar_conflito, StatusReserva

class R:
    def __init__(self, id, status, data, hi, hf):
        self.id, self.status, self.data, self.hora_inicio, self.hora_fim = id, status, data, hi, hf

def test_ct01():
    assert verificar_conflito([R("R1",StatusReserva.APROVADA,"2026-06-10","08:00","10:00")], None,"2026-06-10","09:00","11:00") is True

def test_ct02():
    assert verificar_conflito([], None,"2026-06-10","09:00","11:00") is False

def test_ct03():
    assert verificar_conflito([R("R1",StatusReserva.APROVADA,"2026-06-10","08:00","10:00")], "R99","2026-06-10","09:00","11:00") is True

def test_ct04():
    assert verificar_conflito([R("R1",StatusReserva.APROVADA,"2026-06-10","08:00","10:00")], "R1","2026-06-10","09:00","11:00") is False

def test_ct05():
    assert verificar_conflito([R("R1",StatusReserva.PENDENTE,"2026-06-10","08:00","10:00")], None,"2026-06-10","09:00","11:00") is False

def test_ct06():
    assert verificar_conflito([R("R1",StatusReserva.APROVADA,"2026-06-11","08:00","10:00")], None,"2026-06-10","09:00","11:00") is False

def test_ct07():
    assert verificar_conflito([R("R1",StatusReserva.APROVADA,"2026-06-10","14:00","16:00")], None,"2026-06-10","10:00","12:00") is False

def test_ct08():
    assert verificar_conflito([R("R1",StatusReserva.APROVADA,"2026-06-10","08:00","10:00")], None,"2026-06-10","10:00","12:00") is False

def test_ct09():
    reservas=[R("R1",StatusReserva.APROVADA,"2026-06-11","08:00","10:00"), R("R2",StatusReserva.APROVADA,"2026-06-10","09:00","11:00")]
    assert verificar_conflito(reservas, None,"2026-06-10","10:00","12:00") is True
