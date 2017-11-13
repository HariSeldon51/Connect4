import math
import random
import time


class GameState:
    """An abstract class which can be extended to provide an object which
    handles the rendering and updating during a particular state of the game"""
    game_state_manager = None

    def __init__(self, game_state_manager):
        self.game_state_manager = game_state_manager

    def render(self, game_objects, game_players):
        raise NotImplementedError()

    def update(self, game_objects, game_players):
        raise NotImplementedError()

    @staticmethod
    def print_error(message):
        print("------------------------------")
        print("!! I'm sorry, that's not a a valid response.")
        print(message + " !!")
        print("------------------------------")

    @staticmethod
    def player_input(text, input_min, input_max, error='That is not a valid entry -- please try again'):
        while True:
            try:
                data = input(text)
                if int(data) < input_min or int(data) > input_max:
                    GameState.print_error(error)
                    continue
                else:
                    return int(data)
            except ValueError:
                print(error)
                continue


class GameObject:
    """An abstract class which can be extended to provide an object which
    handles the rendering and updating of a game object"""
    game_object_list = None

    def __init__(self, game_object_list):
        self.game_object_list = game_object_list

    def render(self, game_state, game_players):
        raise NotImplementedError()

    def update(self, game_state, game_players, current_player):
        raise NotImplementedError()


class GamePlayer:
    """A class representing a player in the game"""
    name = None
    token = None
    player_type = None
    types = ('human', 'computer')

    def __init__(self, name, token, player_type):
        self.name = name
        self.token = token
        self.player_type = player_type

    def render(self):
        print("It is now " + self.name + "'s turn (" + self.token + ")")


class GameStart(GameState):

    def render(self, game_objects, game_players):
        print('========================')
        print('Welcome to Connect More!')
        print('------------------------')
        print(' a game by Will DeHaven')
        print('   written in Python3')
        print('========================')

    def update(self, game_objects, game_players):
        time.sleep(4)
        self.game_state_manager.change_state('setup')


