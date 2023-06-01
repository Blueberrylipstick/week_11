"""Модуль для роботи з ігровим полем."""
class Board:
    """A simple game of tic-tac-toe."""
    def init(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.last_move = {'symbol': None, 'position': None}

    def get_status(self):
        """Перевірка статусу гри."""
        # Перевірка на виграш
        for i in range(3):
            # Перевірка рядків
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
            # Перевірка стовпців
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]
        # Перевірка діагоналей
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        # Перевірка на нічию
        if all(self.board[i][j] != ' ' for i in range(3) for j in range(3)):
            return 'draw'
        # Гра продовжується
        return 'continue'

    def make_move(self, position, turn):
        """A simple game of tic-tac-toe."""
        if self.board[position[0]][position[1]] == ' ':
            self.board[position[0]][position[1]] = turn
            self.last_move = {'symbol': turn, 'position': position}
        else:
            raise IndexError("Invalid move: position already occupied.")

    def make_computer_move(self):
        """Логіка для ходу комп'ютера (можна реалізувати по-різному)."""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.make_move((i, j), '0')
                    return None

    def str(self):
        rows = [str(row) for row in self.board]
        return '\n'.join(rows)