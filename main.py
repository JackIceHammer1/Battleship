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
    ship_names = ["Destroyer", "Submarine", "Cruiser", "Battleship", "Carrier"]
    for size, name in zip(ship_sizes[:num_ships], ship_names[:num_ships]):
        while True:
            orientation = random.choice(['horizontal', 'vertical'])
            row, col = random_row(board), random_col(board)
            if can_place_ship(board, row, col, size, orientation):
                ships.append((row, col, size, orientation, name, size))  # Added size for multiple hits
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
    closest_distance = min(get_distance(guess_row, guess_col, ship_row, ship_col) for ship_row, ship_col, _, _, _, _ in ships)
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
    ship_names = ["Destroyer", "Submarine", "Cruiser", "Battleship", "Carrier"]
    ships = []
    for size, name in zip(ship_sizes[:num_ships], ship_names[:num_ships]):
        while True:
            print(f"Place your {name} of size {size}.")
            row = int(input(f"Enter starting row (0-{len(board) - 1}): "))
            col = int(input(f"Enter starting col (0-{len(board[0]) - 1}): "))
            orientation = input("Enter orientation (horizontal/vertical): ").lower()
            if can_place_ship(board, row, col, size, orientation):
                ships.append((row, col, size, orientation, name, size))  # Added size for multiple hits
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

def log_move(log, player, row, col, result):
    log.append(f"{player} guessed row {row}, column {col} - {result}")

def display_log(log):
    print("\nGame Log:")
    for entry in log:
        print(entry)

def use_power_up(board, power_up):
    if power_up == 'reveal':
        reveal_board(board)
    elif power_up == 'extra_turn':
        return True
    return False

def reveal_board(board):
    print("Power-up activated: Reveal part of the board!")
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == "S":
                board[row][col] = "R"  # Reveal ships

def choose_board_size():
    while True:
        size = input("Enter board size (minimum 5): ")
        if size.isdigit() and int(size) >= 5:
            return int(size)
        else:
            print("Invalid size. Please enter a number 5 or greater.")

def choose_game_mode():
    while True:
        mode = input("Select game mode (quick, classic): ").lower()
        if mode in ['quick', 'classic']:
            return mode
        else:
            print("Invalid game mode. Please enter 'quick' or 'classic'.")

def update_player_stats(stats, won):
    stats['games_played'] += 1
    if won:
        stats['games_won'] += 1
    else:
        stats['games_lost'] += 1

def display_player_stats(stats):
    print(f"Games Played: {stats['games_played']}, Games Won: {stats['games_won']}, Games Lost: {stats['games_lost']}")


def main():
    leaderboard = []
    game_log = []

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

        # Initialize power-ups
        player_power_ups = ['reveal', 'extra_turn']
        ai_power_ups = ['reveal', 'extra_turn']

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
            
            power_up_used = False
            if player_power_ups:
                use_power = input("Do you want to use a power-up? (yes/no): ").lower()
                if use_power == 'yes':
                    power_up = input(f"Choose a power-up {player_power_ups}: ").lower()
                    if power_up in player_power_ups:
                        power_up_used = use_power_up(player_guesses, power_up)
                        player_power_ups.remove(power_up)

            player_hit = False
            for ship_row, ship_col, size, orientation, name, remaining in ai_ships:
                if orientation == 'horizontal' and ship_row == guess_row and ship_col <= guess_col < ship_col + size:
                    print(f"Congratulations! You hit the {name}!")
                    player_guesses[guess_row][guess_col] = "H"
                    ai_board[guess_row][guess_col] = "H"
                    player_hit = True
                    remaining -= 1
                    if remaining == 0:
                        print(f"You sank the {name}!")
                    break
                elif orientation == 'vertical' and ship_col == guess_col and ship_row <= guess_row < ship_row + size:
                    print(f"Congratulations! You hit the {name}!")
                    player_guesses[guess_row][guess_col] = "H"
                    ai_board[guess_row][guess_col] = "H"
                    player_hit = True
                    remaining -= 1
                    if remaining == 0:
                        print(f"You sank the {name}!")
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
            track_statistics(player_stats, player_hit)
            display_statistics(player_stats)
            log_move(game_log, player_name, guess_row, guess_col, "Hit" if player_hit else "Miss")

            if all([ai_board[ship_row][ship_col] == 'H' for ship_row, ship_col, _, _, _, _ in ai_ships]):
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
            for ship_row, ship_col, size, orientation, name, remaining in player_ships:
                if orientation == 'horizontal' and ship_row == ai_guess_row and ship_col <= ai_guess_col < ship_col + size:
                    print(f"AI hit your {name}!")
                    player_board[ai_guess_row][ai_guess_col] = "H"
                    ai_hit = True
                    remaining -= 1
                    if remaining == 0:
                        print(f"AI sank your {name}!")
                    break
                elif orientation == 'vertical' and ship_col == ai_guess_col and ship_row <= ai_guess_row < ship_row + size:
                    print(f"AI hit your {name}!")
                    player_board[ai_guess_row][ai_guess_col] = "H"
                    ai_hit = True
                    remaining -= 1
                    if remaining == 0:
                        print(f"AI sank your {name}!")
                    break

            if not ai_hit:
                print("AI missed your battleship!")
                player_board[ai_guess_row][ai_guess_col] = "X"

            print("Player's Board:")
            print_board(player_board)
            track_statistics(ai_stats, ai_hit)
            display_statistics(ai_stats)
            log_move(game_log, "AI", ai_guess_row, ai_guess_col, "Hit" if ai_hit else "Miss")

            if all([player_board[ship_row][ship_col] == 'H' for ship_row, ship_col, _, _, _, _ in player_ships]):
                print("AI sank all your battleships! You lose!")
                break

            if turn == max_turns - 1:
                print("Game Over. The remaining AI battleships were at:")
                for ship_row, ship_col, size, orientation, name, _ in ai_ships:
                    print(f"Row: {ship_row}, Col: {ship_col}")

        # Display game log
        display_log(game_log)

        # Ask if the player wants to play again
        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
