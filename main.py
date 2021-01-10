from threading import Thread
from graphics import TicTacToeTable 
from tictactoe import TicTacToe,Squares

table  = TicTacToeTable()
game = TicTacToe(table,Squares.Circle)
control_thread = Thread(target=game.run, daemon=True)
control_thread.start()
table.run_mainloop()


