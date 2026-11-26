import json
import uuid
from datetime import datetime
from pathlib import Path
from app.models.reserva import Reserva

DATA_FILE = Path('data/reservas.json')

class ReservaRepository:

    def _load(self) -> list[Reserva]:
        if not DATA_FILE.exists():
            return []
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return [Reserva.from_dict(d) for d in json.load(f)]

    def _save(self, reservas: list[Reserva]):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([r.to_dict() for r in reservas], f,
                      ensure_ascii=False, indent=2)

    def listar(self) -> list[Reserva]:
        return self._load()

    def listar_por_laboratorio(self, lab_id: str) -> list[Reserva]:
        return [r for r in self._load() if r.laboratorio_id == lab_id]

    def buscar_por_id(self, id: str) -> Reserva | None:
        return next((r for r in self._load() if r.id == id), None)

    def salvar(self, reserva: Reserva) -> Reserva:
        reservas = self._load()
        reserva.id = str(uuid.uuid4())
        reserva.data_hora_solicitacao = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        reservas.append(reserva)
        self._save(reservas)
        return reserva

    def atualizar(self, reserva: Reserva) -> Reserva:
        reservas = self._load()
        reservas = [reserva if r.id == reserva.id else r for r in reservas]
        self._save(reservas)
        return reserva