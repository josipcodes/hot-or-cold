import random
from simple_term_menu import TerminalMenu
from statements import (
    LAVA_STATEMENTS,
    HOT_STATEMENTS,
    WARMER_STATEMENTS,
    FIRST_GUESS_STATEMENTS,
    COLDER_STATEMENTS,
    SAME_DIFFERENCE_STATEMENTS
    )

# Copied from Love sandwiches project
import gspread
from google.oauth2.service_account import Credentials

# Copied from Love sandwiches project
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Copied from Love sandwiches project and adjusted with naming
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("hot-or-cold-scoreboard")


def continue_playing():
    check = True
    while check:
        user_input = input("Wanna play again? (y/n) ")
        if user_input.lower() == "y":
            difficulty_menu()
            check = False
        elif user_input.lower() == "n":
            quit_game()
            check = False
        else:
            print(f"You have entered '{user_input}'.")
            print("This is not a valid command.")
            print("Please enter a valid command. \n")


def print_scoreboard(game_mode, flag):
    """
    Function pulls top 10 results depending on the difficulty played:
    Function collects values from 2 columns.
    Values are zipped together and sorted by the int in second column.
    Results are unpacked from a tuple and printed out aligned.
    If there are less than 10 results available,
    only available results are printed.
    """
    worksheet = SHEET.worksheet(game_mode)
    columns = []
    score = []
    for ind in range(1, 3):
        column = worksheet.col_values(ind)
        columns.append(column[1:])
    for username, guess in zip(columns[0], columns[1]):
        score.append((username, int(guess)))
    score.sort(key=lambda tup: tup[1])
    position = 0
    print()
    print(f"{'Position' : <10} {'Username' : ^27} {'Result' : >10}")
    for item in score[:10]:
        position += 1
        position_string = str(position) + '.'
        username, result = item
        print(f"{position_string : >5} {username : ^35} {result : >4}")
    print()
    if flag:
        continue_playing()


def scoreboard_preference(game_mode):  # review function naming
    """
    Functions checks user's preference to add their name to the scoreboard.
    Function obtains user's validated username,
    pushes it along with the amount of guesses to
    the relevant worksheet depending on the difficulty played.
    Function calls print_scoreboard().
    Alternatively, function thanks user for playing.
    Username validation - length of 15 characters,
    accepts all characters.
    """
    data = []
    check = True
    while check:
        scoreboard_confirm = input(
            "Want to see if you make it onto the leaderboard? (y/n) "
        )
        print()
        if scoreboard_confirm.lower() == "y":
            username_check = False
            while username_check is False:
                username = input("Enter a preferred username: ")
                if len(username) > 15:
                    print()
                    print("Username can only be 15 characters long. \n")
                else:
                    username_check = True
                    data.append(username)
                    data.append(len(player_guesses) + 1)
                    print()
                    print(f"Hi {username}, let's see " \
                        "if you've scored a position on the leaderboard...")
                    worksheet = SHEET.worksheet(game_mode)
                    worksheet.append_row(data)
                    print_scoreboard(game_mode, True)
                    check = False
        elif scoreboard_confirm.lower() == "n":
            print("Not a competitive one, eh?")
            print("That's ok, thank you for playing! \n")
            continue_playing()
            check = False
        else:
            print(f"You have entered '{scoreboard_confirm}'.")
            print("This is not a valid command.")
            print("Please enter a valid command. \n")


def check_if_won(random_number, player_choice, game_mode, difficulty):
    """
    Function compares player's guess with the computer's choice.
    If the choice is correct, player won:
    Function informs the player - wording depends on the guess volume.
    If the guess is wrong, check_choice function is called.
    """
    if random_number == player_choice:
        if len(player_guesses) != 0:
            win_statement = "attempts"
        else:
            win_statement = "attempt"
        print("You won!")
        print(f"It took you {len(player_guesses) + 1} {win_statement}.\n")
        scoreboard_preference(game_mode)
        return True
    elif player_choice is None:
        pass
        return False
    else:
        check_choice(random_number, player_choice, difficulty)
        return False


def check_choice(random_number, player_choice, difficulty):
    """
    Function calculates min and max between random_number and player_choice.
    Function calculates the difference between the bigger and smaller number.
    Difference is appended to player_guesses.
    check_difference function is called.
    """
    difference = 0
    smaller_number = min(random_number, player_choice)
    bigger_number = max(random_number, player_choice)
    difference = bigger_number - smaller_number
    player_guesses.append(difference)
    check_difference(player_guesses, difficulty)


def check_difference(player_guesses, difficulty):
    """
    Function checks player's guesses.
    If it's player's first guess, confirms it's not right.
    If the last two guesses player made are equal length away from the result,
    player is informed they haven't guessed the number.
    If the last guess is worse than the previous one, player is informed.
    If the last guess is better than the previous one, player is informed.
    If the guess is within 10% of the random_number, player is informed.
    #need to add a note regarding multiple statements.
    """
    if player_guesses[-1] <= difficulty / 20:
        statement_index = random.randint(0, 2)
        print(f"{LAVA_STATEMENTS[statement_index]}")
    elif player_guesses[-1] <= difficulty / 10:
        statement_index = random.randint(0, 2)
        print(f"{HOT_STATEMENTS[statement_index]}")
    elif len(player_guesses) == 1:
        statement_index = random.randint(0, 2)
        print(f"{FIRST_GUESS_STATEMENTS[statement_index]}")
    else:
        if player_guesses[-2] < player_guesses[-1]:
            statement_index = random.randint(0, 2)
            print(f"{COLDER_STATEMENTS[statement_index]}")
        elif player_guesses[-2] == player_guesses[-1]:
            statement_index = random.randint(0, 3)
            print(f"{SAME_DIFFERENCE_STATEMENTS[statement_index]}")
        else:
            statement_index = random.randint(0, 2)
            print(f"{WARMER_STATEMENTS[statement_index]}")


