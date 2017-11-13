import random

class GameStateManager():

    render = None
    update = None
    gameStates = {'start': None, 'setup': None, 'play': None, 'end': None}

    def __new__(self, render, update):
        self.render = render
        self.update = update

class Game():

    gameOn = True
    board = None
    gameStateManager = GameStateManager()

    def start(self): 
        while self.gameOn == True:
            self.gameLoop()

    def end(self):
        self.gameOn = False
        
    def gameLoop(self):
        self.render()
        self.update()
        self.end()

    def render(self):
        self.board.render()

    def logic(self):
        print('It is your turn.')
        choice = input('Choose a column:')

class Board():

    spaces = list()
    boardWidth = None
    boardHeight = None
    

    def __init__(self, width=7, height=6):
        self.boardWidth = width
        self.boardHeight = height

        ## Initializes all spaces on the board to 0 (empty)
        for i in range(self.boardWidth * self.boardHeight):
            self.spaces.append(0)

    def render(self):
        print('Columns:')
        print(' 1  2  3  4  5  6  7')

        for i in range(self.boardHeight):
            print(self.getRow(i + 1))

    def getRow(self, row):
        rowList = list()
        start = (row - 1) * self.boardWidth

        for i in range(start, start + self.boardWidth):
            rowList.append(self.spaces[i])

        return rowList

game = Game()
game.start()
