import pytest
from typing import Type
from JuegoTresEnRaya import JuegoTresEnRaya
from TresEnRayaShamir import TresEnRayaShamirAPI

@pytest.fixture
def juego() -> JuegoTresEnRaya:
    # Inyección de dependencia: usamos la interfaz, instanciando la implementación
    return TresEnRayaShamirAPI()

def test_movimiento_valido(juego: JuegoTresEnRaya):
    resultado = juego.realizar_movimiento(0, 0)
    assert resultado is True
    assert juego.obtener_tablero()[0][0] == 'X'

def test_movimiento_en_celda_ocupada(juego: JuegoTresEnRaya):
    juego.realizar_movimiento(1, 1)
    resultado = juego.realizar_movimiento(1, 1)
    assert resultado is False

def test_cambio_de_turno(juego: JuegoTresEnRaya):
    juego.realizar_movimiento(0, 0)
    assert juego.obtener_jugador_actual() == 'O'
    juego.realizar_movimiento(0, 1)
    assert juego.obtener_jugador_actual() == 'X'

def test_movimiento_fuera_de_rango(juego: JuegoTresEnRaya):
    resultado = juego.realizar_movimiento(3, 3)
    assert resultado is False
    resultado = juego.realizar_movimiento(-1, 0)
    assert resultado is False

def test_movimiento_despues_de_ganar(juego: JuegoTresEnRaya):
    # X gana
    juego.realizar_movimiento(0, 0)  # X
    juego.realizar_movimiento(1, 0)  # O
    juego.realizar_movimiento(0, 1)  # X
    juego.realizar_movimiento(1, 1)  # O
    juego.realizar_movimiento(0, 2)  # X gana

    assert juego.verificar_ganador() == 'X'
    resultado = juego.realizar_movimiento(2, 2)  # Ya no se puede mover
    assert resultado is False


# 1. Test reiniciar_juego resets tablero and player
def test_reiniciar_resets_state(juego):
    juego.realizar_movimiento(0,0)
    juego.realizar_movimiento(1,1)
    juego.reiniciar_juego()
    tablero = juego.obtener_tablero()
    assert all(cell == '' for row in tablero for cell in row)
    assert juego.obtener_jugador_actual() == 'X'
    assert not juego.esta_juego_terminado()

# 2. Test deep copy of tablero  XDD
def test_tablero_deep_copy(juego):
    copia = juego.obtener_tablero()
    copia[0][0] = 'Z'
    assert juego.obtener_tablero()[0][0] == ''

# 3. Test invalid move does not change turn
def test_invalid_move_no_turn_change(juego):
    initial = juego.obtener_jugador_actual()
    resultado = juego.realizar_movimiento(5,5)
    assert resultado is False
    assert juego.obtener_jugador_actual() == initial

# 4. Test negative and out-of-range moves
@pytest.mark.parametrize("fila,columna", [(-1,-1), (3,0), (0,3), (10,10)])
def test_move_out_of_range(juego, fila, columna):
    assert not juego.realizar_movimiento(fila, columna)

# 5. Test victory on main diagonal
def test_main_diagonal_victory(juego):
    moves = [(0,0),(0,1),(1,1),(0,2),(2,2)]
    for m in moves:
        juego.realizar_movimiento(*m)
    assert juego.verificar_ganador() == 'X'
    assert juego.esta_juego_terminado()

# 6. Test victory on anti-diagonal
def test_anti_diagonal_victory(juego):
    moves = [(0,2),(0,1),(1,1),(2,1),(2,0)]
    for m in moves:
        juego.realizar_movimiento(*m)
    assert juego.verificar_ganador() == 'X'

