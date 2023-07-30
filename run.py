import random
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


random_number = random.randint(1, 10) #todo: when menu is created, stop needs to depend on the game mode chosen. 
print(random_number) #todo: delete later
player_choice = None
player_guesses = []

def check_if_won(random_number, player_choice):
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
        scoreboard()
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
            print("Try again, still not right.")
        else:
            print("Warmer")


# scoreboard_handling = check_if_won(random_number, player_choice)
# print(scoreboard_handling)


def scoreboard():
    scoreboard_confirm = input("Want to see if you make it onto the leaderboard? (y/n) ") #todo: Add validation for n and invalid responses
    if scoreboard_confirm == "y":
        username = input("Enter a preferred username: ") #todo: Add validation
        print(f"Hi, {username}, let's see if you've scored a position on the leaderboard...")


while random_number != player_choice:
    player_choice = int(input("Your guess: "))
    check_if_won(random_number, player_choice)




    


