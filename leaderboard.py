def print_scoreboard(game_mode, flag, SHEET, continue_playing):
    """
    Function pulls top 10 results depending on the difficulty played:
    Function collects values from 2 columns.
    Values are zipped together and sorted by the int in second column.
    Results are unpacked from a tuple and printed out aligned with header.
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


def scoreboard_preference(
        game_mode,
        player_guesses,
        SHEET,
        continue_playing):
    """
    Functions checks user's preference to add their name to the scoreboard.
    Function obtains user's validated username,
    pushes it along with the amount of guesses to
    the relevant worksheet depending on the difficulty played.
    Function calls print_scoreboard().
    To control the flow, bool is passed to print_scoreboard().
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
                    print(
                        f"Hi {username}, let's see "
                        "if you've scored a position on the leaderboard..."
                    )
                    worksheet = SHEET.worksheet(game_mode)
                    worksheet.append_row(data)
                    print_scoreboard(game_mode, True, SHEET, continue_playing)
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
