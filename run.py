import random
from pprint import pprint
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

# game_running = False

def update_scoreboard(difficulty):
    """
    Function pulls top 10 results depending on the difficulty played.
    Function collects values from 2 columns.
    Values are zipped together and sorted by the int in second column.
    """
    if difficulty == 10:
        worksheet = SHEET.worksheet("beginner")
    elif difficulty == 100:
        worksheet = SHEET.worksheet("intermediate")
    elif difficulty == 1000:
        worksheet = SHEET.worksheet("expert")
    # column = sales.col_values(3)
    # print(column)
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


def scoreboard(difficulty):
    """
    Function obtains user's username and pushes it along with the amount of guesses to
    the relevant worksheet depending on the difficulty played.
    Function calls update_scoreboard().
    """
    data = []
    scoreboard_confirm = input("Want to see if you make it onto the leaderboard? (y/n) ") #todo: Add validation for n and invalid responses
    if scoreboard_confirm == "y":
        username = input("Enter a preferred username: ") #todo: Add validation
        data.append(username)
        data.append(len(player_guesses) + 1)
        # print(data)
        print(f"Hi, {username}, let's see if you've scored a position on the leaderboard...")
        if difficulty == 10:
            worksheet = SHEET.worksheet("beginner")
            worksheet.append_row(data)
        elif difficulty == 100:
            worksheet = SHEET.worksheet("intermediate")
            worksheet.append_row(data)
        elif difficulty == 1000:
            worksheet = SHEET.worksheet("expert")
            worksheet.append_row(data)
        update_scoreboard(difficulty)


def check_if_won(random_number, player_choice, difficulty):
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
        print("You won!") #todo: need to count checks to calculate highscore.
        print(f"It took you {len(player_guesses) + 1} {win_statement}.")
        scoreboard(difficulty)
        # scoreboard_confirm = input("Want to see if you make it onto the scoreboard? y/n ") #todo: Add validation for n and invalid responses
        # print(scoreboard_confirm)
        # return scoreboard_confirm
    elif player_choice == None:
        pass
    else:
        check_choice(random_number, player_choice)


def check_choice(random_number, player_choice): #investigate why this is called unnecessarily.
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
    check_difference(player_guesses)


def check_difference(player_guesses):
    """
    Function checks player's guesses.
    If it's player's first guess, confirms it's not right.
    If the last two guesses player made are equal length away from the result,
    player is informed they haven't guessed the number.
    If player's last guess is worse than the previous one, player is informed.
    If player's last guess is better than the previous one, player is informed.
    """
    if len(player_guesses) == 1: #todo: investigate why this is triggered (early appending)
        #todo: build logic
        print(player_guesses)
        print("You made a guess...but it's wrong...")
    else:
        if player_guesses[-2] < player_guesses[-1]:
            print("Colder...")
        elif player_guesses[-2] == player_guesses[-1]:
            print("Hmmm, not warmer, nor colder, surprisingly.")
        else:
            print("Warmer")

player_guesses = []

def run_game(difficulty):
    """
    Function takes the difficulty level chosen and adjust parameters.
    """
    random_number = random.randint(1, difficulty) #todo: when menu is created, stop needs to depend on the game mode chosen. 
    print(f"You need to guess a number between 1 and {difficulty}.")
    print(random_number) #todo: delete later
    player_choice = None
    # if game_active == True:
    while random_number != player_choice:
        player_choice = int(input("Your guess: "))
        check_if_won(random_number, player_choice, difficulty)


def run_beginner_mode():
    """
    Function calls the run_game and provides a stop parameter of 10.
    """
    run_game(10)
    return "beginner"


def run_intermediate_mode():
    """
    Function calls the run_game and provides a stop parameter of 100.
    """
    run_game(100)
    return "intermediate"

def run_expert_mode():
    """
    Function calls the run_game and provides a stop parameter of 1000.
    """
    run_game(1000)
    return "expert"

game_mode = 0 # can this capture mode?

#at the moment copied from simple term menu, needs review
def main():
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
            print("quit")
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
                # current_display = None
                run_beginner_mode()
                break
            elif user_choice == "[2] Intermediate":
                # current_display = None
                run_intermediate_mode()
                break
            elif user_choice == "[3] Expert":
                # current_display = None
                run_expert_mode()
                break
            # else:
            #     print(f"You have selected {options[option_index]}!")

if __name__ == "__main__":
    main()

# scoreboard_handling = check_if_won(random_number, player_choice)
# print(scoreboard_handling)


game_running = main()

# def run_game(game_running):
    # if game_active == True:
    #     while random_number != player_choice:
    #         player_choice = int(input("Your guess: "))
    #         check_if_won(random_number, player_choice)




    


