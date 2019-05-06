import random
import XOBoard
import RobotArm
import time

def drawBoard(board):
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')
    print('---+---+---')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('---+---+---')
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')

def inputPlayerLetter():
    return ['O', 'X']

def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def playAgain():
    print('Would you like to play again? (yes/no)')
    return input().lower().startswith('y')

def makeMove(board, letter, move):
    board[move] = letter
    


def isWinner(bo, le):
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or
            (bo[4] == le and bo[5] == le and bo[6] == le) or
            (bo[1] == le and bo[2] == le and bo[3] == le) or
            (bo[7] == le and bo[4] == le and bo[1] == le) or 
            (bo[8] == le and bo[5] == le and bo[2] == le) or
            (bo[9] == le and bo[6] == le and bo[3] == le) or  
            (bo[7] == le and bo[5] == le and bo[3] == le) or 
            (bo[9] == le and bo[5] == le and bo[1] == le)) 


def getBoardCopy(board):
    dupeBoard = []

    for i in board:
        dupeBoard.append(i)

    return dupeBoard


def isSpaceFree(board, move):
    return board[move] == ' '


def getPlayerMove(board):
    move = ''
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('Your turn (1-9):')
        move = input()
    return int(move)


def chooseRandomMoveFromList(board, movesList):
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None


def getComputerMove(board, computerLetter):
    playerLetter = 'O'
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, computerLetter, i)
            if isWinner(copy, computerLetter):
                return i

    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, playerLetter, i)
            if isWinner(copy, playerLetter):
                return i

    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    if isSpaceFree(board, 5):
        return 5

    return chooseRandomMoveFromList(board, [2, 4, 6, 8])


def isBoardFull(board):
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True


def get_player_move(board):
    board_ = [[]]
    print(board)
    i = 0
    while i < 5:
        board_ = add_to_matrix(board, camera.get_game_board())
        time.sleep(0.3)
        board__ = add_to_matrix(board, camera.get_game_board())
        if matrix_equal(board_, board__) and not matrix_equal(board, board_):
            i += 1
        else:
            i = 0
    return add_to_matrix(board, board_)


def add_to_matrix(board, board_):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != -1:
                board_[i][j] = board[i][j]
    return board_


def matrix_equal(matrix0, matrix1):
    for i in range(len(matrix0)):
        for j in range(len(matrix0[0])):
            if matrix0[i][j] != matrix1[i][j]:
                return False
    return True


def matrix_to_array(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == -1:
                val = ' '
            elif matrix[i][j] == 1:
                val = 'X'
            elif matrix[i][j] == 0:
                val = 'O'
            matrix[i][j] = val

    return [' '] + matrix[2] + matrix[1] + matrix[0]


def array_to_matrix(array):
    matrix = []
    div_by = 3
    line = []
    for i in range(1, len(array)):
        if array[i] == ' ':
            val = -1
        elif array[i] == 'X':
            val = 1
        elif array[i] == 'O':
            val = 0
        if i % div_by == 0:
            line.append(val)
            matrix.append(line)
            line = []
            continue
        line.append(val)

    tmp = matrix[0]
    matrix[0] = matrix[2]
    matrix[2] = tmp
    return matrix


arm = RobotArm.RobotArm(11.2, 12, 8, 4, 3, 2)
camera = XOBoard.CamAutoDetectBoard(desktop_mode=False, console_debug=False, window_name="TicTacToe")
print("Let's play TicTacToe!")
try:

    while True:
        theBoard = [' '] * 10
        playerLetter, computerLetter = inputPlayerLetter()
        turn = whoGoesFirst()
        print('First turn: ' + turn)
        gameIsPlaying = True

        while gameIsPlaying:
            print("game is playing")
            if turn == 'player':
                # Ход игрока
                drawBoard(theBoard)
                print("WAS", theBoard)
                board = matrix_to_array(get_player_move(array_to_matrix(theBoard)))
                theBoard = board
                print("NOW", board)

                if isWinner(theBoard, playerLetter):
                    drawBoard(theBoard)
                    print('Congratulations!!! You have won!')
                    gameIsPlaying = False
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        print('Draw. Play better next time.')
                        break
                    else:
                        turn = 'computer'

            else:
                # Ход компьютера
                move = getComputerMove(theBoard, computerLetter)
                makeMove(theBoard, computerLetter, move)
                arm.drawX(2-(move-1)//3, (move-1)%3)
                print("comp")
                if isWinner(theBoard, computerLetter):
                    drawBoard(theBoard)
                    print('The computer has won! You have losed.')
                    gameIsPlaying = False
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        print('Draw.Play better next time.')
                        break
                    else:
                        turn = 'player'

        if not playAgain():
            arm.end()
            camera.end()
            break
except KeyboardInterrupt:
        arm.end()
        camera.end()
