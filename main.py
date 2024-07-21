import random
import pickle

def print_board(board):
    for row in board:
        print(" ".join(row))

def random_row(board):
    return random.randint(0, len(board) - 1)

def random_col(board):
    return random.randint(0, len(board[0]) - 1)

def place_ships(board, num_ships):
    ships = []
    ship_sizes = [2, 3, 3, 4, 5]  # Example ship sizes
    for size in ship_sizes[:num_ships]:
        while True:
            orientation = random.choice(['horizontal', 'vertical'])
            row, col = random_row(board), random_col(board)
            if can_place_ship(board, row, col, size, orientation):
                ships.append((row, col, size, orientation))
                place_ship_on_board(board, row, col, size, orientation)
                break
    return ships

def can_place_ship(board, row, col, size, orientation):
    if orientation == 'horizontal':
        if col + size > len(board[0]):
            return False
        for i in range(size):
            if board[row][col + i] != "O":
                return False
    else:
        if row + size > len(board):
            return False
        for i in range(size):
            if board[row + i][col] != "O":
                return False
    return True

def place_ship_on_board(board, row, col, size, orientation):
    if orientation == 'horizontal':
        for i in range(size):
            board[row][col + i] = "S"
    else:
        for i in range(size):
            board[row + i][col] = "S"

def save_game(state):
    with open('battleship_save.pkl', 'wb') as f:
        pickle.dump(state, f)
    print("Game saved successfully!")

def load_game():
    try:
        with open('battleship_save.pkl', 'rb') as f:
            state = pickle.load(f)
        print("Game loaded successfully!")
        return state
    except FileNotFoundError:
        print("No saved game found.")
        return None

def is_valid_input(input_str, board_size):
    return input_str.isdigit() and 0 <= int(input_str) < board_size

def get_distance(guess_row, guess_col, ship_row, ship_col):
    return abs(guess_row - ship_row) + abs(guess_col - ship_col)

def print_instructions():
    print("Welcome to Battleship!")
    print("Try to sink all the ships hidden on the board.")
    print("You have a limited number of turns to find them all.")
    print("Enter row and column numbers to make your guesses.")
    print("You can save the game anytime by typing 'save'.")
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
    closest_distance = min(get_distance(guess_row, guess_col, ship_row, ship_col) for ship_row, ship_col, _, _ in ships)
    if closest_distance == 0:
        print("You hit a ship!")
    else:
        print(f"Hint: The closest ship is {closest_distance} units away.")

def ai_guess(board, previous_guesses, board_size):
    while True:
        guess_row, guess_col = strategic_guess(board, previous_guesses, board_size)
        if (guess_row, guess_col) not in previous_guesses:
            previous_guesses.add((guess_row, guess_col))
            return guess_row, guess_col

def strategic_guess(board, previous_guesses, board_size):
    # Improved AI strategy: prioritize areas around hits
    hit_coords = [(r, c) for r in range(board_size) for c in range(board_size) if board[r][c] == 'H']
    if hit_coords:
        for r, c in hit_coords:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < board_size and 0 <= nc < board_size and (nr, nc) not in previous_guesses:
                    return nr, nc
    return random_row(board), random_col(board)

def player_place_ships(board, num_ships):
    ship_sizes = [2, 3, 3, 4, 5]  # Example ship sizes
    ships = []
    for size in ship_sizes[:num_ships]:
        while True:
            print(f"Place your ship of size {size}.")
            row = int(input(f"Enter starting row (0-{len(board) - 1}): "))
            col = int(input(f"Enter starting col (0-{len(board[0]) - 1}): "))
            orientation = input("Enter orientation (horizontal/vertical): ").lower()
            if can_place_ship(board, row, col, size, orientation):
                ships.append((row, col, size, orientation))
                place_ship_on_board(board, row, col, size, orientation)
                print_board(board)
                break
            else:
                print("Invalid placement. Try again.")
    return ships

def track_statistics(stats, hit):
    if hit:
        stats['hits'] += 1
    else:
        stats['misses'] += 1
    stats['remaining_ships'] = len([row for row in stats['board'] if 'S' in row])

