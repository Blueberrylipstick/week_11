'''module game'''
from board import Board

def main():
    '''main function'''
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
