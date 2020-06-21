from PyQt5.QtWidgets import QMainWindow,QPushButton,QLabel
from PyQt5.QtGui import  QPalette, QBrush, QPixmap

class First(QMainWindow):

  def __init__(self):
    super().__init__()

    self.initUI()

  def initUI(self):
    self.btn1 = QPushButton("Start", self)
    self.btn2 = QPushButton("Close", self)
    self.btn1.move(300, 200)
    self.btn1.setStyleSheet( "QPushButton:hover{color:grey}"
                              "QPushButton{background-color:rgb(211,211,211)}"
                              "QPushButton{border:2px}"
                              "QPushButton{border-radius:10px}"
                              "QPushButton{padding:2px 4px}")
    self.btn2.move(300, 250)
    self.btn2.setStyleSheet( "QPushButton:hover{color:grey}"
                              "QPushButton{background-color:rgb(211,211,211)}"
                              "QPushButton{border:2px}"
                              "QPushButton{border-radius:10px}"
                              "QPushButton{padding:2px 4px}")
    self.label = QLabel(self)
    self.label.setText('Teeko')
    self.label.setGeometry(300, 400, 300, 300)
    self.label.setStyleSheet('font-size:40px;color:white;font-family:Arial ')
    palette = QPalette()
    palette.setBrush(QPalette.Window, QBrush(QPixmap('imgs/blue.png')))
    self.setPalette(palette)
    self.setFixedSize(700, 700)
    self.setWindowTitle('Teeko Gamer')
    self.show()

class Second(QMainWindow):

  def __init__(self):
    super().__init__()

    self.initUI()

  def initUI(self):
    self.btn3 = QPushButton("Easy", self)
    self.btn3.setStyleSheet( "QPushButton:hover{color:grey}"
                              "QPushButton{background-color:rgb(211,211,211)}"
                              "QPushButton{border:2px}"
                              "QPushButton{border-radius:10px}"
                              "QPushButton{padding:2px 4px}")
    self.btn4 = QPushButton("Medium", self)
    self.btn4.setStyleSheet( "QPushButton:hover{color:grey}"
                              "QPushButton{background-color:rgb(211,211,211)}"
                              "QPushButton{border:2px}"
                              "QPushButton{border-radius:10px}"
                              "QPushButton{padding:2px 4px}")
    self.btn5 = QPushButton("Hard", self)
    self.btn5.setStyleSheet( "QPushButton:hover{color:grey}"
                              "QPushButton{background-color:rgb(211,211,211)}"
                              "QPushButton{border:2px}"
                              "QPushButton{border-radius:10px}"
                              "QPushButton{padding:2px 4px}")
    self.btn3.move(300, 200)
    self.btn4.move(300, 250)
    self.btn5.move(300, 300)
    self.label = QLabel(self)
    self.label.setText('Teeko')
    self.label.setGeometry(300, 400, 200, 200)
    self.label.setStyleSheet('font-size:35px;color:white;font-family:Arial ')
    palette = QPalette()
    palette.setBrush(QPalette.Window, QBrush(QPixmap('imgs/blue.png')))
    self.setPalette(palette)
    self.setFixedSize(700, 700)
    self.setWindowTitle('Teeko Gamer')


