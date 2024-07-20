import random

def print_board(board):
    for row in board:
        print(" ".join(row))

def random_row(board):
    return random.randint(0, len(board) - 1)

def random_col(board):
    return random.randint(0, len(board[0]) - 1)

def main():
    # Initialize the game board
    board = [["O"] * 5 for _ in range(5)]
    
    print("Let's play Battleship!")
    print_board(board)
    
    # Place the battleship randomly on the board
    ship_row = random_row(board)
    ship_col = random_col(board)
    
    # Allow the player 5 turns to guess
    for turn in range(5):
        print(f"Turn {turn + 1}")
        
        # Get player's guess
        guess_row = int(input("Guess Row: "))
        guess_col = int(input("Guess Col: "))
        
        if guess_row == ship_row and guess_col == ship_col:
            print("Congratulations! You sank my battleship!")
            break
        else:
            if (guess_row < 0 or guess_row >= 5) or (guess_col < 0 or guess_col >= 5):
                print("Oops, that's not even in the ocean.")
            elif board[guess_row][guess_col] == "X":
                print("You guessed that one already.")
            else:
                print("You missed my battleship!")
                board[guess_row][guess_col] = "X"
            if turn == 4:
                print("Game Over. The battleship was at:")
                print(f"Row: {ship_row}, Col: {ship_col}")
        
        print_board(board)

if __name__ == "__main__":
    main()
