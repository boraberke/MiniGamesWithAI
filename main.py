from threading import Thread
from collections import deque
from featureExtractors import is_dead_end
from graphics import TicTacToeTable 
from tictactoe import TicTacToe,Squares,GameState
from snake import Squares
from snake import GameState


table = TicTacToeTable()
game = TicTacToe(table,'Human','AI')
control_thread = Thread(target=game.run, daemon=True)
control_thread.start()
table.run_mainloop()