# 7. Test O can win
def test_o_can_win(juego):
    # X at (0,0), O at (1,1), X (0,1), O (2,2), X (0,2), O (0,2) invalid, O wins diagonal
    juego.realizar_movimiento(0,0)  # X
    juego.realizar_movimiento(1,1)  # O
    juego.realizar_movimiento(0,1)  # X
    juego.realizar_movimiento(2,2)  # O
    juego.realizar_movimiento(1,0)  # X
    juego.realizar_movimiento(0,2)  # O
    juego.realizar_movimiento(1,2)  # X
    resultado = juego.realizar_movimiento(2,0)  # O
    assert resultado is True
    assert juego.verificar_ganador() == 'O'

# 8. Test no winner during play
def test_no_winner_yet(juego):
    juego.realizar_movimiento(0,0)
    assert juego.verificar_ganador() is None

# 9. Test empate

def test_empate(juego: JuegoTresEnRaya):
    jugadas = [
        (0, 0), (1, 1), (0, 1),
        (0, 2), (2, 0), (1, 0),
        (1, 2), (2, 1), (2, 2)
    ]
    for fila, col in jugadas:
        juego.realizar_movimiento(fila, col)
    assert juego.verificar_ganador() == "Empate"

# 10. Test no moves after end
def test_no_moves_after_end(juego):
    # create quick win
    juego.realizar_movimiento(0,0)
    juego.realizar_movimiento(1,0)
    juego.realizar_movimiento(0,1)
    juego.realizar_movimiento(1,1)
    juego.realizar_movimiento(0,2)
    assert juego.verificar_ganador() == 'X'
    assert not juego.realizar_movimiento(2,2)

# 11. Test obtener_tablero always 3x3
def test_tablero_shape(juego):
    tablero = juego.obtener_tablero()
    assert len(tablero) == 3
    assert all(len(row) == 3 for row in tablero)

# 12. Test multiple reiniciar calls
def test_multiple_reiniciar_calls(juego):
    for _ in range(5):
        juego.realizar_movimiento(0,0)
        juego.reiniciar_juego()
    assert juego.obtener_jugador_actual() == 'X'

# 13. Test turn alternation after valid moves
def test_turn_alternation(juego):
    assert juego.obtener_jugador_actual() == 'X'
    juego.realizar_movimiento(0,0)
    assert juego.obtener_jugador_actual() == 'O'
    juego.realizar_movimiento(1,1)
    assert juego.obtener_jugador_actual() == 'X'

# 14. Test invalid repeated move on occupied cell
def test_repeated_move_occupied(juego):
    assert juego.realizar_movimiento(2,2)
    assert not juego.realizar_movimiento(2,2)

# 15. Test verifying ganador does not change state
def test_verificar_no_side_effects(juego):
    juego.realizar_movimiento(0,0)
    antes = juego.obtener_tablero()
    _ = juego.verificar_ganador()
    despues = juego.obtener_tablero()
    assert antes == despues

# 16. Test obtener_jugador_actual type
def test_obtener_jugador_actual_type(juego):
    jugador = juego.obtener_jugador_actual()
    assert isinstance(jugador, str)
    assert jugador in ('X','O')

# 17. Test realizar_movimiento returns bool
@staticmethod
def validar_return_type(juego, fila, col):
    ret = juego.realizar_movimiento(fila, col)
    assert isinstance(ret, bool)

def test_return_type(juego):
    validar_return_type(juego, 0, 0)
    validar_return_type(juego, -1, 0)

# 18. Test board immutability on obtener_tablero modifications
def test_tablero_immutability(juego):
    tablero1 = juego.obtener_tablero()
    tablero1_copy = [row.copy() for row in tablero1]
    tablero1[0][0] = 'X'
    assert juego.obtener_tablero() == tablero1_copy

# 19. Test esta_juego_terminado consistency
def test_esta_juego_terminado_consistency(juego):
    assert not juego.esta_juego_terminado()
    juego.realizar_movimiento(0,0)
    juego.realizar_movimiento(1,0)
    juego.realizar_movimiento(0,1)
    juego.realizar_movimiento(1,1)
    juego.realizar_movimiento(0,2)
    assert juego.esta_juego_terminado()
