import random

random_number = random.randint(1, 10) #todo: when menu is created, stop needs to depend on the game mode chosen. 
print(random_number)
player_choice = 0
player_guesses = []


def check_if_won(random_number, player_choice):
    """
    Function compares player's guess with the computer's choice.
    If the choice is correct, player won.
    If the guess is wrong, player is told this. #todo: Decide the hot/cold logic. 
    """
    print(player_guesses)
    if random_number == player_choice:
        print("You won!")
    else:
        check_choice(random_number, player_choice)


def check_choice(random_number, player_choice):
    difference = 0
    if random_number != player_choice and bool(player_guesses) == False:
        print("Cold")
    elif random_number != player_choice and bool(player_guesses):
        smaller_number = min(random_number, player_choice)
        bigger_number = max(random_number, player_choice)
        difference = bigger_number - smaller_number
        print(difference)
    player_guesses.append(difference)




while random_number != player_choice:
    player_choice = int(input("Your guess: "))
    check_if_won(random_number, player_choice)
    



