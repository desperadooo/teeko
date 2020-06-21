from PyQt5.QtWidgets import QMainWindow, QMessageBox,QPushButton,QLabel
from PyQt5.QtGui import QPainter, QPen, QColor, QPalette, QBrush, QPixmap, QRadialGradient
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.Qt import QWidget, QApplication
import sys

from Controller import Controller
from IA import IA
from Login import First,Second


class Window(QWidget):
    def __init__(self,ia):
        super().__init__()
        self.initUI()
        self.last_pos = (-1, -1)
        self.ia = ia
        self.changeStatus=0
        self.tempX = -1
        self.tempY = -1

        #self.position[0][0]=1


    def initUI(self):

        self.setObjectName('MainWindow')
        self.setWindowTitle('Teeko')
        self.setFixedSize(700, 700)
        palette = QPalette()
        self.setMouseTracking(True)
        palette.setBrush(QPalette.Window, QBrush(QPixmap('imgs/blue.png')))
        self.setPalette(palette)
        self.flash_cnt = 0
        self.flash_pieces = (-1, -1)
        self.end_timer = QTimer(self)
        self.end_timer.timeout.connect(self.flash)

    def reInit(self):
        self.last_pos = (-1, -1)
        self.ia = ia
        self.changeStatus = 0
        self.tempX = -1
        self.tempY = -1

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        self.draw_teek(qp)
        qp.end()
     #Line drawing event function
    def drawLines(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        # draw a horizontal line
        for x in range(5):
            qp.drawLine(120 * (x + 1), 120, 120 * (x + 1), 600)
        # draw a vertical line
        for y in range(5):
            qp.drawLine(120, 120 * (y + 1), 600, 120 * (y + 1))

        qp.drawLine(120, 120, 240, 240)
        # Drawing black dots on a chessboard
        qp.setBrush(QColor(255, 255, 255))
        key_points = [(3, 3), (3, 6),(3,9),(3, 12),(3,15),(6,3),(6,6),(6,9),(6,12),(6,15),(9,3),(9,6),(9,9),(9,12),(9,15),
                      (12,3),(12,6),(12,9),(12,12),(12,15),(15,3),(15,6),(15,9),(15,12),(15,15)]
        for t in key_points:
            qp.drawEllipse(QPoint(40 * t[0], 40 * t[1]), 20, 20)

        for i in range(19):
            if i!=4 and i!=9 and i!=14 and i!=19:
               qp.drawLine(40*key_points[i][0],40*key_points[i][1],40*key_points[i+6][0],40*key_points[i+6][1])
        for i in range(20):
            if i != 0 and i != 5 and i != 10 and i != 15:
               qp.drawLine(40 * key_points[i][0], 40 * key_points[i][1], 40 * key_points[i + 4][0],40 * key_points[i + 4][1])
        for t in key_points:
            qp.drawEllipse(QPoint(40 * t[0], 40 * t[1]), 20, 20)

    def draw_teek(self, qp):
        key_points = [(3, 3), (3, 6), (3, 9), (3, 12), (3, 15), (6, 3), (6, 6), (6, 9), (6, 12), (6, 15), (9, 3),
                      (9, 6), (9, 9), (9, 12), (9, 15),(12, 3), (12, 6), (12, 9), (12, 12), (12, 15), (15, 3), (15, 6), (15, 9), (15, 12), (15, 15)]

        for i in range(5):
            for j in range(5):
                 if self.ia.board.coordinate[i][j]== 1:
                    if self.flash_cnt % 2 == 1 and (i, j) == self.flash_pieces:
                         continue
                    qp.setBrush(QColor(0,0,0))
                    qp.drawEllipse(QPoint(40 * key_points[i+5*j][0], 40 * key_points[i+5*j][1]), 20, 20)
                 if self.ia.board.coordinate[i][j] == 2:
                     if self.flash_cnt % 2 == 1 and (i, j) == self.flash_pieces:
                         continue
                     qp.setBrush(QColor(244,121,131))
                     qp.drawEllipse(QPoint(40 * key_points[i + 5 * j][0], 40 * key_points[i + 5 * j][1]), 20, 20)
    def mouseMoveEvent(self, e):
        # 1. First determine which square on the board corresponds to the mouse position.
        mouse_x = e.windowPos().x()
        mouse_y = e.windowPos().y()
        if 100<= mouse_x <= 620 and 100 <= mouse_y <= 620 and (mouse_x % 120 <= 20 or mouse_x % 120 >= 100) and (mouse_y % 120 <= 20 or mouse_y % 120 >= 100):
            game_x = int((mouse_x + 20) // 120) - 1
            game_y = int((mouse_y + 20) // 120) - 1
        else:  # The current position of the mouse does not correspond to any of the game grids, mark it as (01, 01)
            game_x = -1
            game_y = -1


         # 2. Then determine if the mouse position has changed from the previous moment.
        pos_change = False  # Mark if the mouse position has changed
        if game_x != self.last_pos[0] or game_y != self.last_pos[1]:
             pos_change = True
        self.last_pos = (game_x, game_y)

         # 3. Finally, draw special markers according to the change in mouse position.
        if pos_change and game_x != -1:
             self.setCursor(Qt.PointingHandCursor)
        if pos_change and game_x == -1:
             self.setCursor(Qt.ArrowCursor)


    def mousePressEvent(self, e):
        """Determine the position of the drop according to the mouse movement"""
        if e.button() == Qt.LeftButton:
            # Determine which cell is pressed first
            mouse_x = e.windowPos().x()
            mouse_y = e.windowPos().y()

            if 100 <= mouse_x <= 620 and 100 <= mouse_y <= 620 and (mouse_x % 120 <= 20 or mouse_x % 120 >= 100) and (mouse_y % 120 <= 20 or mouse_y % 120 >= 100):
                game_x = int((mouse_x + 20) // 120) - 1
                game_y = int((mouse_y + 20) // 120) - 1
            else:  # The mouse click is not in the right place.
                return

            if self.ia.board.coordinate[game_y][game_x]!=2 or self.ia.board.flagH<4:
                if self.ia.board.flagH < 4:
                    if self.ia.board.putFlag(game_y, game_x):
                        self.ia.board.changeRole()
                        if self.ia.board.whether_win() is True:
                            QMessageBox.about(self, 'Congratulation', "Win!!!!")
                            wd.close()
                            return
                        self.ia.board.changeRole()
                        self.ia.minmax()
                        self.ia.board.changeRole()
                        if self.ia.board.whether_win() is True:
                            QMessageBox.about(self, 'Congratulation', "Lose!!!")
                            wd.close()
                            return
                        self.ia.board.changeRole()
                    else:
                        QMessageBox.about(self, 'Warning', "You can't put the flag in this position")
                elif self.ia.board.flagH >= 4:
                    if self.changeStatus==0 and self.ia.board.coordinate[game_y][game_x]==1:
                        self.tempX=game_x
                        self.tempY=game_y
                        self.changeStatus=1
                        self.flash_pieces = (game_y, game_x)
                        self.end_timer.start(300)
                    elif self.changeStatus == 1:
                        position = self.ia.board.moveHelper(game_y-self.tempY,game_x-self.tempX)
                        if self.ia.board.changePosition(position,self.tempY,self.tempX):
                            self.ia.board.changeRole()
                            if self.ia.board.whether_win() is True:
                                QMessageBox.about(self, 'Congratulation', "Win!!!!")
                                wd.close()
                                print("hello")
                            self.ia.board.changeRole()
                            self.ia.minmax()
                            self.ia.board.changeRole()
                            if self.ia.board.whether_win() is True:
                                QMessageBox.about(self, 'Congratulation', "Lose!!!")
                                wd.close()
                                return
                            self.ia.board.changeRole()
                            self.changeStatus=0
            self.repaint(0, 0, 700, 700)
            self.ia.board.prt()
            print()


    def flash(self):
        if self.flash_cnt <= 5:
            # 执行闪烁
            self.flash_cnt = self.flash_cnt + 1
            self.repaint(0, 0, 700, 700)
        else :
            self.end_timer.stop()
            self.flash_cnt=0
    def btn1_clicked(self):
       difficulty.show()
       login.close()

    def btn2_clicked(self):
        login.close()

    def btn3_clicked(self):
        wd.show()
        difficulty.close()
        self.ia.depth=2

    def btn4_clicked(self):
        wd.show()
        difficulty.close()
        self.ia.depth = 3


    def btn5_clicked(self):
        wd.show()
        difficulty.close()
        self.ia.depth = 4

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = First()
    difficulty=Second()
    c = Controller()
    ia = IA(c)
    wd = Window(ia)
    login.btn1.clicked.connect(wd.btn1_clicked)
    login.btn2.clicked.connect(wd.btn2_clicked)
    difficulty.btn3.clicked.connect(wd.btn3_clicked)
    difficulty.btn4.clicked.connect(wd.btn4_clicked)
    difficulty.btn5.clicked.connect(wd.btn5_clicked)
    sys.exit(app.exec_())

