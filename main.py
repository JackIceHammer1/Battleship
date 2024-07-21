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

def save_leaderboard(leaderboard, filename):
    with open(filename, 'w') as file:
        for player, score in leaderboard:
            file.write(f"{player}: {score}\n")

def load_leaderboard(filename):
    leaderboard = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                player, score = line.strip().split(': ')
                leaderboard.append((player, int(score)))
    except FileNotFoundError:
        print("No saved leaderboard found.")
    return leaderboard

def display_hint(ai_ships, guess_row, guess_col):
    nearby_ships = []
    for row, col, size, orientation, name, remaining_size in ai_ships:
        if orientation == 'horizontal':
            if row == guess_row and col <= guess_col < col + size:
                nearby_ships.append(name)
        elif orientation == 'vertical':
            if col == guess_col and row <= guess_row < row + size:
                nearby_ships.append(name)
    if nearby_ships:
        print(f"Hint: You are close to {', '.join(nearby_ships)}.")
    else:
        print("Hint: No ships nearby.")

def activate_shield(board, ships):
    print("Power-up activated: Shield a part of your board!")
    for _ in range(3):  # Shield 3 random spots
        row, col = random_row(board), random_col(board)
        board[row][col] = "P"  # P for Protected
        print(f"Protected a spot at ({row}, {col})!")
        for i, (r, c, size, orientation, name, remaining_size) in enumerate(ships):
            if orientation == 'horizontal' and r == row and c <= col < c + size:
                ships[i] = (r, c, size, orientation, name, remaining_size)
            elif orientation == 'vertical' and c == col and r <= row < r + size:
                ships[i] = (r, c, size, orientation, name, remaining_size)

def power_up_shield(board, player_ships, ai_ships, power_up_choice):
    if power_up_choice == 'shield':
        activate_shield(board, player_ships)
        return False
    return False

def player_choose_power_up():
    power_ups = ['reveal', 'extra_turn', 'bomb', 'shield']
    print("Choose a power-up: ")
    for i, power_up in enumerate(power_ups, 1):
        print(f"{i}. {power_up}")
    choice = int(input("Enter the number of your choice: "))
    return power_ups[choice - 1]

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
    elif power_up_choice == 'shield':
        power_up_shield(board, player_ships, ai_ships, power_up_choice)
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

def log_move(game_log, player_name, guess_row, guess_col, result):
    game_log.append({'player': player_name, 'row': guess_row, 'col': guess_col, 'result': result})

def display_log(game_log):
    print("Game Log:")
    for move in game_log:
        print(f"{move['player']} guessed ({move['row']}, {move['col']}) - {move['result']}")

def print_instructions():
    print("Welcome to Battleship!")
    print("Instructions:")
    print("1. Place your ships on the board.")
    print("2. Take turns guessing the locations of the opponent's ships.")
    print("3. Use power-ups to gain advantages.")
    print("4. The game ends when all ships of one player are sunk.")
    print("5. Try to sink all opponent's ships before they sink yours.")

def save_scoreboard(scoreboard, filename):
    with open(filename, 'w') as file:
        for player, score in scoreboard:
            file.write(f"{player}: {score}\n")

def load_scoreboard(filename):
    scoreboard = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                player, score = line.strip().split(': ')
                scoreboard.append((player, int(score)))
    except FileNotFoundError:
        print("No saved scoreboard found.")
    return scoreboard

def display_scoreboard(scoreboard):
    print("Scoreboard:")
    for player, score in scoreboard:
        print(f"{player}: {score}")

def random_row(board):
    return random.randint(0, len(board) - 1)

def random_col(board):
    return random.randint(0, len(board) - 1)

def reveal_board(board):
    print("Revealing the board:")
    for row in board:
        print(" ".join(row))

