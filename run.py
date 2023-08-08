# importing random to enable randomisation
import random
# importing to assist with menu building
from simple_term_menu import TerminalMenu
# importing to delay printing
import time
# enabling text coloring
import colorama
# importing statements.py
from statements import (
    LAVA_STATEMENTS,
    HOT_STATEMENTS,
    WARMER_STATEMENTS,
    FIRST_GUESS_STATEMENTS,
    COLDER_STATEMENTS,
    SAME_DIFFERENCE_STATEMENTS
    )
# importing leaderboard.py
from leaderboard import (
    print_scoreboard,
    scoreboard_preference
    )
# importing helper functions
from helpers import (
    slow_print,
    clear,
    hello,
    bye
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
    """
    Function checks if player would like to play again,
    and calls relevant function.
    """
    # Continue options.
    continue_options = [
        "[y] Yes",
        "[n] No"
    ]

    # Continue menu.
    continue_menu = TerminalMenu(
        continue_options,
    )

    # Variable stores user's current choice within the menu.
    user_choice = None

    print("Wanna play again?")

    while True:
        current_display = continue_menu.show()
        user_choice = continue_options[current_display]
        # User navigates the menu with y/n, or arrows and Enter.
        # No validation implemented as is implicit with the menu set up.
        # If 'y', difficulty_menu() is called.
        if user_choice == "[y] Yes":
            difficulty_menu()
        # One could call main(),
        # but current solution prevents unnecessary clicks.
        # Otherwise quit_game() is called.
        elif user_choice == "[n] No":
            quit_game()
        # once choice made, returns False
        return False


def check_if_won(random_number, player_choice, game_mode, difficulty):
    """
    Function compares player's guess with the computer's choice.
    Return statements are sent to run_game() to control the flow.
    """
    # If the choice is correct, player won:
    # Function informs the player - wording depends on the guess volume.
    if random_number == player_choice:
        if len(player_guesses) != 0:
            win_statement = "attempts"
        else:
            win_statement = "attempt"
        clear()
        print("You won! 🍀")
        print(f"It took you {len(player_guesses) + 1} {win_statement}.\n")
        scoreboard_preference(
            game_mode,
            player_guesses,
            SHEET,
            continue_playing,
        )
        return True
    # If the guess is wrong, check_choice() function is called.
    else:
        check_choice(random_number, player_choice, difficulty)
        return False


def check_choice(random_number, player_choice, difficulty):
    """
    Function calculates min and max between random_number and player_choice.
    Function calculates the difference between the bigger and smaller number.
    Difference is appended to player_guesses variable.
    check_difference() function is called.
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
    Player is informed if:
    -their first guess is wrong,
    -if the last two guesses player made are equal length away from the result,
    -if the last guess is worse than the previous one,
    -if the last guess is better than the previous one,
    -if the guess is within certain percentage of the random_number.
    Wording is randomised between the available choices.
    """
    # lava_divisor and hot_divisor are set based on difficulty.
    if difficulty == 10:
        lava_divisor = 10
        hot_divisor = 5
    elif difficulty == 100:
        lava_divisor = 20
        hot_divisor = 10
    elif difficulty == 1000:
        lava_divisor = 50
        hot_divisor = 25
    # Statement is produced depending on the circumstance.
    if player_guesses[-1] <= difficulty / lava_divisor:
        statement_index = random.randint(0, 2)
        print(f"{LAVA_STATEMENTS[statement_index]}")
    elif player_guesses[-1] <= difficulty / hot_divisor:
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


# List collecting difference between random number and player's choice.
player_guesses = []


def run_game(game_mode):
    """
    Function takes the game_mode and adjusts difficulty level parameter.
    It asks for input from user as long as the user doesn't guess the number.
    Once input is received, validate_input() is called.
    When validation result is returned,
    input is converted into an integer and check_if_won() is called.
    Function prints out previous wrong guesses.
    """
    player_guesses.clear()
    clear()
    # Sets difficulty based on the game_mode
    if game_mode == "beginner":
        difficulty = 10
    elif game_mode == "intermediate":
        difficulty = 100
    else:
        difficulty = 1000
    # Pseudo-random number between 1 and difficulty int is generated.
    random_number = random.randint(1, difficulty)
    print(f"You need to guess a number between 1 and {difficulty}.")
    # Variable which takes player's choice.
    player_choice = None
    # Variable which takes player's previous choices.
    previous_choices = []
    # Validation flag, default is False.
    validation = False
    # Variable which takes player's previous choices as a str.
    previous_choices_str = ""
    # Asks for input as long as validation flag is False.
    while validation is False:
        print()
        player_choice = input("Your guess: ")
        clear()
        # If input is valid, does further actions.
        if validate_input(player_choice, difficulty):
            # converts input to int
            player_choice = int(player_choice)
            # appends the latest choice to previous_choices
            previous_choices.append(player_choice)
            # sorts previous_choices in ascending order
            previous_choices.sort()
            # for each choice, converts previous_choices to str
            previous_choices_str = ', '.join(
                [str(choice) for choice in previous_choices]
                )
            # prints previous_choices_str in yellow
            print(
                Fore.YELLOW +
                f"Your previous guesses: {previous_choices_str}"
                )
            print(Style.RESET_ALL)
            # check_if_won regulates validation.
            # If player won (True), loop is broken.
            validation = check_if_won(
                random_number,
                player_choice,
                game_mode,
                difficulty
            )


def validate_input(player_choice, difficulty):
    """
    Function validates user's input,
    by checking if it can be converted to int.
    If not int or choice is outside of parameters,
    user is notified, return False.
    If the choice is valid, bool True is returned.
    """
    # Attempt converting to an int.
    try:
        player_choice = int(player_choice)
    # Input validation, returns False if validation fails.
    except ValueError:
        print(f"You have entered '{player_choice}' instead of a number. \n")
        print(Fore.RED + "This is not a valid command.")
        print(Style.RESET_ALL)
        print("Please try again.")
        return False
    # If input can be converted to an int, check if within the parameters.
    else:
        # Returns True if choice within parameters.
        if int(player_choice) in range(1, difficulty + 1):
            return True
        # Returns False if choice outside of parameters.
        else:
            print(
                "Hold on, Katy Perry, "
                f"you're guessing a number between 1 and {difficulty}.\n"
                )
            return False


def main():
    """
    Function prints out the game name and creates a main menu.
    If user chooses 'New Game', difficulty_menu() is called.
    If user chooses 'About', about_info() is called.
    If user chooses 'Leaderboard', leaderboard_info() is called.
    If user chooses 'Quit game', quit_game() is called,
    while loop is stopped.
    """
    clear()
    # prints game name in graffity
    hello()
    print(
        "Welcome, stranger! Choose an option below. "
        "All of them are bad, really. \n"
        )

    # Main menu options.
    main_options = [
        "[1] New Game",
        "[2] About",
        "[3] Leaderboard",
        "[4] Quit"]

    # Main menu.
    main_menu = TerminalMenu(
        main_options,
    )

    # Variable stores user's current choice within the menu.
    user_choice = None

    while True:
        current_display = main_menu.show()
        user_choice = main_options[current_display]
        # 'else' avoided to prevent unvalidated choice.
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
    """
    Function generates a sub-menu to show difficulty levels available.
    If difficulty is chosen, run_game() is called,
    difficulty is passed on.
    Otherwise if user chooses to go back, function calls main().
    """
    # Sub-menu options.
    difficulty_options = [
        "[1] Beginner",
        "[2] Intermediate",
        "[3] Expert",
        "[4] Go back"
    ]

    clear()
    # prints game name in grafitti
    hello()
    print("Choose a difficulty level, I dare you. \n")

    # Difficulty menu.
    difficulty_menu = TerminalMenu(
        difficulty_options,
    )

    current_display = difficulty_menu.show()
    user_choice = difficulty_options[current_display]

    # calls main() if user wants to go back
    # user_choice is used to navigate through run_game
    # choice wording is shortened and turned to lowercase
    main() if user_choice == "[4] Go back" else run_game(
        user_choice.lower()[4:]
        )


def about_info():
    """
    Function prints out information about the game.
    Function then calls return_option()
    """
    clear()
    print(
        "This game was created for educational purposes "
        "only as a part of the course with Code Institute. \n"
    )
    print(
        "The objective of the game is to guess the correct number. "
        "The player can choose the difficulty, and as a result "
        "the player will have to guess a number between "
        "1-10, 1-100 or 1-1000. \n"
    )
    print(
        "Unlike the usual guessing games, this one won't help "
        "the player by saying if the number is higher or lower. "
        "Worry not, the player will be told if their number is... "
        "Well, hot! \n"
    )
    return_option()


def leaderboard_info():
    """
    Function generates a sub-menu to choose which leaderboard to show.
    Function calls print_scoreboard() once difficulty chosen,
    or main() if user chooses to go back a step.
    To control the flow, bool is passed to print_scoreboard().

    """
    clear()
    # Sub-menu options.
    leaderboard_options = [
        "[1] Beginner",
        "[2] Intermediate",
        "[3] Expert",
        "[4] Go back"
        ]

    print("Choose which leaderboard you wish to take a sneak peak into.\n")

    # Leaderboard menu.
    leaderboard_menu = TerminalMenu(
        leaderboard_options,
    )

    current_display = leaderboard_menu.show()
    user_choice = leaderboard_options[current_display]

    # Calls main() if user wants to go a step back.
    if user_choice == "[4] Go back":
        main()
    # Prints which leaderboard was chosen.
    # No need to use .title() due to the user_choice format.
    else:
        print(f"{user_choice[4:]} leaderboard:\n")
        # Calls print_scoreboard.
        print_scoreboard(
            user_choice.lower()[4:],
            False,
            SHEET,
            continue_playing
            )
        # Calls return_option().
        return_option()


def return_option():
    """
    Function adds an option of returning to the main menu,
    triggered by 'r' or Enter since 'r' is the default option.
    Function calls main().
    """
    # Return options.
    return_option = [
        "[r] Go back to Main Menu"
        ]

    # Return menu.
    return_menu = TerminalMenu(
        return_option
    )

    current_display = return_menu.show()
    user_choice = return_option[current_display]

    # Calls main if user_choice is to return.
    if user_choice == return_option[current_display]:
        main()


def quit_game():
    """
    Function asks for confirmation of quitting.
    If yes, prints goodbye message.
    If no, calls return_option()
    """
    clear()

    # Quit options.
    quit_options = [
        "[y] Yes",
        "[n] No"
    ]

    # Quit menu.
    quit_menu = TerminalMenu(
        quit_options,
    )

    # Variable stores user's current choice within the menu.
    user_choice = None

    hello()
    print("Are you sure you want to quit?")

    while True:
        current_display = quit_menu.show()
        user_choice = quit_options[current_display]
        # if 'y', prints a goodbye message
        if user_choice == "[y] Yes":
            clear()
            print("Thank you for playing Hot or Cold. \n")
            print("Hope to see you soon. \n")
            # prints goodbye in grafitti
            bye()
        # if 'n', calls return_option()
        elif user_choice == "[n] No":
            clear()
            # prints game name in graffiti
            hello()
            print("Let's go back. \n")
            return_option()
        return False


# calls main function
main()