class GameSetup(GameState):
    error1 = "Please enter a number between 5 and 9"
    error2 = "Please enter a number between 3 and 5"
    computer_tokens = ['X', 'Y', 'Z', 'Q']
    computer_names = ['Howard', 'Frances', 'John', 'Ada', 'Charles', 'Evelyn', 'Bertrand', 'Ida', 'Alan', 'Kathleen']
    player_tokens = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
    player_tokens.extend(['N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])

    def render(self, game_objects, game_players):
        print('Game Setup:')
        print('--------------------------------------')

    def update(self, game_objects, game_players):
        time.sleep(2)
        print("Let's set up the game board...")
        print('--------------------------------------')
        time.sleep(2)
        width = int(self.player_input('How many columns wide (5-9)? ', 5, 9, self.error1))
        height = int(self.player_input('How many rows high (5-9)? ', 5, 9, self.error1))
        win = int(self.player_input('How many tokens in a row are needed to win (3-5)? ', 3, 5, self.error2))
        board = Board(game_objects, width, height, win)
        game_objects.append(board)
        time.sleep(1)
        print(".")
        time.sleep(1)
        print(".")
        time.sleep(1)
        print(".")
        time.sleep(1)
        print("The game board has been assembled")
        time.sleep(2)
        print("Now let's set up the players...")
        print('--------------------------------------')
        time.sleep(2)
        max_players = int(math.floor(math.sqrt(width * height) / 2))
        print("For your board size (" + str(width) + "x" + str(height) + "),")
        time.sleep(2)
        print("there can be up to " + str(max_players) + " players, human or computer")
        time.sleep(2)

        while True:
            human = int(self.player_input('How many human players? ', 1, max_players))
            computer = int(self.player_input('How many computer players? ', 0, max_players))

            if human + computer > max_players:
                print("------------------------------")
                print("!! " + str(human) + " human players + " + str(computer) + " computer players is too many!")
                print("There can only be up to " + str(max_players) + " total players !!")
                print("------------------------------")
            elif human + computer < 2:
                print("------------------------------")
                print("!! " + str(human) + " human players + " + str(computer) + " computer players is too few!")
                print("There must be at least 2 total players !!")
                print("------------------------------")
            else:
                break

        print("Preparing to register " + str(human) + " human players and " + str(computer) + " computer players.")
        for player in range(human):
            title = "Player " + str(player + 1)
            time.sleep(2)

            while True:
                name = str(input(title + ", please enter your name: "))
                if all(i.isalpha() or i == ' ' for i in name):
                    break
                else:
                    print("------------------------------")
                    print("!! Please enter a name that contains only letters and spaces !!")
                    print("------------------------------")
                    continue

            while True:
                try:
                    token = str(input(title + ", please select a letter as your token: "))
                    if token.isalpha() and len(token) == 1:
                        token.upper()
                        self.player_tokens.remove(token)
                        if self.computer_tokens.count(token) > 0:
                            self.computer_tokens.remove(token)
                        break
                    else:
                        print("------------------------------")
                        print("!! Your entry was either not a letter or was longer than 1 letter !!")
                        print("------------------------------")
                        continue
                except ValueError:
                    print("------------------------------")
                    print("!! That token has already been selected by another player !!")
                    print("------------------------------")

            human_player = GamePlayer(name, token, 0)
            game_players.append(human_player)
            print("Great, " + str(name) + "! Your token is the letter " + str(token))

        if computer > 0:
            time.sleep(2)
            print("You will be joined by the following computer players:")
            for player in range(computer):
                name = random.choice(self.computer_names)
                self.computer_names.remove(name)
                token = random.choice(self.computer_tokens)
                self.computer_tokens.remove(token)

                computer_player = GamePlayer(name, token, 1)
                game_players.append(computer_player)

                time.sleep(2)
                print("  " + name + ", whose token will be the letter " + token)

        time.sleep(2)
        print('--------------------------------------')
        print("We are now ready! Let's play...")
        print('--------------------------------------')

        time.sleep(4)
        self.game_state_manager.change_state('play')


class GamePlay(GameState):
    currentPlayer = 0

    def render(self, game_objects, game_players):
        game_players[self.currentPlayer].render()
        for game_object in game_objects:
            game_object.render(self, game_players)

    def update(self, game_objects, game_players):
        for game_object in game_objects:
            game_object.update(self, game_players, game_players[self.currentPlayer])

        if self.currentPlayer + 1 >= len(game_players):
            self.currentPlayer = 0
        else:
            self.currentPlayer += 1


class GameWin(GameState):

    def render(self, game_objects, game_players):
        print('==============================')
        print("Congratulations! You Win!")
        print('==============================')

    def update(self, game_objects, game_players):
        self.game_state_manager.change_state('end')


class GameEnd(GameState):

    def render(self, game_objects, game_players):
        print('\n')
        print('================================')
        print('Thanks for playing Connect More!')
        print('--------------------------------')
        print("       Goodbye for now...")
        print('================================')

    def update(self, game_objects, game_players):
        self.game_state_manager.end_game()


class GameStateManager:
    """Maintains current game state as well as list of available game states"""

    # The available game states for this game
    gameStates = {'start': None, 'setup': None, 'play': None, 'end': None}
    currentState = None
    game = None

    def __init__(self, main_game, state='start'):
        self.change_state(state)
        self.game = main_game
        self.gameStates['start'] = GameStart(self)
        self.gameStates['setup'] = GameSetup(self)
        self.gameStates['play'] = GamePlay(self)
        self.gameStates['win'] = GameWin(self)
        self.gameStates['end'] = GameEnd(self)

    # Allows the game state to be changed
    def change_state(self, state):
        self.currentState = state

    # Allows the game to be ended
    def end_game(self):
        self.game.end()

    # Renders the game according to the current game state
    def render(self, game_objects, game_players):
        self.gameStates[self.currentState].render(game_objects, game_players)

    # Updates the game according to the current game state
    def update(self, game_objects, game_players):
        self.gameStates[self.currentState].update(game_objects, game_players)


class Game:
    gameOn = None
    gameObjectList = None
    gamePlayerList = None
    gameStateManager = None

    def __init__(self):
        self.gameOn = True
        self.gameObjectList = []
        self.gamePlayerList = []
        self.gameStateManager = GameStateManager(self, 'start')

    # Start the game loop
    def start(self):
        while self.gameOn:
            self.game_loop()

    # End the game loop
    def end(self):
        self.gameOn = False

    # Run render and update methods in each loop cycle
    def game_loop(self):
        self.gameStateManager.render(self.gameObjectList, self.gamePlayerList)
        self.gameStateManager.update(self.gameObjectList, self.gamePlayerList)


class Board(GameObject):
    spaces = list()
    boardWidth = None
    boardHeight = None
    win = None
    conditions = ['vertical', 'horizontal', 'forward diagonal', 'backward diagonal']
    div1 = ""
    div2 = ""
    heading = ""
    input_message = "Select a column to drop your token: "
    error = "Please choose a column between 1 and "

    def __init__(self, game_objects, width=7, height=6, win=4):
        super().__init__(game_objects)
        self.boardWidth = width
        self.boardHeight = height
        self.win = win

        # Initializes a two-dimensional array and sets all spaces on the board to 0 (empty)
        # Afterward, first index will reference the 'column' - second index will reference items in each column ('row')
        self.spaces = [[0 for row in range(self.boardHeight)] for column in range(self.boardWidth)]

        for i in range(self.boardWidth):
            self.div1 += "==="
            self.div2 += "---"
            self.heading += " " + str(i+1) + " "

    def render(self, game_state, player_list):
        print(self.div1)
        print('Columns:')
        print(self.heading)
        print(self.div2)

        # Iterate through each row of the board
        for j in range(self.boardHeight):
            row = ""

            # Iterate through each column of each row
            for i in range(self.boardWidth):
                if self.spaces[i][j] < 1:
                    row += "[ ]"
                else:
                    row += "[" + player_list[self.spaces[i][j] - 1].token + "]"

            print(row)

        print(self.div2)

    def update(self, game_state, player_list, current_player):
        name = current_player.name
        token = current_player.token

        if current_player.player_type < 1:
            # Ask player which column to place token
            while True:
                column = game_state.player_input(self.input_message, 1, self.boardWidth, self.error + str(self.boardWidth))
                if self.spaces[column - 1][0] > 0:
                    print("Column " + str(column) + " is full. Please choose another column")
                    continue
                else:
                    break
        else:
            # Choose a random column with at least one open space
            while True:
                column = random.randrange(self.boardWidth)
                if self.spaces[column][0] > 0:
                    continue
                else:
                    break

        for x in range(60):
            print("\n")
        print(name + " dropped their token (" + token + ") in column " + str(column))

        # Place the token in the column
        for i in range(self.boardHeight):
            if i == self.boardHeight - 1 and self.spaces[column - 1][i] < 1:
                self.spaces[column - 1][i] = player_list.index(current_player) + 1
                if self.check_win(column - 1, i, player_list.index(current_player) + 1):
                    print(name + " wins! Well done")
                    self.render(game_state, player_list)
                    game_state.game_state_manager.change_state("win")
            elif self.spaces[column - 1][i] < 1:
                pass
            elif i > 0 and self.spaces[column - 1][i-1] < 1:
                self.spaces[column - 1][i-1] = player_list.index(current_player) + 1
                if self.check_win(column - 1, i-1, player_list.index(current_player) + 1):
                    print(name + " wins! Well done")
                    self.render(game_state, player_list)
                    game_state.game_state_manager.change_state("win")

    def check_win(self, col, row, num):
        for condition in self.conditions:

            if condition == 'horizontal':
                tally = 1
                for x in range(1, self.win):
                    if col - x >= 0 and self.spaces[col - x][row] == num:
                        tally += 1
                    else:
                        break
                for x in range(1, self.win):
                    if col + x < self.boardWidth and self.spaces[col + x][row] == num:
                        tally += 1
                    else:
                        break

            elif condition == 'vertical':
                tally = 1
                for x in range(1, self.win):
                    if row - x >= 0 and self.spaces[col][row - x] == num:
                        tally += 1
                    else:
                        break
                for x in range(1, self.win):
                    if row + x < self.boardHeight and self.spaces[col][row + x] == num:
                        tally += 1
                    else:
                        break

            elif condition == 'forward diagonal':
                tally = 1
                for x in range(1, self.win):
                    if col - x >= 0 and row + x < self.boardHeight and self.spaces[col - x][row + x] == num:
                        tally += 1
                    else:
                        break
                for x in range(1, self.win):
                    if col + x < self.boardWidth and row - x >= 0 and self.spaces[col + x][row - x] == num:
                        tally += 1
                    else:
                        break

            elif condition == 'backward diagonal':
                tally = 1
                for x in range(1, self.win):
                    if col - x >= 0 and row - x >= 0 and self.spaces[col - x][row - x] == num:
                        tally += 1
                    else:
                        break
                for x in range(1, self.win):
                    if col + x < self.boardWidth and row + x < self.boardHeight and self.spaces[col+x][row+x] == num:
                        tally += 1
                    else:
                        break

            if tally >= self.win:
                print("There are " + str(tally) + " tokens in a " + condition + " row!")
                return True
            else:
                pass

        return False


# Initialize Game object and start the game!
game = Game()
game.start()
