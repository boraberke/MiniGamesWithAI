from threading import Thread
from collections import deque
from snake import start_snake
from tictactoe import start_tictactoe
import sys
import getopt

argv = sys.argv[1:]
game_name = None
game_type = None

try:
    opts, args = getopt.getopt(argv,"g:t:h",
                                ["game = ",
                                "type =",
                                "help = "])
except:
    print("python main.py <game> <type>")
    print("e.g. python main.py tictactoe human_vs_ai")


for opt, arg in opts:
    if opt in ('-g', '--game'):
        game_name = arg
    elif opt in ('-t', '--type'):
        game_type = arg
    elif opt in ('-h', '--help'):
        print("python main.py <game> <type>")

print("Starting the game: ",game_name)
if game_name == "tictactoe":
    if game_type in ("human_vs_ai", "ai_vs_human"):
        start_tictactoe('Human','AI')
    elif game_type == "human_vs_human":
        start_tictactoe('Human','Human')
    elif game_type == "ai_vs_ai":
        start_tictactoe('AI','AI')
elif game_name == "snake":
    start_snake()






