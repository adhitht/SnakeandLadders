# SnakeandLadders

## Note: This repository is archived and is no longer maintained.

Snake and Ladders is a classic board game played between two or more players on a game board with numbered squares. The objective is to navigate from the start to the finish according to dice rolls, with the help or hindrance of snakes and ladders placed on the board.

This bot is live at [@snakeandladdersbot](https://t.me/snakeandladderbot).

This project aims to build this into python in the form of a bot. Add this bot to your telegram group and use `/joingame` command to join the game. When enough players have joined, use `/startgame` to start the game. The bot will assign dice rolls and move the players accordingly. The game will continue until all players reach 100. `/killgame` command can be used to end the game at any time.

There is no database for this project, game states are saved as `txt` files. 


## Commands
- `/start` - Start the bot and display a welcome message.
- `/help` - Display help information.
- `/newgame` - Start a new game.
- `/joingame` - Join an existing game.
- `/killgame` - End the current game.
- `/startgame` - Begin the game after players have joined.

## Installation
1. Installation

```bash
git clone https://github.com/adhitht/SnakeandLadders.git
cd SnakeandLadders
```

2. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your bot token:
```makefile
BOT_TOKEN=your-bot-token
```

### Usage
1. Run the bot:    
```bash
python3 homerun.py # On Windows python homerun.py
```
2. Open Telegram and search for your bot.
3. Start interacting with the bot using the available commands.
