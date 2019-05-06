import cv2
import numpy as np


class CamAutoDetectBoard:
    '''
        desktop_mode     is responsible for showing the windows
        consolde_debug   is responsible for output to the console
        solidity         contour_area/convex_hull_area
        window_name      desktop frame title
    '''
    def __init__(self, desktop_mode=False, console_debug=False, solidity=0.85, min_contour_area=500, window_name="Frame"):
        self.__img = None
        self.__gray_img = None
        self.__desktop_mode = desktop_mode
        self.__console_debug = console_debug
        self.__solidity = solidity  # contour_area / convex_hull_area
        self.__min_contour_area = min_contour_area
        self.__window_name = window_name  # title
        self.__cap = cv2.VideoCapture(0)

    def __del__(self):
        self.__cap.release()
        cv2.destroyAllWindows()

    def end(self):
        self.__del__()

    def __str__(self):
        return self.__window_name

    '''
        -1 : empty
        0  : O
        1  : X
    '''
    def get_game_board(self):
        board = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        _, self.__img = self.__cap.read()
        self.__gray_img = 255 - cv2.cvtColor(self.__img, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(self.__gray_img, 50, 150, apertureSize=3)
        min_line_length = 5000
        max_line_gap = 9
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, min_line_length, max_line_gap)

        xs = []
        ys = []
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    xs.append(x1)
                    xs.append(x2)
                    ys.append(y1)
                    ys.append(y2)
        if len(xs) > 0 and len(ys) > 0:
            min_x, min_y = min(xs), min(ys)
            max_x, max_y = max(xs), max(ys)
            tmp_x = (max_x - min_x) // 3
            tmp_y = (max_y - min_y) // 3

            if self.__console_debug:
                print("Start X: {0}; end X {1}\nStart Y: {2}; End Y: {3}".format(min_x, max_x, min_y, max_y))

            board[0][0] = self.__get_type(min_y, min_y + tmp_y, min_x, min_x + tmp_x)
            board[0][1] = self.__get_type(min_y, min_y + tmp_y, min_x + tmp_x, max_x - tmp_x)
            board[0][2] = self.__get_type(min_y, min_y + tmp_y, max_x - tmp_x, max_x)

            board[1][0] = self.__get_type(min_y + tmp_y, max_y - tmp_y, min_x, min_x + tmp_x)
            board[1][1] = self.__get_type(min_y + tmp_y, max_y - tmp_y, min_x + tmp_x, max_x - tmp_x)
            board[1][2] = self.__get_type(min_y + tmp_y, max_y - tmp_y, max_x - tmp_x, max_x)

            board[2][0] = self.__get_type(max_y - tmp_y, max_y, min_x, min_x + tmp_x)
            board[2][1] = self.__get_type(max_y - tmp_y, max_y, min_x + tmp_x, max_x - tmp_x)
            board[2][2] = self.__get_type(max_y - tmp_y, max_y, max_x - tmp_x, max_x)

        if self.__console_debug:
            for row in board:
                for col in row:
                    print(col, "", end="")
                print()

        if self.__desktop_mode:
            cv2.imshow(self.__window_name, self.__img)
            cv2.waitKey(0)

        return board

    '''
        ESC to exit the window
    '''
    def test_camera(self):
        if self.__desktop_mode:
            board = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
            font = cv2.FONT_HERSHEY_SIMPLEX
            while True:
                _, self.__img = self.__cap.read()
                self.__gray_img = 255 - cv2.cvtColor(self.__img, cv2.COLOR_BGR2GRAY)

                edges = cv2.Canny(self.__gray_img, 50, 150, apertureSize=3)
                min_line_length = 5000
                max_line_gap = 9
                lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, min_line_length, max_line_gap)

                xs = []
                ys = []
                if lines is not None:
                    for line in lines:
                        for x1, y1, x2, y2 in line:
                            if self.__desktop_mode:
                                cv2.line(self.__img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                            xs.append(x1)
                            xs.append(x2)
                            ys.append(y1)
                            ys.append(y2)

                if not(len(xs) == 0 and len(ys) == 0):

                    min_x, min_y = min(xs), min(ys)
                    max_x, max_y = max(xs), max(ys)
                    tmp_x = (max_x - min_x) // 3
                    tmp_y = (max_y - min_y) // 3
                    if self.__desktop_mode:
                        cv2.rectangle(self.__img, (min_x, min_y), (max_x, max_y), (255, 0, 0), 1)

                        cv2.rectangle(self.__img, (min_x + tmp_x, min_y), (min_x + tmp_x, max_y), (0, 255, 255), 1)
                        cv2.rectangle(self.__img, (max_x - tmp_x, min_y), (max_x - tmp_x, max_y), (0, 255, 255), 1)

                        cv2.rectangle(self.__img, (min_x, min_y + tmp_y), (max_x, min_y + tmp_y), (0, 255, 255), 1)
                        cv2.rectangle(self.__img, (min_x, max_y - tmp_y), (max_x, max_y - tmp_y), (0, 255, 255), 1)

                        cv2.putText(self.__img, '0', (min_x, min_y + tmp_y), font, 2, (0, 0, 255), 2, cv2.LINE_AA)
                        cv2.putText(self.__img, '1', (min_x + tmp_x, min_y + tmp_y), font, 2, (0, 0, 255), 2, cv2.LINE_AA)
                        cv2.putText(self.__img, '2', (max_x - tmp_x, min_y + tmp_y), font, 2, (0, 0, 255), 2, cv2.LINE_AA)

                        cv2.putText(self.__img, '3', (min_x, min_y + tmp_y + tmp_y), font, 2, (0, 0, 255), 2, cv2.LINE_AA)
                        cv2.putText(self.__img, '4', (min_x + tmp_x, min_y + tmp_y + tmp_y), font, 2, (0, 0, 255), 2,
                                    cv2.LINE_AA)
                        cv2.putText(self.__img, '5', (max_x - tmp_x, min_y + tmp_y + tmp_y), font, 2, (0, 0, 255), 2,
                                    cv2.LINE_AA)

                        cv2.putText(self.__img, '6', (min_x, max_y), font, 2, (0, 0, 255), 2, cv2.LINE_AA)
                        cv2.putText(self.__img, '7', (min_x + tmp_x, max_y), font, 2, (0, 0, 255), 2, cv2.LINE_AA)
                        cv2.putText(self.__img, '8', (max_x - tmp_x, max_y), font, 2, (0, 0, 255), 2, cv2.LINE_AA)

                    if self.__console_debug:
                        print("Start X: {0}; end X {1}\nStart Y: {2}; End Y: {3}".format(min_x, max_x, min_y, max_y))

                    board[0][0] = self.__get_type(min_y, min_y + tmp_y, min_x, min_x + tmp_x)
                    board[0][1] = self.__get_type(min_y, min_y + tmp_y, min_x + tmp_x, max_x - tmp_x)
                    board[0][2] = self.__get_type(min_y, min_y + tmp_y, max_x - tmp_x, max_x)

                    board[1][0] = self.__get_type(min_y + tmp_y, max_y - tmp_y, min_x, min_x + tmp_x)
                    board[1][1] = self.__get_type(min_y + tmp_y, max_y - tmp_y, min_x + tmp_x, max_x - tmp_x)
                    board[1][2] = self.__get_type(min_y + tmp_y, max_y - tmp_y, max_x - tmp_x, max_x)

                    board[2][0] = self.__get_type(max_y - tmp_y, max_y, min_x, min_x + tmp_x)
                    board[2][1] = self.__get_type(max_y - tmp_y, max_y, min_x + tmp_x, max_x - tmp_x)
                    board[2][2] = self.__get_type(max_y - tmp_y, max_y, max_x - tmp_x, max_x)

                if self.__console_debug:
                    for row in board:
                        for col in row:
                            print(col, "", end="")
                        print()

                if self.__desktop_mode:
                    cv2.imshow(self.__window_name, self.__img)
                    key = cv2.waitKey(1)
                    if key == 27:
                        break
        else:
            raise Exception("desktop_mode should be True to test the camera.")

    def __get_contour_area(self, ys, ye, xs, xe):
        _, thresh = cv2.threshold(self.__gray_img[ys:ye, xs:xe], 125, 125, 0)
        _,contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        max_c, cont = 0, None
        if len(contours) > 0:
            max_c, cont = cv2.contourArea(contours[0]), contours[0]
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > max_c:
                    max_c, cont = area, cnt
            if self.__desktop_mode:
                cv2.drawContours(self.__img[ys:ye, xs:xe], [cont], 0, (0, 255, 0), 2)
        return max_c, cont

    def __get_convex_hull_area(self, contour, ys, ye, xs, xe):
        if self.__desktop_mode:
            cv2.drawContours(self.__img[ys:ye, xs:xe], [cv2.convexHull(contour, False)], 0, (255, 0, 0), 2, 8)
        return cv2.contourArea(cv2.convexHull(contour, False))

    def __get_approx_poly(self, contour):
        epsilon = cv2.arcLength(contour, True)*0.02
        return cv2.approxPolyDP(contour, epsilon, True)

    # -1 - none; 0 - O; 1 - X
    def __get_type(self, ys, ye, xs, xe):
        cont_area, cont = self.__get_contour_area(ys, ye, xs, xe)
        convex_hull_area = 1
        approx_poly = -1
        if cont is not None:
            convex_hull_area = self.__get_convex_hull_area(cont, ys, ye, xs, xe)+0.0001
            approx_poly = len(self.__get_approx_poly(cont))
        solidity = cont_area / convex_hull_area

        if self.__console_debug:
            print("Solidity: {0}".format(solidity))
            print("Approx poly: {0}".format(approx_poly))
            print("Contour area: {0}; convex hull area: {1}".format(cont_area, convex_hull_area))
            print()
        if approx_poly >= 7 and cont_area > self.__min_contour_area:
            if solidity >= self.__solidity:
                return 0
            elif 0 < solidity < self.__solidity:
                return 1
        else:
            return -1


class CamFixedBoard:
    def __init__(self):
        raise Exception("fixed board is not working.")

#board = CamAutoDetectBoard(desktop_mode=True, console_debug=True, window_name="TicTacToe")
#board.test_camera()  # press ESC to stop on the current frame
#print(board.get_game_board())
