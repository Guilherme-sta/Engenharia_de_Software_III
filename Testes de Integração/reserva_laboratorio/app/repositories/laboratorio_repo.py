import json
import uuid
from pathlib import Path
from app.models.laboratorio import Laboratorio

DATA_FILE = Path('data/laboratorios.json')

class LaboratorioRepository:

    def _load(self) -> list[Laboratorio]:
        if not DATA_FILE.exists():
            return []
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return [Laboratorio.from_dict(d) for d in json.load(f)]

    def _save(self, labs: list[Laboratorio]):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([l.to_dict() for l in labs], f, ensure_ascii=False, indent=2)

    def listar(self) -> list[Laboratorio]:
        return self._load()

    def buscar_por_id(self, id: str) -> Laboratorio | None:
        return next((l for l in self._load() if l.id == id), None)

    def buscar_por_nome(self, nome: str) -> Laboratorio | None:
        return next((l for l in self._load()
                     if l.nome.lower() == nome.lower()), None)

    def salvar(self, lab: Laboratorio) -> Laboratorio:
        labs = self._load()
        lab.id = str(uuid.uuid4())
        labs.append(lab)
        self._save(labs)
        return lab

    def atualizar(self, lab: Laboratorio) -> Laboratorio:
        labs = self._load()
        labs = [lab if l.id == lab.id else l for l in labs]
        self._save(labs)
        return lab