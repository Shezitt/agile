import pytest
from TresEnRayaShamir import TresEnRayaShamir

@pytest.fixture
def partida():
    juego = TresEnRayaShamir()
    juego.reiniciar_juego()
    return juego

def test_jugada_valido(partida):
    assert partida.realizar_movimiento(0, 0) == True
    assert partida.obtener_tablero()[0][0] == 'X'

def test_turno_cambia(partida):
    partida.realizar_movimiento(0, 0)
    assert partida.obtener_jugador_actual() == 'O'

def test_jugada_en_posicion_ocupada(partida):
    partida.realizar_movimiento(0, 0)
    assert partida.realizar_movimiento(0, 0) == False

def test_estado_ganador(partida):
    partida.realizar_movimiento(0, 0)  # X
    partida.realizar_movimiento(1, 0)  # O
    partida.realizar_movimiento(0, 1)  # X
    partida.realizar_movimiento(1, 1)  # O
    partida.realizar_movimiento(0, 2)  # X gana
    assert partida.verificar_ganador() == 'X'

def test_empate(partida):
    jugadas = [
        (0, 0), (1, 1), (0, 1),
        (0, 2), (2, 0), (1, 0),
        (1, 2), (2, 1), (2, 2)
    ]
    for fila, col in jugadas:
        partida.realizar_movimiento(fila, col)
    assert partida.verificar_ganador() == "Empate"