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
    elif power_up == 'bomb':
        bomb_board(board)
    return False

def reveal_board(board):
    print("Power-up activated: Reveal part of the board!")
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == "S":
                board[row][col] = "R"  # Reveal ships

def bomb_board(board):
    print("Power-up activated: Bombing a part of the board!")
    for _ in range(3):  # Bomb 3 random spots
        row, col = random_row(board), random_col(board)
        if board[row][col] == "S":
            board[row][col] = "H"
            print(f"Hit a ship at ({row}, {col})!")

def update_player_stats(stats, won):
    stats['games_played'] += 1
    if won:
        stats['games_won'] += 1
    else:
        stats['games_lost'] += 1

def display_player_stats(stats):
    print(f"Games Played: {stats['games_played']}, Games Won: {stats['games_won']}, Games Lost: {stats['games_lost']}")

def check_forfeit():
    forfeit = input("Do you want to forfeit the game? (yes/no): ").lower()
    return forfeit == 'yes'

def save_stats_to_file(stats, filename):
    with open(filename, 'w') as file:
        for key, value in stats.items():
            file.write(f"{key}: {value}\n")

def load_stats_from_file(filename):
    stats = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                key, value = line.strip().split(': ')
                stats[key] = int(value)
    except FileNotFoundError:
        print("No saved stats found.")
    return stats

def choose_power_up():
    power_ups = ['reveal', 'extra_turn', 'bomb']
    print("Choose a power-up: ")
    for i, power_up in enumerate(power_ups, 1):
        print(f"{i}. {power_up}")
    choice = int(input("Enter the number of your choice: "))
    return power_ups[choice - 1]

def display_ship_status(ships):
    print("Ship Status:")
    for ship in ships:
        name, size, remaining_size = ship[4], ship[2], ship[5]
        print(f"{name}: {'X' * (size - remaining_size) + '-' * remaining_size}")

def update_scoreboard(scoreboard, player, score):
    scoreboard[player] = score

def display_scoreboard(scoreboard):
    print("Scoreboard:")
    for player, score in scoreboard.items():
        print(f"{player}: {score}")

def save_scoreboard(scoreboard, filename):
    with open(filename, 'w') as file:
        for player, score in scoreboard.items():
            file.write(f"{player}: {score}\n")

def load_scoreboard(filename):
    scoreboard = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                player, score = line.strip().split(': ')
                scoreboard[player] = int(score)
    except FileNotFoundError:
        print("No saved scoreboard found.")
    return scoreboard

def ai_choose_power_up():
    power_ups = ['reveal', 'extra_turn', 'bomb']
    return random.choice(power_ups)

def save_game_state(filename, state):
    with open(filename, 'wb') as file:
        pickle.dump(state, file)

def load_game_state(filename):
    try:
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("No saved game found.")
        return None

def apply_power_up_choice(board, player_ships, ai_ships, power_up_choice):
    if power_up_choice == 'reveal':
        reveal_board(board)
    elif power_up_choice == 'extra_turn':
        return True
    elif power_up_choice == 'bomb':
        bomb_board(board, player_ships, ai_ships)
    return False

def bomb_board(board, player_ships, ai_ships):
    print("Power-up activated: Bombing a part of the board!")
    for _ in range(3):  # Bomb 3 random spots
        row, col = random_row(board), random_col(board)
        if board[row][col] == "S":
            board[row][col] = "H"
            print(f"Hit a ship at ({row}, {col})!")
            update_ship_status(player_ships, ai_ships, row, col)

def update_ship_status(player_ships, ai_ships, row, col):
    for i, (r, c, size, orientation, name, remaining_size) in enumerate(player_ships):
        if orientation == 'horizontal' and r == row and c <= col < c + size:
            player_ships[i] = (r, c, size, orientation, name, remaining_size - 1)
        elif orientation == 'vertical' and c == col and r <= row < r + size:
            player_ships[i] = (r, c, size, orientation, name, remaining_size - 1)
    for i, (r, c, size, orientation, name, remaining_size) in enumerate(ai_ships):
        if orientation == 'horizontal' and r == row and c <= col < c + size:
            ai_ships[i] = (r, c, size, orientation, name, remaining_size - 1)
        elif orientation == 'vertical' and c == col and r <= row < r + size:
            ai_ships[i] = (r, c, size, orientation, name, remaining_size - 1)

