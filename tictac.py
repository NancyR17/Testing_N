def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, player):
    # Check rows, columns, and diagonals
    for row in board:
        if all(s == player for s in row):
            return True
    for col in range(3):
        if all(row[col] == player for row in board):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    turn = 0

    for _ in range(9):
        print_board(board)
        player = players[turn % 2]
        print(f"Player {player}'s turn")

        while True:
            try:
                row = int(input("Enter row (0, 1, 2): "))
                col = int(input("Enter column (0, 1, 2): "))
                if board[row][col] == " ":
                    board[row][col] = player
                    break
                else:
                    print("Cell already taken, try again.")
            except (ValueError, IndexError):
                print("Invalid input, try again.")

        if check_winner(board, player):
            print_board(board)
            print(f"Player {player} wins!")
            return

        turn += 1

    print_board(board)
    print("It's a tie!")

if __name__ == "__main__":
    tic_tac_toe()
