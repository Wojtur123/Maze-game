import yaml


class Game:
    def __init__(self, name_of_gamefile):

        with open(name_of_gamefile, 'r') as gamefile:
            x = yaml.load(gamefile)
            self.player_position = x['player_position']
            self.board = x['board']

        number_of_treasures_left = 0
        for line in self.board:
            if '##' in line:
                for sign in line:
                    if sign == '##':
                        number_of_treasures_left += 1
        if self.player_position[-1] == 0 and len(self.player_position) == 3:
            self.player_position.append(number_of_treasures_left)
        self.score = self.player_position[-1] * 10
        self.actionlist = ((-1, 0), (1, 0), (0, 1), (0, -1))

    def move(self, direction):
        try:
            action = 'WSDA'.index(direction)
            nextpos = [self.player_position[0] + self.actionlist[action][0], self.player_position[1] + self.actionlist[action][1]]
            nextsign = self.board[nextpos[0]][nextpos[1]]
            if nextsign[0] in ('|' , '_'):
                return False
            if len(nextsign) == 2:
                if nextsign[1] == '!':
                    return True
                if nextsign[1] == '#':
                    self.player_position[-1] -= 1
                    self.score += 100
                    if self.player_position[-1] == 0:
                        return True
                    else:
                        self.player_position[0] = nextpos[0]
                        self.player_position[1] = nextpos[1]

            self.player_position[0] += self.actionlist[action][0]
            self.player_position[1] += self.actionlist[action][1]
            self.score -= 10

        except ValueError:
            return

    def display_board(self):
        number_of_line = 0
        for line in self.board:
            temporary_line = line
            if number_of_line == self.player_position[0]:
                temporary_line[self.player_position[1]] = '&'
                print(*temporary_line, end="\n")
                temporary_line[self.player_position[1]] = ' '
            else:
                print(*temporary_line, end="\n")
            number_of_line += 1

    def getinput(self):
        while True:
            tempinput = input("GO!")
            if tempinput in "wsdaWSDA":
                return tempinput.upper()
            elif tempinput in 'Qq':
                self.savegame()
                print("saved")
                continue

    def savegame(self):
        savegame = {'board': self.board,
                    'playerpos': self.player_position,
                    'score': self.score}
        with open('save.yml', 'w') as savefile:
            yaml.dump(savegame, savefile, default_flow_style=False)


while True:

    x = input('To load game press l, to new game press n')
    if x in 'lL':
        game = Game('save.yml')
    else:
        game = Game('board.yml')
    while True:
        game.display_board()
        temp = game.getinput()
        temp = game.move(temp)
        if temp:
            if game.player_position[-1] == 0:
                result = 'won, You escaped the maze !'
            else:
                result = 'lost, You will remain in the maze for eternity !'
            print('Game over, Score: {0}, You {1}'.format(game.score, result))
            break
    input("Press anything to load again")