def player_place_ships(board, num_ships):
    ships = []
    for _ in range(num_ships):
        while True:
            try:
                row = int(input("Enter the starting row for your ship (0-4): "))
                col = int(input("Enter the starting column for your ship (0-4): "))
                size = int(input("Enter the size of your ship (1-3): "))
                orientation = input("Enter orientation (horizontal/vertical): ").strip().lower()
                if orientation not in ['horizontal', 'vertical']:
                    raise ValueError("Invalid orientation.")
                if orientation == 'horizontal' and col + size > len(board):
                    raise ValueError("Ship extends beyond board.")
                if orientation == 'vertical' and row + size > len(board):
                    raise ValueError("Ship extends beyond board.")
                if orientation == 'horizontal':
                    for c in range(col, col + size):
                        if board[row][c] == "S":
                            raise ValueError("Ship overlaps with another ship.")
                if orientation == 'vertical':
                    for r in range(row, row + size):
                        if board[r][col] == "S":
                            raise ValueError("Ship overlaps with another ship.")
                break
            except ValueError as e:
                print(e)
        if orientation == 'horizontal':
            for c in range(col, col + size):
                board[row][c] = "S"
        else:
            for r in range(row, row + size):
                board[r][col] = "S"
        ships.append((row, col, size, orientation, f"Ship{_+1}", size))
    return ships

def track_statistics(stats_dict, hit):
    if hit:
        stats_dict['hits'] += 1
    else:
        stats_dict['misses'] += 1

def display_statistics(stats_dict):
    print(f"Hits: {stats_dict['hits']}")
    print(f"Misses: {stats_dict['misses']}")
    print(f"Remaining Ships: {stats_dict['remaining_ships']}")

def calculate_score(turns, max_turns):
    return max(100 - (turns - 1) * 10, 0)

def update_leaderboard(leaderboard, player_name, score):
    found = False
    for i, (player, old_score) in enumerate(leaderboard):
        if player == player_name:
            leaderboard[i] = (player_name, max(score, old_score))
            found = True
            break
    if not found:
        leaderboard.append((player_name, score))

def update_scoreboard(scoreboard, player_name, score):
    found = False
    for i, (player, old_score) in enumerate(scoreboard):
        if player == player_name:
            scoreboard[i] = (player_name, max(score, old_score))
            found = True
            break
    if not found:
        scoreboard.append((player_name, score))

def save_game(state):
    filename = input("Enter filename to save the game: ")
    save_game_state(filename, state)
    print("Game saved.")

def load_game():
    filename = input("Enter filename to load the game: ")
    state = load_game_state(filename)
    if state:
        print("Game loaded.")
    return state

def advanced_ai_guess(board_size, previous_guesses, hits):
    # Use a simple strategy to prioritize previously hit locations
    if hits:
        last_hit = hits[-1]
        # Check adjacent cells
        adjacent_cells = [
            (last_hit[0] - 1, last_hit[1]), 
            (last_hit[0] + 1, last_hit[1]), 
            (last_hit[0], last_hit[1] - 1), 
            (last_hit[0], last_hit[1] + 1)
        ]
        # Filter out cells that are out of bounds or already guessed
        adjacent_cells = [(r, c) for r, c in adjacent_cells if 0 <= r < board_size and 0 <= c < board_size and (r, c) not in previous_guesses]
        if adjacent_cells:
            return random.choice(adjacent_cells)
    # If no adjacent cells or no hits yet, fall back to random guessing
    return get_ai_guess(board_size, previous_guesses)

def update_ships_board(board, ships):
    for ship in ships:
        row, col, size, orientation, _, _ = ship
        if orientation == 'horizontal':
            for c in range(col, col + size):
                board[row][c] = "S"
        else:
            for r in range(row, row + size):
                board[r][col] = "S"

def display_ship_info(ships):
    print("Ship Information:")
    for ship in ships:
        row, col, size, orientation, name, remaining_size = ship
        orientation_str = "Horizontal" if orientation == 'horizontal' else "Vertical"
        print(f"{name}: Start({row}, {col}), Size: {size}, Orientation: {orientation_str}, Remaining: {remaining_size}")

def deploy_power_up(board, power_up_type, row, col):
    if power_up_type == 'radar':
        # Show all ship locations for one turn
        print("Radar Power-Up Activated!")
        reveal_board(board)
    elif power_up_type == 'airstrike':
        # Randomly sink a ship on the board
        print("Airstrike Power-Up Activated!")
        for r in range(len(board)):
            for c in range(len(board)):
                if board[r][c] == "S":
                    board[r][c] = "X"  # Sink the ship
                    return
    elif power_up_type == 'missile':
        # Remove a ship from the opponent's board
        print("Missile Power-Up Activated!")
        row = random_row(len(board))
        col = random_col(len(board))
        if board[row][col] == "S":
            board[row][col] = "X"

