import XOBoard
import RobotArm


def get_player_move(board):
    board_ = [[]]
    i = 0
    while i < 10:
        board_ = camera.get_game_board()
        board__ = camera.get_game_board()
        if matrix_equal(board_, board__) and not matrix_equal(board, board_):
            i += 1
        else:
            i = 0
    return board_


def matrix_equal(matrix0, matrix1):
    for i in range(len(matrix0)):
        for j in range(len(matrix0[0])):
            if matrix0[i][j] != matrix1[i][j]:
                return False
    return True


camera = XOBoard.CamAutoDetectBoard(desktop_mode=True, console_debug=True, window_name="TicTacToe")
camera.test_camera()  # press ESC to stop on the current frame
board = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]

while True:
    board = get_player_move(board)
    print(board)
