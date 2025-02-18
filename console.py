from bot_algorithm import Minimax


def display_board(board):
    for i, row in enumerate(board):
        display_row = [str(i * 3 + j + 1) if cell == '_' else cell for j, cell in enumerate(row)]
        print(" | ".join(display_row))
        if i < 2:
            print("-" * 9)

def initialize_board():
    return [['_' for _ in range(3)] for _ in range(3)]

def play_game():
    print("Welcome to Group 4's Tic-Tac-Toe!")

    print("Grid reference numbers for moves:\n1 | 2 | 3\n4 | 5 | 6\n7 | 8 | 9\n")

    while True:
        choice = input("Choose X or O (X goes first): ").upper()
        player, bot = ('X', 'O') if choice == 'X' else ('O', 'X')

        board = initialize_board()
        minimax = Minimax(bot, player)
        player_turn = (player == 'X')

        while True:
            display_board(board)

            if minimax.evaluate(board) == 10:
                print("\nL\nO\nS\nE\nR\n")
                break
            elif minimax.evaluate(board) == -10:
                print("You win! Impossible!")
                break
            elif not minimax.isMovesLeft(board):
                print("It's a tie!")
                break

            if player_turn:
                move = int(input(f"Enter your move (1-9) as {player}: ")) - 1
                row, col = divmod(move, 3)
                if board[row][col] == '_':
                    board[row][col] = player
                    player_turn = False
                else:
                    print("Invalid move. Try again.")
            else:
                print("Bot is making its move...")
                bot_move = minimax.findBestMove(board)
                board[bot_move[0]][bot_move[1]] = bot
                player_turn = True

        # display_board(board)

        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

if __name__ == '__main__':
    play_game()