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
    # prints a header
    print(f"{'Position' : <10} {'Username' : ^27} {'Result' : >10}")
    for item in score[:10]:
        position += 1
        position_string = str(position) + '.'
        usernames, results = item
        # if True, slow prints in green and resets style
        if player_won is False:
            slow_print(
                f"{position_string : >5} "
                f"{usernames : ^35} {results : > 4}"
                )
        elif search_element(item, username):
            slow_print(
                Fore.GREEN +
                f"{position_string : >5} {username : ^35} {results : >4}" +
                Style.RESET_ALL
                )
        # If False, slow prints normally
        else:
            slow_print(
                f"{position_string : >5} "
                f"{usernames : ^35} {results : > 4}"
                )
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

    leaderboard_menu = TerminalMenu(
        leaderboard_options
        )

    # variable stores user's current choice within the menu.
    user_choice = None

    print("Want to see if you make it onto the leaderboard?")

    while True:
        current_display = leaderboard_menu.show()
        user_choice = leaderboard_options[current_display]

        if user_choice == "[y] Yes":
            username_check = False
            while username_check is False:
                username = input("Enter a preferred username: ")
                if len(username) > 15 or len(username) < 2:
                    clear()
                    print(
                        Fore.RED +
                        "Username must be at least 3 characters long, "
                        "and can only be 15 characters long. \n" +
                        Style.RESET_ALL
                        )
                else:
                    clear()
                    username_check = True
                    data.append(username)
                    data.append(len(player_guesses) + 1)
                    print()
                    print(
                        f"Hi {username}, let's see "
                        "if you've scored a position on the leaderboard..."
                    )
                    worksheet = SHEET.worksheet(game_mode)
                    worksheet.append_row(data)
                    print_scoreboard(game_mode, True, SHEET, continue_playing)
                    return False
        elif user_choice == "[n] No":
            clear()
            print("Not a competitive one, eh? \n")
            print("That's ok, thank you for playing! \n")
            continue_playing()
            return False