def main():
    print_instructions()

    leaderboard = []
    player_stats = {'games_played': 0, 'games_won': 0, 'games_lost': 0}
    game_log = []
    scoreboard = load_scoreboard("scoreboard.txt")
    player_name = input("Enter your name: ")

    while True:
        difficulty = select_difficulty()
        board_size, num_ships, max_turns = set_parameters(difficulty)

        player_board = [["O"] * board_size for _ in range(board_size)]
        ai_board = [["O"] * board_size for _ in range(board_size)]

        game_mode = choose_game_mode()
        if game_mode == 'classic':
            player_ships = place_ships(player_board, num_ships)
        else:
            player_ships = player_place_ships(player_board, num_ships)
        ai_ships = place_ships(ai_board, num_ships)

        player_stats_dict = {'board': player_board, 'hits': 0, 'misses': 0, 'remaining_ships': num_ships}
        ai_stats_dict = {'board': ai_board, 'hits': 0, 'misses': 0, 'remaining_ships': num_ships}

        previous_ai_guesses = set()

        for turn in range(max_turns):
            if check_forfeit():
                print("You have forfeited the game.")
                update_player_stats(player_stats, False)
                display_player_stats(player_stats)
                break

            print(f"\nTurn {turn + 1}/{max_turns}")
            print("Player Board:")
            print_board(player_board)
            print("AI Board:")
            print_board(ai_board)

            guess_row = int(input(f"Guess Row (0-{board_size - 1}): "))
            guess_col = int(input(f"Guess Col (0-{board_size - 1}): "))
            if ai_board[guess_row][guess_col] == "S":
                print("You hit a ship!")
                ai_board[guess_row][guess_col] = "H"
                for i, (row, col, size, orientation, name, remaining_size) in enumerate(ai_ships):
                    if orientation == 'horizontal' and row == guess_row and col <= guess_col < col + size:
                        ai_ships[i] = (row, col, size, orientation, name, remaining_size - 1)
                    elif orientation == 'vertical' and col == guess_col and row <= guess_row < row + size:
                        ai_ships[i] = (row, col, size, orientation, name, remaining_size - 1)
                if all(remaining_size == 0 for _, _, _, _, _, remaining_size in ai_ships):
                    print("Congratulations! You sank all the AI's ships!")
                    score = calculate_score(turn + 1, max_turns)
                    print(f"Your score: {score}")
                    update_leaderboard(leaderboard, player_name, score)
                    display_leaderboard(leaderboard)
                    update_player_stats(player_stats, True)
                    display_player_stats(player_stats)
                    update_scoreboard(scoreboard, player_name, score)
                    save_scoreboard(scoreboard, "scoreboard.txt")
                    break
                track_statistics(player_stats_dict, True)
                log_move(game_log, player_name, guess_row, guess_col, "hit")
            else:
                print("You missed.")
                ai_board[guess_row][guess_col] = "X"
                track_statistics(player_stats_dict, False)
                log_move(game_log, player_name, guess_row, guess_col, "miss")
                give_hint(ai_ships, guess_row, guess_col)

            power_up_choice = choose_power_up()
            if apply_power_up_choice(ai_board, player_ships, ai_ships, power_up_choice):
                continue

            print("AI's turn...")
            ai_power_up_choice = ai_choose_power_up()
            if apply_power_up_choice(player_board, ai_ships, player_ships, ai_power_up_choice):
                ai_guess_row, ai_guess_col = ai_guess(player_board, previous_ai_guesses, board_size)
                if player_board[ai_guess_row][ai_guess_col] == "S":
                    print(f"AI hit your ship at ({ai_guess_row}, {ai_guess_col})!")
                    player_board[ai_guess_row][ai_guess_col] = "H"
                    for i, (row, col, size, orientation, name, remaining_size) in enumerate(player_ships):
                        if orientation == 'horizontal' and row == ai_guess_row and col <= ai_guess_col < col + size:
                            player_ships[i] = (row, col, size, orientation, name, remaining_size - 1)
                        elif orientation == 'vertical' and col == ai_guess_col and row <= ai_guess_row < row + size:
                            player_ships[i] = (row, col, size, orientation, name, remaining_size - 1)
                    if all(remaining_size == 0 for _, _, _, _, _, remaining_size in player_ships):
                        print("Game over! The AI sank all your ships.")
                        update_player_stats(player_stats, False)
                        display_player_stats(player_stats)
                        break
                    track_statistics(ai_stats_dict, True)
                    log_move(game_log, "AI", ai_guess_row, ai_guess_col, "hit")
                else:
                    print(f"AI missed at ({ai_guess_row}, {ai_guess_col}).")
                    player_board[ai_guess_row][ai_guess_col] = "X"
                    track_statistics(ai_stats_dict, False)
                    log_move(game_log, "AI", ai_guess_row, ai_guess_col, "miss")

        else:
            print("Game over! You've used all your turns.")
            update_player_stats(player_stats, False)
            display_player_stats(player_stats)

        display_statistics(player_stats_dict)
        display_log(game_log)
        display_scoreboard(scoreboard)

        save_choice = input("Do you want to save the game? (yes/no): ").lower()
        if save_choice == 'yes':
            save_game((player_board, ai_board, player_ships, ai_ships, turn, leaderboard, player_stats_dict, ai_stats_dict, previous_ai_guesses, game_log, player_name, player_stats))

        load_choice = input("Do you want to load a saved game? (yes/no): ").lower()
        if load_choice == 'yes':
            state = load_game()
            if state:
                (player_board, ai_board, player_ships, ai_ships, turn, leaderboard, player_stats_dict, ai_stats_dict, previous_ai_guesses, game_log, player_name, player_stats) = state
                continue

        replay_choice = input("Do you want to play again? (yes/no): ").lower()
        if replay_choice == 'no':
            break

if __name__ == "__main__":
    main()
