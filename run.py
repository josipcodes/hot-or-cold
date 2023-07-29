import random

random_number = random.randrange(1, 10) #todo: when menu is created, stop needs to depend on the game mode chosen. 
player_choice = 0

def check_choice(random_number, player_choice):
    """
    Function compares player's guess with the computer's choice.
    If the choice is correct, player won.
    If the guess is wrong, player is told this. #todo: Decide the hot/cold logic. 
    """
    if random_number == player_choice:
        print("You won!")
    elif random_number != player_choice:
        print("Nah")

while random_number != player_choice:
    player_choice = int(input("Your guess: "))
    check_choice(random_number, player_choice)
    



