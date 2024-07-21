import random

def print_board(board):
    for row in board:
        print(" ".join(row))

def random_row(board):
    return random.randint(0, len(board) - 1)

def random_col(board):
    return random.randint(0, len(board[0]) - 1)

def place_ships(board, num_ships):
    ships = []
    while len(ships) < num_ships:
        row, col = random_row(board), random_col(board)
        if (row, col) not in ships:
            ships.append((row, col))
    return ships

def is_valid_input(input_str, board_size):
    return input_str.isdigit() and 0 <= int(input_str) < board_size

def get_distance(guess_row, guess_col, ship_row, ship_col):
    return abs(guess_row - ship_row) + abs(guess_col - ship_col)

def print_instructions():
    print("Welcome to Battleship!")
    print("Try to sink all the ships hidden on the board.")
    print("You have a limited number of turns to find them all.")
    print("Enter row and column numbers to make your guesses.")
    print("Good luck!\n")

def select_difficulty():
    while True:
        difficulty = input("Select difficulty (easy, medium, hard): ").lower()
        if difficulty in ['easy', 'medium', 'hard']:
            return difficulty
        else:
            print("Invalid difficulty. Please enter 'easy', 'medium', or 'hard'.")

def set_parameters(difficulty):
    if difficulty == 'easy':
        return 5, 2, 15  # board_size, num_ships, max_turns
    elif difficulty == 'medium':
        return 7, 3, 10
    else:
        return 10, 4, 8

def calculate_score(turn, max_turns):
    return max(0, max_turns - turn)

def update_leaderboard(leaderboard, player_name, score):
    leaderboard.append((player_name, score))
    leaderboard.sort(key=lambda x: x[1], reverse=True)

def print_leaderboard(leaderboard):
    print("\nLeaderboard:")
    for idx, (name, score) in enumerate(leaderboard):
        print(f"{idx + 1}. {name}: {score} points")

def give_hint(ships, guess_row, guess_col):
    closest_distance = min(get_distance(guess_row, guess_col, ship_row, ship_col) for ship_row, ship_col in ships)
    if closest_distance == 0:
        print("You hit a ship!")
    else:
        print(f"Hint: The closest ship is {closest_distance} units away.")

def ai_guess(board, previous_guesses):
    while True:
        guess_row = random_row(board)
        guess_col = random_col(board)
        if (guess_row, guess_col) not in previous_guesses:
            previous_guesses.add((guess_row, guess_col))
            return guess_row, guess_col

def main():
    leaderboard = []

    while True:
        print_instructions()
        
        difficulty = select_difficulty()
        board_size, num_ships, max_turns = set_parameters(difficulty)
        
        # Initialize the game boards
        player_board = [["O"] * board_size for _ in range(board_size)]
        ai_board = [["O"] * board_size for _ in range(board_size)]
        player_guesses = [["O"] * board_size for _ in range(board_size)]

        player_name = input("Enter your name: ")

        print("Player's Board:")
        print_board(player_board)
        
        # Place the battleships randomly on the boards
        player_ships = place_ships(player_board, num_ships)
        ai_ships = place_ships(ai_board, num_ships)

        ai_previous_guesses = set()

        # Allow the player and AI a certain number of turns to guess
        for turn in range(max_turns):
            print(f"\nTurn {turn + 1}")

            # Player's turn
            while True:
                guess_row = input(f"Guess Row (0-{board_size - 1}): ")
                guess_col = input(f"Guess Col (0-{board_size - 1}): ")
                if is_valid_input(guess_row, board_size) and is_valid_input(guess_col, board_size):
                    guess_row, guess_col = int(guess_row), int(guess_col)
                    break
                else:
                    print(f"Invalid input. Please enter numbers between 0 and {board_size - 1}.")

            player_hit = False
            for ship_row, ship_col in ai_ships:
                if guess_row == ship_row and guess_col == ship_col:
                    print("Congratulations! You sank a battleship!")
                    player_guesses[guess_row][guess_col] = "S"
                    ai_ships.remove((ship_row, ship_col))
                    player_hit = True
                    break
                elif get_distance(guess_row, guess_col, ship_row, ship_col) == 1:
                    print("So close! You were just one unit away from a battleship!")

            if not player_hit:
                if player_guesses[guess_row][guess_col] == "X":
                    print("You guessed that one already.")
                else:
                    print("You missed my battleship!")
                    player_guesses[guess_row][guess_col] = "X"
                    give_hint(ai_ships, guess_row, guess_col)

            print("Player's Guesses:")
            print_board(player_guesses)

            if not ai_ships:
                print("You sank all the AI's battleships! You win!")
                score = calculate_score(turn + 1, max_turns)
                print(f"Your score: {score}")
                update_leaderboard(leaderboard, player_name, score)
                print_leaderboard(leaderboard)
                break

            # AI's turn
            ai_guess_row, ai_guess_col = ai_guess(player_board, ai_previous_guesses)
            print(f"\nAI guesses: Row {ai_guess_row}, Col {ai_guess_col}")

            ai_hit = False
            for ship_row, ship_col in player_ships:
                if ai_guess_row == ship_row and ai_guess_col == ship_col:
                    print("AI sank one of your battleships!")
                    player_board[ai_guess_row][ai_guess_col] = "S"
                    player_ships.remove((ship_row, ship_col))
                    ai_hit = True
                    break

            if not ai_hit:
                print("AI missed your battleship!")
                player_board[ai_guess_row][ai_guess_col] = "X"

            print("Player's Board:")
            print_board(player_board)

            if not player_ships:
                print("AI sank all your battleships! You lose!")
                break

            if turn == max_turns - 1:
                print("Game Over. The remaining AI battleships were at:")
                for ship_row, ship_col in ai_ships:
                    print(f"Row: {ship_row}, Col: {ship_col}")

        # Ask if the player wants to play again
        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
