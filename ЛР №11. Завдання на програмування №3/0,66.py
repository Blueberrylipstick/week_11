import random

class Board:
    def __init__(self) -> None:
        self.board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        self.last_move = (None, (None, None))

    def get_status(self):
        res1x =  any(all(elem == 'x' for elem in value) for value in self.board)
        res10 = any(all(elem == '0' for elem in value) for value in self.board)
        res2x = any(all(self.board[i][j] == 'x' for i in range(3)) for j in range(3))
        res20 = any(all(self.board[i][j] == '0' for i in range(3)) for j in range(3))
        res3x = any([all(self.board[i][i] == 'x' for i in range(3)),\
            all(elem == 'x' for elem in [self.board[0][2], self.board[1][1], self.board[2][0]])])
        res30 = any([all(self.board[i][i] == '0' for i in range(3)),\
            all(elem == '0' for elem in [self.board[0][2], self.board[1][1], self.board[2][0]])])

        if any([res1x, res2x, res3x]):
            return 'x'

        if any([res10, res20, res30]):
            return '0'

        if any([elem == ' ' for val in self.board for elem in val]):
            return 'continue'

        return 'draw'

    def __str__(self) -> str:
        rows = [str(row) for row in self.board]
        return '\n'.join(rows)

    def make_move(self, position, turn):
        if self.board[position[0]][position[1]] != ' ':
            raise IndexError

        self.board[position[0]][position[1]] = turn
        self.last_move = (turn, position)

    def make_computer_move(self):
        while True:
            turn = '0'
            position = self.choice()
            try:
                self.make_move(position, turn)
                break
            except (IndexError, ValueError):
                continue

    def choice(self):
        for num, elem in enumerate(self.board):
            for ind, val in enumerate(elem):
                variants = [(num-1, ind-1), (num-1, ind), (num-1, ind+1),\
                            (num, ind-1), (num, ind+1),
                            (num+1, ind-1), (num+1, ind), (num+1, ind+1)]
                neighbors = []
                for pos in variants:
                    try:
                        if pos[0] < 0 or pos[1] < 0:
                            continue
                        neighbors.append(self.board[pos[0]][pos[1]] == '0')
                    except IndexError:
                        continue
                if val == '' and any(neighbors):
                    return num, ind
        return random.randint(0, 2), random.randint(0, 2)





from board import Board

def main():
    play_board = Board()
    turn = 'x'

    while True:
        print(play_board, '\n')

        if turn == 'x':
            try:
                move = input('Enter your move in such format: x y\n').split(' ')
                move = tuple(map(int, move))
                play_board.make_move(move, turn)
                turn = '0'
            except (IndexError, ValueError):
                print('Indexes out of range or slot already occupied')
        else:
            play_board.make_computer_move()
            turn = 'x'

        status = play_board.get_status()
        if status != 'continue':
            if status == 'draw':
                print(play_board, '\n')
                print('You\'r as good as the computer')
            else:
                print(f'{status} won!')
                print(play_board, '\n')
            break

if __name__ == '__main__':
    main()
