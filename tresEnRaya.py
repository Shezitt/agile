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
    def __init__(self):
        self.board = Board()
        self.players = [Player('X'), Player('O')]

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

if __name__ == "__main__":
    Game().run()