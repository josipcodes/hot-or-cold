# importing to enable text coloring
from colorama import Fore, Style
# importing to assist with menu building
from simple_term_menu import TerminalMenu
# importing helper functions
from helpers import (
    slow_print,
    search_element,
    clear
)


def print_scoreboard(game_mode, player_won, SHEET, continue_playing):
    """
    Function pulls top 10 results depending on the difficulty played:
    Function collects values from 2 columns.
    Values are zipped together and sorted by the int (second column).
    Results are unpacked from a tuple and printed out aligned with header.
    If there are less than 10 results available,
    only available results are printed.
    player_won:
    False if function accessed through leaderboard_info(),
    True if player won, continue_playing() gets called.
    """
    # Sets worksheet to match the game_mode
    worksheet = SHEET.worksheet(game_mode)
    # Collects values in columns
    columns = []
    # Collects usernames tied to the guesses
    score = []
    for index in range(1, 3):
        column = worksheet.col_values(index)
        columns.append(column[1:])
    for username, guess in zip(columns[0], columns[1]):
        score.append((username, int(guess)))
    # Sorts score by the guess volume, from least to most
    score.sort(key=lambda tup: tup[1])
    # Used to calculate a position on the scoreboard
    position = 0
    # print()
    # prints a header
    print(f"{'Position' : <10} {'Username' : ^27} {'Result' : >10}")
    # Loop uses first 10 results on the worksheet.
    for item in score[:10]:
        # Increases position by 1.
        position += 1
        # Turns position int into str.
        position_string = str(position) + '.'
        # Unpacking a tuple
        usernames, results = item
        # If player_won is False, calls slow_print_default.
        if player_won is False:
            slow_print_default(position_string, usernames, results)
        # If player_won is True, and username is on the board,
        # slow prints their username in green and resets style.
        elif search_element(item, username):
            slow_print(
                Fore.GREEN +
                f"{position_string : >5} {username : ^35} {results : >4}" +
                Style.RESET_ALL
                )
        # Else, calls slow_print_default()
        else:
            slow_print_default(position_string, usernames, results)
    print()
    # If True (player won and is not accessing leaderboard via the menu),
    # calls function
    if player_won:
        continue_playing()


def scoreboard_preference(
        game_mode,
        player_guesses,
        SHEET,
        continue_playing,
        ):
    """
    Functions checks user's preference to add their name to the scoreboard.
    Function obtains user's validated username,
    pushes it along with the amount of guesses to
    the relevant worksheet depending on the difficulty played.
    Function calls print_scoreboard().
    To control the flow, bool is passed to print_scoreboard().
    Alternatively, function thanks user for playing.
    Username validation - length of > 2 and <= 15 characters,
    accepts all characters.
    """
    # collects username and guess amount
    data = []

    # Leaderboard options.
    leaderboard_options = [
        "[y] Yes",
        "[n] No"
        ]

    # Leaderboard menu.
    leaderboard_menu = TerminalMenu(
        leaderboard_options
        )

    # variable stores user's current choice within the menu.
    user_choice = None

    print("Want to see if you make it onto the leaderboard?")

    while True:
        current_display = leaderboard_menu.show()
        user_choice = leaderboard_options[current_display]
        # Checks if the user wants to add their name to the board.
        if user_choice == "[y] Yes":
            # set a validation flag, default is False.
            username_check = False
            while username_check is False:
                username = input("Enter a preferred username: ")
                # If username is too short/long or blank, warn player.
                if len(username) > 15 or len(username) < 2 or str.isspace(
                        username
                        ):
                    clear()
                    print(
                        Fore.RED +
                        "Username must be at least 3 characters long, "
                        "and can only be 15 characters long. \n" +
                        "Username cannot consist solely of spaces.")
                    print(Style.RESET_ALL)
                # If validation passed, update flag to True
                else:
                    clear()
                    username_check = True
                    # Append username and score to data.
                    data.append(username)
                    data.append(len(player_guesses) + 1)
                    print()
                    print(
                        f"Hi {username}, let's see "
                        "if you've scored a position on the leaderboard... \n"
                    )
                    # Set worksheet to the relevant worksheet
                    worksheet = SHEET.worksheet(game_mode)
                    # Append data onto relevant worksheet
                    worksheet.append_row(data)
                    # Calls print_scoreboard()
                    print_scoreboard(game_mode, True, SHEET, continue_playing)
                    return False
        # If user doesn't want to add their name onto the board,
        # call continue_playing()
        elif user_choice == "[n] No":
            clear()
            print("Not a competitive one, eh? \n")
            print("That's ok, thank you for playing! \n")
            continue_playing()
            return False


def slow_print_default(position_string, usernames, results):
    """
    Slow prints position, username and result in preferred format.
    """
    slow_print(
        f"{position_string : >5} "
        f"{usernames : ^35} {results : > 4}"
        )
