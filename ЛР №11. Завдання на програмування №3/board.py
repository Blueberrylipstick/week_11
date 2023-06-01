'''module board'''

class Board:
    '''class board'''
    def __init__(self) -> None:
        '''initialization'''
        self.board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        self.last_move = (None, (None, None))

    def get_status(self):
        """Function to get board's status

        Returns:
            bool: result of the round
        """
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
        """Function to get string representation

        Returns:
            str: string representation
        """
        rows = [str(row) for row in self.board]
        return '\n'.join(rows)

    def make_move(self, position, turn):
        """Function to make a move

        Args:
            position (tuple(int)): position square
            turn (str): turn

        Raises:
            IndexError: if the indexes are wrong or square already occupied
        """
        if self.board[position[0]][position[1]] != ' ':
            raise IndexError

        self.board[position[0]][position[1]] = turn
        self.last_move = (turn, position)

    def make_computer_move(self):
        """Function for a computer to make a move

        Returns:
            None: nothing
        """
        turn = '0'
        for num, square_x in enumerate(self.board):
            for ind, square_y in enumerate(square_x):
                if square_y == ' ':
                    position = (num, ind)
                    self.make_move(position, turn)
                    return None
