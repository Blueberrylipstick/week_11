"""A simple game of tic-tac-toe."""
from board import Board
def play_game():
    """Play a game of tic-tac-toe."""
    board = Board()
    turn = 'x'

    while True:
        print(board)
        status = board.get_status()

        if status != 'continue':
            if status == 'draw':
                print("It's a draw!")
            else:
                print(f"{status} wins!")
            break

        if turn == 'x':
            try:
                position = tuple(int(x) for x\
in input("Enter your move (row, column): ").split(','))
                board.make_move(position, turn)
                turn = '0'
            except (IndexError, ValueError):
                print("Invalid move. Try again.")
        else:
            board.make_computer_move()
            turn = 'x'
if __name__ == 'main':
    play_game()
