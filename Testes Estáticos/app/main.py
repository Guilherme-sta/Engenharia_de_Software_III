from fastapi import FastAPI
from app.routers import laboratorios
from app.routers import reserva_router

app = FastAPI(
    title='Sistema de Reserva de Laboratórios',
    description='IFPI TADS — Engenharia de Software II',
    version='1.0.0',
)

app.include_router(laboratorios.router)
app.include_router(reserva_router.router)

@app.get('/')
def root():
    return {'message': 'API de Reserva de Laboratórios — acesse /docs'}