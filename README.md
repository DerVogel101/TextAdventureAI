# TextAdventureAI
This is my Game written in Python using the ChatGPT API to play a game in the Commandline
## How to start
1. Install python 3.10 or higher
2. Launch the launch script (`launch.cmd`, `launch.sh` or `launch.ps1`)
If you are using the sh script you need to run `sudo pip install virtualenv` before launching with `bash launch.sh`
3. Enter in the API Key for the ChatGPT API if you already entered it, the programm will skip this step, if your key is not valid just delete the .env file and restart the script.
### Manual start
1. Install python 3.10 or higher
2. Install the requirements with `pip install -r requirements.txt` (recommended in a venv)
3. Create a `.env` file in the same directory as the `main.py` file
4. Edit it and write this inside it `API_KEY="YOUR API KEY"` and replace the placeholder with your key
5. Launch the main.py file with `python main.py` or `python3 main.py`

## How to play
1. You will be asked to Edit the Prompt for the AI, if not changed it will be the default prompt (I recommend changing it if you cant understand German)
2. You can now Continue
3. If you have already played the Game you can now load your save, if not you can start a new game
4. You can now send Your Actions to the Game and the AI will respond to it, with [EXIT] can you exit the game
5. you can now just enter the save name and the game will save your game and exit
