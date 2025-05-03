from abc import ABC, abstractmethod
from typing import Optional, Tuple, List

class JuegoTresEnRaya(ABC):
    @abstractmethod
    def reiniciar_juego(self) -> None:
        """Reinicia el tablero y establece al jugador X como el primero en jugar."""

    @abstractmethod
    def realizar_movimiento(self, fila: int, columna: int) -> bool:
        """
        Intenta colocar el símbolo del jugador actual en la posición (fila, columna).
        Devuelve True si el movimiento fue válido, False si la celda ya estaba ocupada.
        """

    @abstractmethod
    def obtener_tablero(self) -> List[List[str]]:
        """
        Devuelve una copia del estado actual del tablero como una lista de listas.
        Las celdas vacías están representadas por una cadena vacía ''.
        """

    @abstractmethod
    def verificar_ganador(self) -> Optional[str]:
        """
        Verifica si hay un ganador.
        Devuelve 'X' o 'O' si uno ha ganado, 'Empate' si no hay más movimientos posibles,
        o None si el juego sigue en curso.
        """

    @abstractmethod
    def obtener_jugador_actual(self) -> str:
        """Devuelve el símbolo del jugador actual ('X' o 'O')."""

    @abstractmethod
    def esta_juego_terminado(self) -> bool:
        """Devuelve True si el juego ha terminado (ya sea por victoria o empate)."""

