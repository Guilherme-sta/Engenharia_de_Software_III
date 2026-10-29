import pytest
from calculadora import Calculadora

def test_somar_acerto():
    calculadora = Calculadora()

    resultado = calculadora.somar(20, 10)

    assert resultado == 30

@pytest.mark.parametrize(
    "a, b, esperado",
    [
        (20, 10, 30),
        (10, 5, 15),
        (5, 5, 10),
        (100, 50, 150)
    ]
)

def test_somar_acerto_parametrizado(a, b, esperado):
    calculadora = Calculadora()

    resultado = calculadora.somar(a, b)

    assert resultado == esperado

def test_subtrair_acerto():
    calculadora = Calculadora()

    resultado = calculadora.subtrair(20, 10)

    assert resultado == 10

def test_multiplicar_acerto():
    calculadora = Calculadora()

    resultado = calculadora.multiplicar(20, 10)

    assert resultado == 200

def test_dividir_acerto():
    calculadora = Calculadora()

    resultado = calculadora.dividir(20, 10)

    assert resultado == 2

def test_dividir_por_zero_lanca_excecao():
    calculadora = Calculadora()

    with pytest.raises(ZeroDivisionError):
        calculadora.dividir(20, 0)

def test_somar_erro():
    calculadora = Calculadora()

    resultado = calculadora.somar(20, 10)

    assert resultado == 31

def test_subtrair_erro():
    calculadora = Calculadora()

    resultado = calculadora.subtrair(20, 10)

    assert resultado == 6

def test_multiplicar_erro():
    calculadora = Calculadora()

    resultado = calculadora.multiplicar(20, 10)

    assert resultado == 100

def test_dividir_erro():
    calculadora = Calculadora()

    resultado = calculadora.dividir(20, 10)

    assert resultado == 3