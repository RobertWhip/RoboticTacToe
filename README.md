# RoboticTacToe
Play TicTacToe against a raspberry pi robot arm.

##Requirements:
  1. Raspberry pi
  2. Camera
  3. TicTacToe board

##How to start:
  1. Run Test.py. The camera will turn on. Center the board.
  2. Run Main.py
  3. Play

XOBoard.py - in this file I have released the mark (x and o) detection, I have used the OpenCV library. 
    - CamAutoDetectBoard.get_game_board() returns a two dimensional array of the game field ( [[-1,-1,-1],[-1,-1,-1],[-1, 1 0]], where -1 if the cell is empty; 0 if the cell contains an O mark; 1 if the cell contains a 1 mark).

RobotArm.py - in this file I have released the mechanics of the robot arm with pigpiod library.

Main.py - in this file I have released the tictactoe game logic and using XOBoard.py and RobotArm.py filet to read the board and draw on it.

Test.py - in this file I have released the testing of the camera, so the user can correct(center) the camera before he starts to play.