player_guesses = []



def run_game(game_mode):
    """
    Function takes the difficulty level chosen and adjust parameters.
    It obtains a pseudo-random number between 1 and difficulty int.
    It asks for input from user as long as user doesn't guess the number.
    Once input is received, validate_input is called.
    When validation result is received back, 
    input is converted into an integer and check_if_won is called.

    """
    # difficulty = ""
    if game_mode == "beginner":
        difficulty = 10
    elif game_mode == "intermediate":
        difficulty = 100
    else:
        difficulty = 1000
    random_number = random.randint(1, difficulty)
    print(f"You need to guess a number between 1 and {difficulty}.")
    print(random_number)  # todo: delete later
    player_choice = None
    validation = False
    while validation is False:
        player_choice = input("Your guess: ")
        if validate_input(player_choice, difficulty):
            player_choice = int(player_choice)
            validation = check_if_won(random_number, player_choice, game_mode, difficulty)


def validate_input(player_choice, difficulty):
    """
    Function validates user's input by checking if int.
    If not int, user is notified.
    If choice is outside of parameters, user is notified.
    If the choice is valid, bool True is returned.
    """
    try:
        player_choice = int(player_choice)
    except ValueError:
        print(f"You have entered '{player_choice}' instead of a number.")
        print("Please try again. \n")
        return False
    else:
        if int(player_choice) in range(1, difficulty + 1):
            return True
        else:
            print(
                "Hold on, Katy Perry, " \
                f"you're guessing a number between 1 and {difficulty}.\n"
                )
            return False


# at the moment copied from simple term menu, needs review
def main():
    """
    Function creates a main menu.
    """
    print(" __    __            _                     "
            "                _        _")
    print("|  |  |  |   ___    | |       ___    _  _  "
            "  ___    ___   | |      | |")
    print("|  |__|  |  / _ \  |   |     / _ \  | |/ | "
        " / __\  / _ \  | |    __| |")
    print("|   __   | | | | |  | |     | | | | |  _/  "
        " | |   | | | | | |   / _  |")
    print("|  |  |  | | |_| |  | |_    | |_| | | |    "
        " | |__ | |_| | | |_ | |_| |")
    print("|__|  |__|  \___/   |___|    \___/  |_|    "
        " \___/  \___/  |___| \___/")
    print()  
    print("Welcome, stranger! Choose an option below. " 
        "All of them are bad, really. \n")
     
    # Main menu options.
    main_options = [
        "[1] New Game",
        "[2] About",
        "[3] Leaderboard",
        "[4] Quit"]

    main_menu = TerminalMenu(
        main_options,
        # title = "Hot or Cold"
    )

    user_choice = None

    # main_menu_style = ("bg_red", "fg_yellow") #todo: need to check

    while True:
        current_display = main_menu.show()
        user_choice = main_options[current_display]

        if user_choice == "[1] New Game":
            difficulty_menu()
            return False 
        elif user_choice == "[2] About":
            about_info()
        elif user_choice == "[3] Leaderboard":
            leaderboard_info()
        elif user_choice == "[4] Quit":
            quit_game()
            return False


def difficulty_menu():
    # Sub-menu options.
    difficulty_options = [
        "[1] Beginner",
        "[2] Intermediate",
        "[3] Expert",
        "[4] Go back"
    ]

    print()
    print("Choose a difficulty level, I dare you. \n")

    difficulty_menu = TerminalMenu(
        difficulty_options,
    )

    current_display = difficulty_menu.show()
    user_choice = difficulty_options[current_display]

    if user_choice == "[4] Go back":
        main()
    else:
        run_game(user_choice.lower()[4:])


def about_info():
    print(
        "This game was created for educational purposes " \
        "only as a part of the course with Code Institute. \n"
    )
    print(
            "The objective of the game is to guess the correct number. " \
        "The player can choose the difficulty, and as a result " \
        "the player will have to guess a number between " \
        "1-10, 1-100 or 1-1000. \n"
    )
    print(
        "Unlike the usual guessing games, this one won't help " \
        "the player by saying if the number is higher or lower. " \
        "Worry not, the player will be told if their number is... " \
        "Well, hot! \n"
    )
    return_option()


def leaderboard_info():
    """
    Function generates a sub-menu to choose which leaderboard to show.
    Function calls print_scoreboard() once difficulty chosen,
    or main() if user chooses to go back a step.

    """
    # Sub-menu options.
    leaderboard_options = [
        "[1] Beginner",
        "[2] Intermediate",
        "[3] Expert",
        "[4] Go back"
        ]

    print("Choose which leaderboard you wish to take a sneak peak into.\n")

    leaderboard_menu = TerminalMenu(
        leaderboard_options,
        title = "Leadeboard"
    )

    current_display = leaderboard_menu.show()
    user_choice = leaderboard_options[current_display]

    if user_choice == "[4] Go back":
        main()
    else:
        print(f"{user_choice[4:]} leaderboard:\n")
        print_scoreboard(user_choice.lower()[4:], False)


def return_option():
    return_option = [
        "[r] Go back"
        ]
    return_menu = TerminalMenu(
        return_option
    )
    current_display = return_menu.show()
    user_choice = return_option[current_display]
    if user_choice == return_option[current_display]:
        main()

def quit_game():
    print("Thank you for playing Hot or Cold. \n")
    print("Hope to see you soon. \n")


main()