def check_achievements(player_stats):
    achievements = []
    if player_stats['games_won'] >= 10:
        achievements.append("Victory Veteran: 10 wins")
    if player_stats['hit_accuracy'] >= 80:
        achievements.append("Sharp Shooter: 80% accuracy")
    return achievements

def award_rewards(achievements):
    for achievement in achievements:
        print(f"Congratulations! You've earned the achievement: {achievement}")

def update_player_stats(player_stats, won_game):
    player_stats['games_played'] += 1
    if won_game:
        player_stats['games_won'] += 1
    else:
        player_stats['games_lost'] += 1
    player_stats['hit_accuracy'] = (player_stats['hits'] / (player_stats['hits'] + player_stats['misses'])) * 100 if (player_stats['hits'] + player_stats['misses']) > 0 else 0

def save_game_state(filename, state):
    with open(filename, 'w') as file:
        for item in state:
            file.write(f"{item}\n")

def load_game_state(filename):
    try:
        with open(filename, 'r') as file:
            state = [line.strip() for line in file]
            return state
    except FileNotFoundError:
        print("No saved game found.")
        return None

def display_game_statistics(player_stats):
    print(f"Games Played: {player_stats['games_played']}")
    print(f"Games Won: {player_stats['games_won']}")
    print(f"Games Lost: {player_stats['games_lost']}")
    print(f"Hit Accuracy: {player_stats['hit_accuracy']:.2f}%")

def log_move(game_log, player_name, row, col, result):
    game_log.append(f"{player_name} guessed ({row}, {col}): {result}")

def display_log(game_log):
    print("Game Log:")
    for entry in game_log:
        print(entry)

def get_ai_guess(board_size, previous_guesses):
    row, col = random_row(board_size), random_col(board_size)
    while (row, col) in previous_guesses:
        row, col = random_row(board_size), random_col(board_size)
    return row, col

def setup_multiplayer():
    print("Setting up multiplayer mode...")
    player1_name = input("Enter Player 1's name: ")
    player2_name = input("Enter Player 2's name: ")
    return player1_name, player2_name

def multiplayer_turn(player_name, board, ships):
    print(f"{player_name}'s Turn")
    print_board(board)
    guess_row = int(input(f"Guess Row (0-{len(board) - 1}): "))
    guess_col = int(input(f"Guess Col (0-{len(board) - 1}): "))
    if board[guess_row][guess_col] == "S":
        print("Hit!")
        board[guess_row][guess_col] = "H"
        for i, (row, col, size, orientation, name, remaining_size) in enumerate(ships):
            if orientation == 'horizontal' and row == guess_row and col <= guess_col < col + size:
                ships[i] = (row, col, size, orientation, name, remaining_size - 1)
            elif orientation == 'vertical' and col == guess_col and row <= guess_row < row + size:
                ships[i] = (row, col, size, orientation, name, remaining_size - 1)
        if all(remaining_size == 0 for _, _, _, _, _, remaining_size in ships):
            print(f"{player_name} sank all the ships!")
            return True
    else:
        print("Miss.")
        board[guess_row][guess_col] = "X"
    return False

def multiplayer_game():
    player1_name, player2_name = setup_multiplayer()
    board_size = 10
    num_ships = 5
    player1_board = [["O"] * board_size for _ in range(board_size)]
    player2_board = [["O"] * board_size for _ in range(board_size)]
    player1_ships = place_ships(player1_board, num_ships)
    player2_ships = place_ships(player2_board, num_ships)
    
    while True:
        if multiplayer_turn(player1_name, player2_board, player2_ships):
            print(f"{player1_name} wins!")
            break
        if multiplayer_turn(player2_name, player1_board, player1_ships):
            print(f"{player2_name} wins!")
            break

