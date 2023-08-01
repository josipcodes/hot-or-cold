import random
import math
from pprint import pprint # is it needed?
from simple_term_menu import TerminalMenu
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
CREDS = Credentials.from_service_account_file("credentials.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("hot-or-cold-scoreboard")


def update_scoreboard(game_mode):
    """
    Function pulls top 10 results depending on the difficulty played.
    Function collects values from 2 columns.
    Values are zipped together and sorted by the int in second column.
    Function prints out top 10 results off the scoreboard
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
    for item in score[:10]:
        print(item)


def scoreboard(game_mode): #review function naming
    """
    Function obtains user's username and pushes it along with the amount of guesses to
    the relevant worksheet depending on the difficulty played.
    Function calls update_scoreboard().
    """
    data = []
    while True:
        scoreboard_confirm = input("Want to see if you make it onto the leaderboard? (y/n) ")
        print(scoreboard_confirm)
        if scoreboard_confirm.lower() == "y":
            username = input("Enter a preferred username: ")
            data.append(username)
            data.append(len(player_guesses) + 1)
            print(f"Hi, {username}, let's see if you've scored a position on the leaderboard...")
            worksheet = SHEET.worksheet(game_mode)
            worksheet.append_row(data)
            update_scoreboard(game_mode)
            break
        elif scoreboard_confirm.lower() == "n":
            print("Not a competitive one, eh?")
            print("That's ok, thank you for playing! \n")
            break
        else:
            print(f"You have entered '{scoreboard_confirm}', which is not a valid command.")
            print("Please enter a valid command. \n")


def check_if_won(random_number, player_choice, game_mode, difficulty):
    """
    Function compares player's guess with the computer's choice.
    If the choice is correct, player won.
    If the guess is wrong, check_choice function is called. #todo: Decide the hot/cold logic. 
    """
    if random_number == player_choice:
        if len(player_guesses) != 0:
            win_statement = "attempts"
        else:
            win_statement = "attempt"
        print("You won!") 
        print(f"It took you {len(player_guesses) + 1} {win_statement}.\n")
        scoreboard(game_mode)
    elif player_choice == None:
        pass
    else:
        check_choice(random_number, player_choice, difficulty)


def check_choice(random_number, player_choice, difficulty): #investigate why this is called unnecessarily.
    """
    Function calculates the difference between the bigger and smaller number.
    Numbers are comprised of the computer's and player's choices.
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
    If player's last guess is worse than the previous one, player is informed.
    If player's last guess is better than the previous one, player is informed.
    #need to add a note regarding multiple statements.
    """
    if player_guesses[-1] <= difficulty / 10:
        hot_statements = [
        "Hot! Hot! Hot!...", 
        "Sizzling!", 
        "Global warming ahead, you're close!"
        ]
        statement_index = random.randint(0, 2)
        print(f"{hot_statements[statement_index]}")
    elif len(player_guesses) == 1: #todo: investigate why this is triggered (early appending)
        #todo: build logic
        print(player_guesses)
        first_guess_statements = [
        "You made a guess...but it's wrong...", 
        "Hmmm, not quite right, try again.", 
        "Wanna take another swing at this?"
        ]
        statement_index = random.randint(0, 2)
        print(f"{first_guess_statements[statement_index]}")
    else:
        if player_guesses[-2] < player_guesses[-1]:
            colder_statements = [
            "Colder...", 
            "If you're trying to be bad at this, great job!", 
            "Snowman alert!"
            ]
            statement_index = random.randint(0, 2)
            print(f"{colder_statements[statement_index]}")
        elif player_guesses[-2] == player_guesses[-1]:
            same_difference_statements = [
            "Hmmm, not warmer, nor colder, surprisingly.", 
            "Yeah, so the answer is somewhere in between your previous guess and this one.", 
            "Same temperature, seems like you like consistency.",
            "April 25th, it's not too hot, not too cold. All you need is a light jacket."
            ]
            statement_index = random.randint(0, 3)
            print(f"{same_difference_statements[statement_index]}")
        else:
            warmer_statements = [
            "Warmer...", 
            "Temperature rising!", 
            "Oooh, someone switched on the heating!"
            ]
            statement_index = random.randint(0, 2)
            print(f"{warmer_statements[statement_index]}")

player_guesses = []

def run_game(difficulty, game_mode):
    """
    Function takes the difficulty level chosen and adjust parameters.
    Function obtains a pseudo-random number between 1 and difficulty int.
    It asks for input from user as long as user doesn't guess the number.

    """

    random_number = random.randint(1, difficulty) #todo: when menu is created, stop needs to depend on the game mode chosen. 
    print(f"You need to guess a number between 1 and {difficulty}.")
    print(random_number) #todo: delete later
    player_choice = None
    validation = False
    while validation == False:
        player_choice = input("Your guess: ")
        if validate_input(player_choice, difficulty):
            player_choice = int(player_choice)
            check_if_won(random_number, player_choice, game_mode, difficulty)


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
                f"Hold on, Katy Perry, you're guessing a number between 1 and {difficulty}. \n"
                )
            return False


#at the moment copied from simple term menu, needs review
def menu():
    # Main menu options.
    main_options = [
        "[1] New Game", 
        "[2] About", 
        "[3] Leaderboard", 
        "[4] Quit"]

    # Sub-menu options.
    difficulty_options = [
        "[1] Beginner",
        "[2] Intermediate", 
        "[3] Expert",
        "[4] Go back"]
    main_menu = TerminalMenu(main_options, title = "Hot or Cold")
    difficulty_menu = TerminalMenu(difficulty_options, title = "Difficulty level")
    # main_menu_style = ("bg_red", "fg_yellow") #todo: need to check
    quit_game = False

    while quit_game == False:
        current_display = main_menu.show()
        user_choice = main_options[current_display]

        if user_choice == "[4] Quit":
            print("Thank you for playing Hot or Cold.")
            print("Hope to see you soon.")
            quit_game = True
            current_display = main_menu.show()
        elif user_choice == "[2] About":
            print("about")
        elif user_choice == "[3] Leaderboard":
            print("leaderboard")
        elif user_choice == "[1] New Game":
            current_display = difficulty_menu.show()
            user_choice = difficulty_options[current_display]
            # if difficulty_menu.show(): #todo: shorten by avoiding repetition
            if user_choice == "[1] Beginner":
                return(True, 10, "beginner")
                break
            elif user_choice == "[2] Intermediate":
                return(True, 100, "intermediate")
                break
            elif user_choice == "[3] Expert":
                return(True, 1000, "expert")
                break
            # else:
            #     print(f"You have selected {options[option_index]}!")


def main():
    """
    Function unpacks a tuple
    """
    game_status, difficulty, game_mode = menu()
    if game_status == True:
        print("if reached")
        run_game(difficulty, game_mode)
    

main()
menu()




