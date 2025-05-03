import copy
from JuegoTresEnRaya import JuegoTresEnRaya

class TresEnRayaShamirAPI(JuegoTresEnRaya):
    def __init__(self):
        self.board = Board()
        self.turno = 'X'
        self.estado = None

    def reiniciar_juego(self):
        self.board = Board()
        self.turno = 'X'
        self.estado = None
    
    def realizar_movimiento(self, fila, columna):
        if self.estado != None:
            return False  
        
        if self.board.play(fila, columna, self.turno):
            if self.board.checkWin(self.turno):
                self.estado = self.turno
            elif self.board.isFull():
                self.estado = "Empate"
            else:
                self.turno = 'O' if self.turno == 'X' else 'X'
            return True
        else:
            return False
    
    def obtener_tablero(self):
        return copy.deepcopy(self.board.grid)

    def verificar_ganador(self):
        return copy.deepcopy(self.estado)

    def obtener_jugador_actual(self):
        return copy.deepcopy(self.turno)

    def esta_juego_terminado(self):
        return False if self.estado == None else True

class Board:
    def __init__(self):
        self.grid = [['' for _ in range(3)] for _ in range(3)]
    
    def play(self, row, col, letra):
        if 0 <= row < 3 and 0 <= col < 3 and self.grid[row][col] == '':
            self.grid[row][col] = letra
            return True
        return False
    
    def checkWin(self, letra):
        for row in self.grid:
            if row == [letra] * 3:
                return True
        
        for col in range(3):
            if [self.grid[row][col] for row in range(3)] == [letra] * 3:
                return True
        
        if [self.grid[i][i] for i in range(3)] == [letra] * 3:
            return True
        
        if [self.grid[i][2 - i] for i in range(3)] == [letra] * 3:
            return True
        
        return False

    def isFull(self):
        for row in self.grid:
            for cell in row:
                if cell == '':
                    return False
        return True

