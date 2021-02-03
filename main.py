from threading import Thread

from featureExtractors import is_dead_end
from graphics import TicTacToeTable 
from tictactoe import TicTacToe,Squares,GameState

from snake import GameState

state = GameState(3, 10, 3, 'NORTH')
print(is_dead_end(state, None, 10))
#
# table  = TicTacToeTable()
# game = TicTacToe(table,'Human','AI')
# control_thread = Thread(target=game.run, daemon=True)
# control_thread.start()
# table.run_mainloop()