def display_statistics(stats):
    print(f"Hits: {stats['hits']}, Misses: {stats['misses']}, Remaining Ships: {stats['remaining_ships']}")

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
        
        # Place the battleships on the boards
        player_ships = player_place_ships(player_board, num_ships)
        ai_ships = place_ships(ai_board, num_ships)

        ai_previous_guesses = set()

        # Initialize game statistics
        player_stats = {'hits': 0, 'misses': 0, 'remaining_ships': num_ships, 'board': player_board}
        ai_stats = {'hits': 0, 'misses': 0, 'remaining_ships': num_ships, 'board': ai_board}

        # Allow the player and AI a certain number of turns to guess
        for turn in range(max_turns):
            print(f"\nTurn {turn + 1}")

            # Player's turn
            while True:
                guess_row = input(f"Guess Row (0-{board_size - 1}): ")
                guess_col = input(f"Guess Col (0-{board_size - 1}): ")
                if guess_row.lower() == 'save' or guess_col.lower() == 'save':
                    save_game((player_board, ai_board, player_guesses, player_ships, ai_ships, ai_previous_guesses, turn, max_turns, player_name, leaderboard, player_stats, ai_stats))
                    continue
                if is_valid_input(guess_row, board_size) and is_valid_input(guess_col, board_size):
                    guess_row, guess_col = int(guess_row), int(guess_col)
                    break
                else:
                    print(f"Invalid input. Please enter numbers between 0 and {board_size - 1}.")

            player_hit = False
            for ship_row, ship_col, size, orientation in ai_ships:
                if orientation == 'horizontal' and ship_row == guess_row and ship_col <= guess_col < ship_col + size:
                    print("Congratulations! You hit a battleship!")
                    player_guesses[guess_row][guess_col] = "H"
                    ai_board[guess_row][guess_col] = "H"
                    player_hit = True
                    break
                elif orientation == 'vertical' and ship_col == guess_col and ship_row <= guess_row < ship_row + size:
                    print("Congratulations! You hit a battleship!")
                    player_guesses[guess_row][guess_col] = "H"
                    ai_board[guess_row][guess_col] = "H"
                    player_hit = True
                    break

            if not player_hit:
                if player_guesses[guess_row][guess_col] in ["X", "H"]:
                    print("You guessed that one already.")
                else:
                    print("You missed my battleship!")
                    player_guesses[guess_row][guess_col] = "X"
                    ai_board[guess_row][guess_col] = "X"
                    give_hint(ai_ships, guess_row, guess_col)

            print("Player's Guesses:")
            print_board(player_guesses)
            display_statistics(player_stats)

            if all([ai_board[ship_row][ship_col] == 'H' for ship_row, ship_col, _, _ in ai_ships]):
                print("You sank all the AI's battleships! You win!")
                score = calculate_score(turn + 1, max_turns)
                print(f"Your score: {score}")
                update_leaderboard(leaderboard, player_name, score)
                print_leaderboard(leaderboard)
                break

            # AI's turn
            ai_guess_row, ai_guess_col = ai_guess(player_board, ai_previous_guesses, board_size)
            print(f"\nAI guesses: Row {ai_guess_row}, Col {ai_guess_col}")

            ai_hit = False
            for ship_row, ship_col, size, orientation in player_ships:
                if orientation == 'horizontal' and ship_row == ai_guess_row and ship_col <= ai_guess_col < ship_col + size:
                    print("AI hit one of your battleships!")
                    player_board[ai_guess_row][ai_guess_col] = "H"
                    ai_hit = True
                    break
                elif orientation == 'vertical' and ship_col == ai_guess_col and ship_row <= ai_guess_row < ship_row + size:
                    print("AI hit one of your battleships!")
                    player_board[ai_guess_row][ai_guess_col] = "H"
                    ai_hit = True
                    break

            if not ai_hit:
                print("AI missed your battleship!")
                player_board[ai_guess_row][ai_guess_col] = "X"

            print("Player's Board:")
            print_board(player_board)
            display_statistics(ai_stats)

            if all([player_board[ship_row][ship_col] == 'H' for ship_row, ship_col, _, _ in player_ships]):
                print("AI sank all your battleships! You lose!")
                break

            if turn == max_turns - 1:
                print("Game Over. The remaining AI battleships were at:")
                for ship_row, ship_col, size, orientation in ai_ships:
                    print(f"Row: {ship_row}, Col: {ship_col}")

        # Ask if the player wants to play again
        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
