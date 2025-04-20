class Player:
    def __init__(self, letra):
        self.letra = letra

    def getTurno(self):
        while True:
            move = input(f"Jugador {self.letra}, ingresa numero (0-2) de fila y columna: ")
            row, col = map(int, move.strip().split())
            if row in range(3) and col in range(3):
                return row, col
            else:
                print("Coordenadas fuera del tablero >:v")

class Board:
    def __init__(self):
        self.grid = [[' ' for _ in range(3)] for _ in range(3)]

    def printBoard(self):
        print("\nTablero:")
        for row in self.grid:
            for cell in row:
                print(f"| {cell} ", end="")   
            print("|")
        print("-------------")
    
    def play(self, row, col, letra):
        if self.grid[row][col] == ' ':
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
                if cell == ' ':
                    return False
        return True

class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.players = [player1, player2]

    def run(self):  
        turn = 0
        while True:
            self.board.printBoard()
            player = self.players[turn]

            while True:
                row, col = player.getTurno()
                if self.board.play(row, col, player.letra):
                    break
                else:
                    print("Posicion ocupada. Elige otra xd")
            
            if self.board.checkWin(player.letra):
                self.board.printBoard()
                print(f"Jugador {player.letra} gana, maestro!")
                break
            if self.board.isFull():
                self.board.printBoard()
                print("Empate :v")
                break
            
            turn = (turn + 1) % 2

class TresEnRayaAPI:
    def __init__(self):
        self.board = Board()
        self.turno = 'X'
        self.estado = "En progreso"

    def nuevaPartida(self):
        self.board = Board()
        self.turno = 'X'
        self.estado = "En progreso"

    def getTablero(self):
        return self.board.grid
    
    def mover(self, fila, columna):
        if self.estado != "En progreso":
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

    def getEstado(self):
        return self.estado

    def getTurnoActual(self):
        return self.turno

if __name__ == "__main__":
    # Game().run()
    api = TresEnRayaAPI()
    api.nuevaPartida()

    api.mover(0, 0)
    api.mover(1, 1)

    tablero = api.getTablero()
    estado = api.getEstado()
    turno = api.getTurnoActual()

    for fila in tablero:
        print(fila)
    print(f"el estado es {estado} y le toca al jugador {turno}")