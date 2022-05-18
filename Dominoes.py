import itertools
import random
import re
import collections


class Dominoes():
    def __init__(self):
        self.stock_pieces = []
        self.player_pieces = []
        self.comp_pieces = []
        self.domino_snake = []

    def get_domino_stock(self):
        stock = list(itertools.combinations(range(7), 2))
        for i in range(7):
            stock.append((i, i))
        self.stock_pieces = list(map(list, stock))


    def get_domino_bricks(self):
        for _ in range(7):
            self.player_pieces.append(self.stock_pieces.pop(self.stock_pieces.index(random.choice(self.stock_pieces))))
            self.comp_pieces.append(self.stock_pieces.pop(self.stock_pieces.index(random.choice(self.stock_pieces))))


    def prepare_to_play(self):
        for i in range(6, 0, -1):
            if [i, i] in self.player_pieces:
                self.domino_snake.append(self.player_pieces.pop(self.player_pieces.index([i, i])))
                self.status = 'computer'
                break
            elif [i, i] in self.comp_pieces:
                self.domino_snake.append(self.comp_pieces.pop(self.comp_pieces.index([i, i])))
                self.status = 'player'
                break
        else:
            return -1


    def display(self):
        print("======================================================================")
        print(f"Stock size: {len(self.stock_pieces)}")
        print(f"Computer pieces: {len(self.comp_pieces)}\n")
        if len(self.domino_snake) <= 6:
            print(*self.domino_snake, sep='', end='\n')
        else:
            print(*self.domino_snake[:3], '...', *self.domino_snake[-3:], sep='', end='\n')

        print("Your pieces:")
        for num, brick in enumerate(self.player_pieces, 1):
            print(num, brick, sep=':')

        print()
        if self.status == 'player':
            print("Status: It's your turn to make a move. Enter your command.")
        elif self.status == 'computer':
            print("Status: Computer is about to make a move. Press Enter to continue...")
        elif self.status == 'player win':
            print("Status: The game is over. You won!")
        elif self.status == 'computer win':
            print("Status: The game is over. The computer won!")
        elif self.status == 'draw':
            print("Status: The game is over. It's a draw!")


    def player_move(self, request):
        pattern = r'^-?[0-7]$'
        if re.match(pattern, request) == None:
            print("Invalid input. Please try again.")
            return -1
        req = list(request)
        if len(req) > 1:
            if int(req[1]) > len(self.player_pieces):
                print("You don't have sufficient amount of pieces")
                return -1
            elif self.add_piece_to_snake(int(req[1]) - 1, 'left') == -1:
                print("Illegal move. Please try again.")
                return -1
            # self.domino_snake.insert(0, self.player_pieces.pop(int(req[1]) - 1))
        elif int(req[0]) > 0:
            if int(req[0]) > len(self.player_pieces):
                print("You don't have sufficient amount of pieces")
                return -1
            elif self.add_piece_to_snake(int(req[0]) - 1, 'right') == -1:
                print("Illegal move. Please try again.")
                return -1
            # self.domino_snake.append(self.player_pieces.pop(int(req[0]) - 1))
        else:
            self.player_pieces.append(self.stock_pieces.pop(self.stock_pieces.index(random.choice(self.stock_pieces))))
        self.status = 'computer'


    def comp_move(self):

        num_occurance = collections.Counter(itertools.chain(*self.comp_pieces, *self.domino_snake))
        comp_pieces_rank = dict()
        for enum, piece in enumerate(self.comp_pieces):
            comp_pieces_rank[enum] = num_occurance.get(piece[0]) + num_occurance.get(piece[1])

        for rank in sorted(comp_pieces_rank.values(), reverse=True):
            selected_piece = list(comp_pieces_rank.keys())[list(comp_pieces_rank.values()).index(rank)]

            if self.add_piece_to_snake(selected_piece, 'left') != -1:
                break
            if self.add_piece_to_snake(selected_piece, 'right') != -1:
                break
        else:
            self.comp_pieces.append(self.stock_pieces.pop(self.stock_pieces.index(random.choice(self.stock_pieces))))

        self.status = 'player'


    def result_check(self):
        if self.domino_snake[0][0] == self.domino_snake[-1][-1]:
            checked_num = self.domino_snake[0][0]
            exist_amount = 0
            for piece in self.domino_snake:
                if checked_num in piece:
                    exist_amount += 1
            if exist_amount >= 8:
                self.status = 'draw'
                return
        if len(self.player_pieces) == 0:
            self.status = 'player win'
        elif len(self.comp_pieces) == 0:
            self.status = 'computer win'
        elif len(self.stock_pieces) == 0:
            self.status = 'draw'
            # if len(self.comp_pieces) > len(self.player_pieces):
            #     self.status = 'player win'
            # elif len(self.comp_pieces) < len(self.player_pieces):
            #     self.status = 'computer win'




    def add_piece_to_snake(self, piece_no, snake_side):
        if self.status == 'player':
            if snake_side == 'left':
                if self.domino_snake[0][0] not in self.player_pieces[piece_no]:
                    return -1
                elif self.domino_snake[0][0] == self.player_pieces[piece_no][0]:
                    self.player_pieces[piece_no].reverse()
                    self.domino_snake.insert(0, self.player_pieces.pop(piece_no))
                elif self.domino_snake[0][0] == self.player_pieces[piece_no][1]:
                    self.domino_snake.insert(0, self.player_pieces.pop(piece_no))
                else:
                    assert False, "add_piece_to_snake player left side forbidden option"
            elif snake_side == 'right':
                if self.domino_snake[-1][-1] not in self.player_pieces[piece_no]:
                    return -1
                elif self.domino_snake[-1][-1] == self.player_pieces[piece_no][0]:
                    self.domino_snake.append(self.player_pieces.pop(piece_no))
                elif self.domino_snake[-1][-1] == self.player_pieces[piece_no][1]:
                    self.player_pieces[piece_no].reverse()
                    self.domino_snake.append(self.player_pieces.pop(piece_no))
                else:
                    assert False, "add_piece_to_snake player right side forbidden option"
        elif self.status == 'computer':
            if snake_side == 'left':
                if self.domino_snake[0][0] not in self.comp_pieces[piece_no]:
                    return -1
                elif self.domino_snake[0][0] == self.comp_pieces[piece_no][0]:
                    self.comp_pieces[piece_no].reverse()
                    self.domino_snake.insert(0, self.comp_pieces.pop(piece_no))
                elif self.domino_snake[0][0] == self.comp_pieces[piece_no][1]:
                    self.domino_snake.insert(0, self.comp_pieces.pop(piece_no))
                else:
                    assert False, "add_piece_to_snake computer left side forbidden option"
            elif snake_side == 'right':
                if self.domino_snake[-1][-1] not in self.comp_pieces[piece_no]:
                    return -1
                elif self.domino_snake[-1][-1] == self.comp_pieces[piece_no][0]:
                    self.domino_snake.append(self.comp_pieces.pop(piece_no))
                elif self.domino_snake[-1][-1] == self.comp_pieces[piece_no][1]:
                    self.comp_pieces[piece_no].reverse()
                    self.domino_snake.append(self.comp_pieces.pop(piece_no))
                else:
                    assert False, "add_piece_to_snake computer right side forbidden option"
        else:
            assert False, "add_piece_to_snake Wrong status"


dominoes_game = Dominoes()

# game preparation
while True:
    dominoes_game.get_domino_stock()
    dominoes_game.get_domino_bricks()
    if dominoes_game.prepare_to_play() != -1:
        break
    else:
        continue

while True:
    dominoes_game.display()
    if dominoes_game.status == 'computer':
        input()
        dominoes_game.comp_move()
    elif dominoes_game.status == 'player':
        while True:
            if dominoes_game.player_move(input()) != -1:
                break
    elif dominoes_game.status in {'player win', 'computer win', 'draw'}:
        break
    dominoes_game.result_check()



