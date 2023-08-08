# HOT OR COLD

Want to play a game? If you've answered 'no', you might be in the wrong place.

Our game is called 'Hot or Cold'. 

You know the drill, the point of the game is to guess a number.

Our target audience are any users with access to the Internet, a bit of a free time, some sense of humour...
...and appreciation for an occasional pop-cultural reference.

Because why? Because we might have hidden a few throughout our sassy game.

![screenshot](documentation/general/heroku-deployed.png)

## UX

### Colour Scheme

Colour scheme is simple:
Color is used to emphasise information for the user.

- `#FF0000` used for invalid information entered.
- `#FFFF00` user a reminder of the previous guesses within the game.
- `#00FF00` used as main informational color.
- `#FFFFFF` used as main informational color.

I used [coolors.co](https://coolors.co/ff0000-ffff00-00ff00-ffffff) to generate my colour palette:

![screenshot](documentation/general/palette.png)

## Flowchart

I used [lucidchart.app](https://lucid.app/) to create a flowchart of the project:

![screenshot](documentation/general/flowchart.png)

## Features

### Existing Features

- **Header**

    - Our game has a header which first welcomes the player to our realm.

![screenshot](documentation/features/header.png)

- **Menu**

    - Our menu is clear and elegant.

![screenshot](documentation/features/menu.gif)

- **Difficulty levels**

    - User can choose their difficulty level.

![screenshot](documentation/features/features/difficulty.gif)

- **Scoreboard input**

    - User can choose to attempt to score a position in the scoreboard.

![screenshot](documentation/features/features/username.gif)

- **Scoreboard output**

    - User can choose to see scoreboard depending on the difficulty to know what they should be aiming for.

![screenshot](documentation/features/features/scoreboard.gif)

- **Scoreboard output - colored**

    - If the user won the game and scored a position on the leaderboard, their line will be emphasised with a green color.

![screenshot](documentation/features/features/username.gif)

- **About section**

    - User can choose to read up on the game.

![screenshot](documentation/features/features/about.gif)

- **Username input**

    - User can choose their username. Username will be validated.

![screenshot](documentation/features/features/username.gif)

- **Input validation**

    - User will be notified if their input is invalid and prompted for another attempt.

![screenshot](documentation/features/features/input-validation.gif)

- **Guess output**

    - User will receive feedback on their guess within the game.

![screenshot](documentation/features/features/feedback.gif)

- **Guess reminder**

    - User has access to their previous guesses so they don't have to memorise it.

![screenshot](documentation/features/features/guess-reminder.gif)

- **Play again?**

    - When viewing the scoreboard, user will be asked if they want to play again. This will only happen if the user finished the game before this.

![screenshot](documentation/features/features/play-again.gif)

- **Quit game**

    - User can choose to quit the game. The game will thank them for their participation.

![screenshot](documentation/features/features/bye.gif)

- **Score calculation**

    - Score equals to the amount of player's guesses. It is used to compare user's result to others' on the scoreboard.

![screenshot](documentation/features/features/username.gif)

- **Game won confirmation**

    - Once player guesses the correct number, they will be notified and prompted to choose if they want to attempt to add their name to the scoreboard.

![screenshot](documentation/features/features/random.gif)

- **Shortcuts**

    - Our menu contains shortcuts, easily visible and accessible to the user.

![screenshot](documentation/features/features/menu.gif)

- **Re-playability**

    - When launching the game, the number user needs to guess will be randomly chosen, allowing for countless plays.

![screenshot](documentation/features/features/random.gif)

- **Colors**

    - Colors are used within the game for the sole purpose of emphasising information.

![screenshot](documentation/features/features/color.gif)


### Future Features

- Statement expansion
    - We would like to add more statements used for randomisation to boost CX.
- Different modes
    - Ideally, user should be able to choose the level of game's sassiness.
    - User should be able to set the game parameters, such as having to guess numbers between X and Y or to be guessing letters instead of numbers.

## Tools & Technologies Used

- [PAGE NAME](https://LINK.org) used for PLACEHOLDER.
- [Git](https://git-scm.com) used for version control. (`git add`, `git commit`, `git push`)
- [GitHub](https://github.com) used for secure online code storage.
- [PLACEHOLDER](https://pages.github.com) used for hosting the deployed front-end site. RENDER? HEROKU?
- [Codeanywhere](https://app.codeanywhere.com) used as a cloud-based IDE for development.

## Testing

For all testing, please refer to the [TESTING.md](TESTING.md) file.

## Deployment

The site was deployed to PLACEHOLDER. The steps to deploy are as follows:
- Placeholder.

The live link can be found [here](PLACEHOLDER LINK)

### Local Deployment

This project can be cloned or forked in order to make a local copy on your own system.

#### Cloning - PLACEHOLDER

You can clone the repository by following these steps:

1. Go to the [GitHub repository](https://github.com/josipcodes/numbers-game) 
2. Locate the Code button above the list of files and click it 
3. Select if you prefer to clone using HTTPS, SSH, or GitHub CLI and click the copy button to copy the URL to your clipboard
4. Open Git Bash or Terminal
5. Change the current working directory to the one where you want the cloned directory
6. In your IDE Terminal, type the following command to clone my repository:
	- `git clone https://github.com/josipcodes/numbers-game.git`
7. Press Enter to create your local clone.

Alternatively, if using Gitpod, you can click below to create your own workspace using this repository.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/josipcodes/numbers-game)

Please note that in order to directly open the project in Gitpod, you need to have the browser extension installed.
A tutorial on how to do that can be found [here](https://www.gitpod.io/docs/configure/user-settings/browser-extension).

#### Forking - PLACEHOLDER

By forking the GitHub Repository, we make a copy of the original repository on our GitHub account to view and/or make changes without affecting the original owner's repository.
You can fork this repository by using the following steps:

1. Log in to GitHub and locate the [GitHub Repository](https://github.com/josipcodes/numbers-game)
2. At the top of the Repository (not top of page) just above the "Settings" Button on the menu, locate the "Fork" Button.
3. Once clicked, you should now have a copy of the original repository in your own GitHub account!

### Local VS Deployment - PLACEHOLDER

There are no known differences between the local version developed, and the live deployment site on GitHub Pages.

## Credits

Below resources were used in the creation of the game. No content was explicitly copied unless stated otherwise within .js, .html or .css files.

### Content

| Source | Location | Notes |
| --- | --- | --- |
| [PLACEHOLDER](PLACEHOLDER LINK) | WHERE - PLACEHOLDER | WHAT - PLACEHOLDER |

### Media - PLACEHOLDER

Placeholder, emoji

| Source | Location | Type | Notes |
| --- | --- | --- | --- |
| [PLACEHOLDER](PLACEHOLDER LINK) | PLACEHOLDER WHERE | PLACEHOLDER WHAT | PLACEHOLDER NOTES |

### Acknowledgements

- I would like to thank my Code Institute mentor, [Alex](PLACEHOLDER LINK) for their support throughout the development of this project.
- I would like to thank the [Code Institute](https://codeinstitute.net) tutor team for their assistance with troubleshooting and debugging some project issues.
- I need to thank [Codewars](https://www.codewars.com); as their katas further helped in understanding Python. 
- PLACEHOLDER
