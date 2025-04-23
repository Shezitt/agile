import pytest
from tresEnRaya import TresEnRayaAPI

@pytest.fixture
def partida():
    juego = TresEnRayaAPI()
    juego.nuevaPartida()
    return juego

def test_jugada_valido(partida):
    assert partida.jugar(0, 0) == True
    assert partida.getTablero()[0][0] == 'X'

def test_turno_cambia(partida):
    partida.jugar(0, 0)
    assert partida.getTurnoActual() == 'O'

def test_jugada_en_posicion_ocupada(partida):
    partida.jugar(0, 0)
    assert partida.jugar(0, 0) == False

def test_estado_ganador(partida):
    partida.jugar(0, 0)  # X
    partida.jugar(1, 0)  # O
    partida.jugar(0, 1)  # X
    partida.jugar(1, 1)  # O
    partida.jugar(0, 2)  # X gana
    assert partida.getEstado() == 'X'

def test_empate(partida):
    jugadas = [
        (0, 0), (1, 1), (0, 1),
        (0, 2), (2, 0), (1, 0),
        (1, 2), (2, 1), (2, 2)
    ]
    for fila, col in jugadas:
        partida.jugar(fila, col)
    assert partida.getEstado() == "Empate"