def customize_ships():
    print("Customize your ships:")
    ships = []
    while True:
        name = input("Enter ship name: ")
        size = int(input(f"Enter size of {name}: "))
        orientation = input(f"Enter orientation for {name} (horizontal/vertical): ").strip().lower()
        row = int(input(f"Enter starting row for {name}: "))
        col = int(input(f"Enter starting column for {name}: "))
        ships.append((row, col, size, orientation, name, size))
        more = input("Add another ship? (yes/no): ").strip().lower()
        if more == 'no':
            break
    return ships

def place_custom_ships(board, ships):
    for ship in ships:
        row, col, size, orientation, _, _ = ship
        if orientation == 'horizontal':
            for c in range(col, col + size):
                board[row][c] = "S"
        else:
            for r in range(row, row + size):
                board[r][col] = "S"

def advanced_score_calculation(turns, max_turns, accuracy):
    base_score = max_turns - turns
    accuracy_bonus = accuracy / 10
    return base_score + accuracy_bonus

def calculate_advanced_score(turns, max_turns, hit_accuracy):
    return advanced_score_calculation(turns, max_turns, hit_accuracy)

def reward_player(player_name, score):
    print(f"{player_name} earned a new reward!")
    if score >= 100:
        print("Reward: Elite Commander")
    elif score >= 50:
        print("Reward: Tactical Genius")
    else:
        print("Reward: Strategic Newbie")

def update_player_rewards(player_stats):
    rewards = []
    if player_stats['games_won'] >= 10:
        rewards.append("Veteran")
    if player_stats['hit_accuracy'] >= 80:
        rewards.append("Sharp Shooter")
    return rewards

def save_game_history(filename, game_history):
    with open(filename, 'a') as file:
        for entry in game_history:
            file.write(f"{entry}\n")

def load_game_history(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        return []

def deploy_power_up_choice():
    print("Power-Ups available:")
    print("1. Radar - Reveals a 3x3 area")
    print("2. Shield - Protects a 2x2 area for 3 turns")
    print("3. Double Shot - Shoot twice in one turn")
    choice = input("Choose a power-up (1/2/3): ").strip()
    return choice

def use_power_up(board, power_up_choice, turn_stats):
    if power_up_choice == '1':
        reveal_area(board)
    elif power_up_choice == '2':
        shield_area(board, turn_stats)
    elif power_up_choice == '3':
        double_shot(board)
        
def reveal_area(board):
    row = int(input("Enter starting row for Radar (0-7): "))
    col = int(input("Enter starting column for Radar (0-7): "))
    print("Revealed Area:")
    for r in range(row, row + 3):
        for c in range(col, col + 3):
            if r < len(board) and c < len(board[0]):
                print(board[r][c], end=" ")
            else:
                print(" ", end=" ")
        print()

def shield_area(board, turn_stats):
    row = int(input("Enter starting row for Shield (0-8): "))
    col = int(input("Enter starting column for Shield (0-8): "))
    turn_stats['shield'] = {'row': row, 'col': col, 'turns_remaining': 3}
    print(f"Shield deployed at ({row}, {col})")

def double_shot(board):
    print("Double Shot activated!")
    for _ in range(2):
        guess_row = int(input(f"Guess Row (0-{len(board) - 1}): "))
        guess_col = int(input(f"Guess Col (0-{len(board) - 1}): "))
        if board[guess_row][guess_col] == "S":
            print("Hit!")
            board[guess_row][guess_col] = "H"
        else:
            print("Miss.")
            board[guess_row][guess_col] = "X"

def ai_guess_smart(board_size, previous_guesses):
    import random
    guess = random.choice([(row, col) for row in range(board_size) for col in range(board_size) if (row, col) not in previous_guesses])
    return guess

def ai_use_power_up(board, power_up_choice):
    if power_up_choice == '1':
        reveal_area(board)
    elif power_up_choice == '2':
        shield_area(board, turn_stats)
    elif power_up_choice == '3':
        double_shot(board)

def apply_fog_of_war(board, revealed_positions):
    fogged_board = [["?" if (row, col) not in revealed_positions else board[row][col] for col in range(len(board[0]))] for row in range(len(board))]
    return fogged_board

def reveal_position(revealed_positions, row, col):
    revealed_positions.add((row, col))

def repair_ship(board, ships):
    ship_to_repair = input("Enter the name of the ship you want to repair: ").strip().lower()
    for i, (row, col, size, orientation, name, remaining_size) in enumerate(ships):
        if name.lower() == ship_to_repair and remaining_size < size:
            if orientation == 'horizontal':
                for c in range(col, col + size):
                    if board[row][c] == 'H':
                        board[row][c] = 'S'
                        ships[i] = (row, col, size, orientation, name, remaining_size + 1)
                        print(f"{name} repaired at ({row}, {c}).")
                        return
            elif orientation == 'vertical':
                for r in range(row, row + size):
                    if board[r][col] == 'H':
                        board[r][col] = 'S'
                        ships[i] = (row, col, size, orientation, name, remaining_size + 1)
                        print(f"{name} repaired at ({r}, {col}).")
                        return
    print("Repair failed. Either the ship is not damaged or the name is incorrect.")

import random

def random_event(board, ships, event_stats):
    event = random.choice(['storm', 'mutiny', 'sea_monster'])
    if event == 'storm':
        print("A storm has damaged one of your ships!")
        damage_ship(board, ships)
    elif event == 'mutiny':
        print("A mutiny has occurred! One turn lost.")
        event_stats['turns_lost'] += 1
    elif event == 'sea_monster':
        print("A sea monster has attacked! One ship lost.")
        destroy_ship(board, ships)
        
def damage_ship(board, ships):
    ship = random.choice(ships)
    if ship[3] == 'horizontal':
        col = random.randint(ship[1], ship[1] + ship[2] - 1)
        board[ship[0]][col] = 'H'
    else:
        row = random.randint(ship[0], ship[0] + ship[2] - 1)
        board[row][ship[1]] = 'H'
    print(f"{ship[4]} was damaged.")
    
def destroy_ship(board, ships):
    ship = random.choice(ships)
    for i in range(ship[2]):
        if ship[3] == 'horizontal':
            board[ship[0]][ship[1] + i] = 'H'
        else:
            board[ship[0] + i][ship[1]] = 'H'
    print(f"{ship[4]} was destroyed.")
    ships.remove(ship)

def apply_consecutive_hit_bonus(player_stats_dict):
    if player_stats_dict['consecutive_hits'] >= 3:
        print("Bonus Applied: Extra turn for 3 consecutive hits!")
        player_stats_dict['bonus_turns'] += 1

def adjust_ai_difficulty(ai_stats_dict, difficulty):
    if difficulty == "hard":
        ai_stats_dict['hit_probability'] += 0.1
    elif difficulty == "easy":
        ai_stats_dict['hit_probability'] -= 0.1

def check_achievements(player_stats_dict):
    achievements = []
    if player_stats_dict['games_won'] >= 10:
        achievements.append("Veteran Commander")
    if player_stats_dict['hit_accuracy'] >= 0.8:
        achievements.append("Sharp Shooter")
    if player_stats_dict['games_played'] >= 20:
        achievements.append("Seasoned Sailor")
    if achievements:
        print("Achievements Unlocked:")
        for achievement in achievements:
            print(f"- {achievement}")

def update_winning_streak(player_name, win_streak, streak_board):
    if player_name in streak_board:
        if win_streak > streak_board[player_name]:
            streak_board[player_name] = win_streak
    else:
        streak_board[player_name] = win_streak

def save_streak_board(streak_board, filename):
    with open(filename, 'w') as file:
        for player, streak in streak_board.items():
            file.write(f"{player},{streak}\n")

def load_streak_board(filename):
    streak_board = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                player, streak = line.strip().split(',')
                streak_board[player] = int(streak)
    except FileNotFoundError:
        pass
    return streak_board

def display_streak_board(streak_board):
    print("\nLongest Winning Streaks:")
    for player, streak in sorted(streak_board.items(), key=lambda item: item[1], reverse=True):
        print(f"{player}: {streak} wins")

def init_chat():
    chat_log = []
    return chat_log

def add_chat_message(chat_log, player_name, message):
    chat_log.append(f"{player_name}: {message}")

def display_chat(chat_log):
    print("\nIn-Game Chat:")
    for message in chat_log:
        print(message)

def log_game_history(game_history, filename):
    with open(filename, 'a') as file:
        for entry in game_history:
            file.write(entry + "\n")

def add_game_entry(game_history, player_name, action, result):
    game_history.append(f"{player_name} - {action}: {result}")

def display_game_history(game_history):
    print("\nGame History:")
    for entry in game_history:
        print(entry)


def main():
    print_instructions()

    leaderboard = load_leaderboard("leaderboard.txt")
    streak_board = load_streak_board("streak_board.txt")
    player_stats = {'games_played': 0, 'games_won': 0, 'games_lost': 0, 'hits': 0, 'misses': 0, 'hit_accuracy': 0, 'consecutive_hits': 0, 'bonus_turns': 0}
    game_log = []
    game_history = []
    chat_log = init_chat()
    player_name = input("Enter your name: ")
    win_streak = 0

    while True:
        game_mode = input("Choose game mode (single/multiplayer/custom): ").strip().lower()

        if game_mode == 'single':
            difficulty = select_difficulty()
            board_size, num_ships, max_turns = set_parameters(difficulty)

            player_board = [["O"] * board_size for _ in range(board_size)]
            ai_board = [["O"] * board_size for _ in range(board_size)]

            player_ships = place_ships(player_board, num_ships)
            ai_ships = place_ships(ai_board, num_ships)

            player_stats_dict = {'board': player_board, 'hits': 0, 'misses': 0, 'remaining_ships': num_ships, 'consecutive_hits': 0, 'bonus_turns': 0}
            ai_stats_dict = {'board': ai_board, 'hits': 0, 'misses': 0, 'remaining_ships': num_ships, 'hit_probability': 0.5}

            previous_ai_guesses = set()
            hits = []
            revealed_positions = set()
            event_stats = {'turns_lost': 0}

            adjust_ai_difficulty(ai_stats_dict, difficulty)

            for turn in range(max_turns):
                if check_forfeit():
                    print("You have forfeited the game.")
                    update_player_stats(player_stats, False)
                    display_game_statistics(player_stats)
                    add_game_entry(game_history, player_name, "Forfeit", "Loss")
                    break

                print(f"\nTurn {turn + 1}/{max_turns}")
                print("Player Board:")
                print_board(player_board)
                print("AI Board (Fog of War):")
                fogged_ai_board = apply_fog_of_war(ai_board, revealed_positions)
                print_board(fogged_ai_board)

                guess_row = int(input(f"Guess Row (0-{board_size - 1}): "))
                guess_col = int(input(f"Guess Col (0-{board_size - 1}): "))

                if ai_board[guess_row][guess_col] == "S":
                    print("You hit a ship!")
                    ai_board[guess_row][guess_col] = "H"
                    reveal_position(revealed_positions, guess_row, guess_col)
                    hits.append((guess_row, guess_col))
                    player_stats_dict['consecutive_hits'] += 1
                    apply_consecutive_hit_bonus(player_stats_dict)

                    for i, (row, col, size, orientation, name, remaining_size) in enumerate(ai_ships):
                        if orientation == 'horizontal' and row == guess_row and col <= guess_col < col + size:
                            ai_ships[i] = (row, col, size, orientation, name, remaining_size - 1)
                        elif orientation == 'vertical' and col == guess_col and row <= guess_row < row + size:
                            ai_ships[i] = (row, col, size, orientation, name, remaining_size - 1)
                    if all(remaining_size == 0 for _, _, _, _, _, remaining_size in ai_ships):
                        print("Congratulations! You sank all the AI's ships!")
                        score = calculate_advanced_score(turn + 1, max_turns, player_stats['hit_accuracy'])
                        print(f"Your score: {score}")
                        reward_player(player_name, score)
                        update_leaderboard(leaderboard, player_name, score)
                        display_leaderboard(leaderboard)
                        save_leaderboard(leaderboard, "leaderboard.txt")
                        update_player_stats(player_stats, True)
                        display_game_statistics(player_stats)
                        update_scoreboard(scoreboard, player_name, score)
                        save_scoreboard(scoreboard, "scoreboard.txt")
                        check_achievements(player_stats_dict)
                        win_streak += 1
                        update_winning_streak(player_name, win_streak, streak_board)
                        save_streak_board(streak_board, "streak_board.txt")
                        display_streak_board(streak_board)
                        add_game_entry(game_history, player_name, "Victory", "Win")
                        log_game_history(game_history, "game_history.txt")
                        break
                    track_statistics(player_stats_dict, True)
                    log_move(game_log, player_name, guess_row, guess_col, "hit")
                else:
                    print("You missed.")
                    ai_board[guess_row][guess_col] = "X"
                    player_stats_dict['consecutive_hits'] = 0
                    track_statistics(player_stats_dict, False)
                    log_move(game_log, player_name, guess_row, guess_col, "miss")

                if player_stats_dict['bonus_turns'] > 0:
                    print("You have an extra turn!")
                    player_stats_dict['bonus_turns'] -= 1
                else:
                    deploy_power_up_choice = input("Do you want to use a power-up? (yes/no): ").strip().lower()
                    if deploy_power_up_choice == 'yes':
                        power_up_choice = deploy_power_up_choice()
                        use_power_up(ai_board, power_up_choice, player_stats_dict)

                    repair_choice = input("Do you want to repair a ship? (yes/no): ").strip().lower()
                    if repair_choice == 'yes':
                        repair_ship(player_board, player_ships)

                    ai_guess_row, ai_guess_col = ai_guess_smart(board_size, previous_ai_guesses)
                    previous_ai_guesses.add((ai_guess_row, ai_guess_col))
                    if ai_board[ai_guess_row][ai_guess_col] == "S":
                        print(f"AI hit your ship at ({ai_guess_row}, {ai_guess_col})!")
                        ai_board[ai_guess_row][ai_guess_col] = "H"
                        for i, (row, col, size, orientation, name, remaining_size) in enumerate(player_ships):
                            if orientation == 'horizontal' and row == ai_guess_row and col <= ai_guess_col < col + size:
                                player_ships[i] = (row, col, size, orientation, name, remaining_size - 1)
                            elif orientation == 'vertical' and col == ai_guess_col and row <= ai_guess_row < row + size:
                                player_ships[i] = (row, col, size, orientation, name, remaining_size - 1)
                        if all(remaining_size == 0 for _, _, _, _, _, remaining_size in player_ships):
                            print("Game over! The AI sank all your ships.")
                            update_player_stats(player_stats, False)
                            display_game_statistics(player_stats)
                            win_streak = 0
                            add_game_entry(game_history, player_name, "Defeat", "Loss")
                            log_game_history(game_history, "game_history.txt")
                            break
                        track_statistics(ai_stats_dict, True)
                        log_move(game_log, "AI", ai_guess_row, ai_guess_col, "hit")
                    else:
                        print(f"AI missed at ({ai_guess_row}, {ai_guess_col}).")
                        player_board[ai_guess_row][ai_guess_col] = "X"
                        track_statistics(ai_stats_dict, False)
                        log_move(game_log, "AI", ai_guess_row, ai_guess_col, "miss")

                    random_event_choice = input("Do you want to trigger a random event? (yes/no): ").strip().lower()
                    if random_event_choice == 'yes':
                        random_event(player_board, player_ships, event_stats)

                save_choice = input("Do you want to save the game? (yes/no): ").strip().lower()
                if save_choice == 'yes':
                    save_game("battleship_save.txt", (player_board, ai_board, player_ships, ai_ships, player_stats_dict, ai_stats_dict, previous_ai_guesses, hits, revealed_positions, event_stats, turn, game_log, player_name))

            replay_choice = input("Do you want to play again? (yes/no): ").lower()
            if replay_choice == 'no':
                break

        elif game_mode == 'multiplayer':
            chat_log = init_chat()
            multiplayer_game(chat_log)
            display_chat(chat_log)

        elif game_mode == 'custom':
            print("Customizing game settings...")
            player_board = [["O"] * board_size for _ in range(board_size)]
            ai_board = [["O"] * board_size for _ in range(board_size)]
            player_ships = customize_ships()
            place_custom_ships(player_board, player_ships)
        
        else:
            print("Invalid game mode selected.")

if __name__ == "__main__":
    main()
