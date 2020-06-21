from PyQt5.QtWidgets import QMessageBox


class Controller:
    def __init__(self):
        self.coordinate = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        self.flagH=0#the number of the human's flag
        self.flagR=0#the number of the robot's flag
        self.turn=1#Point out whose turn it is
        self.player=[0,0,0,0]#stock the position of the human's flags(1-25)
        self.robot=[0,0,0,0] #stock the position of the robot's flags(1-25)

    #Change player
    def changeTurn(self,name):
        if name == 0:#present human
            self.turn=1
        elif name == 1:#present robot
            self.turn=2
        else:
            print("Error!")

    def changeRole(self):
        if self.turn==1:
            self.turn=2
        elif self.turn==2:
            self.turn=1

    def reInit(self):
        self.coordinate = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        self.flagH = 0
        self.flagR = 0
        self.turn = 1
        self.player = [0, 0, 0, 0]
        self.robot = [0, 0, 0, 0]

    #display the array of coordinates
    def prt(self):
        for i in range(5):
            for j in range(5):
                print(self.coordinate[i][j],' ', end="")
            print()
        #print("\n")

    #put the position into array
    def stockPosition(self, lastIndex, x, y):
        index = x*5+y+1
        if self.turn == 1:
            self.player[self.player.index(lastIndex)] = index
        if self.turn == 2:
            self.robot[self.robot.index(lastIndex)] = index

    #The player choose a position to put the flag
    def putFlag(self,x,y):
        if x<0 or x>4 or y<0 or y>4:
            print("Out of border")
            return False
        elif self.turn==1:
            if self.flagH==4:
                print("You already have 4 flags")
                return False
            elif self.coordinate[x][y]!=0:
                print("You can't put the flag in this position")
                return False
            else:
                self.coordinate[x][y]=self.turn
                self.flagH += 1
                self.stockPosition(0,x,y)
                self.changeRole()
                return True
        elif self.turn==2:
            if self.flagR==4:
                print("You already have 4 flags")
                return False
            elif self.coordinate[x][y]!=0:
                print("You can't put the flag in this position")
                return False
            else:
                self.coordinate[x][y]=self.turn
                self.flagR+=1
                self.stockPosition(0,x,y)
                self.changeRole()
                return True
    #change the value of the position
    def changeState(self, lastIndex,x, y):
        if self.turn==1:
            if self.coordinate[x][y]==0:
                self.coordinate[x][y]=1
                self.stockPosition(lastIndex,x,y)
            else:
                print("Error!You can't move to this position")
        elif self.turn==2:
            if self.coordinate[x][y]==0:
                self.coordinate[x][y]=2
                self.stockPosition(lastIndex,x,y)
            else:
                print("Error!You can't move to this position")

    #return the possible positions to put the flag
    def getPossiblePosition(self,x,y):
        position=[]
        if x-1>=0:
            if y-1>=0:
                if self.coordinate[x-1][y-1]==0:
                    position.append(1)
            if self.coordinate[x-1][y]==0:
                    position.append(2)
            if y+1<=4:
                if self.coordinate[x-1][y+1]==0:
                    position.append(3)
        if y-1>=0:
            if self.coordinate[x][y-1]==0:
                position.append(4)
        if y+1<=4:
            if self.coordinate[x][y+1] == 0:
                position.append(6)
        if x+1<=4:
            if y-1>=0:
                if self.coordinate[x+1][y-1] == 0:
                    position.append(7)
            if self.coordinate[x+1][y] == 0:
                position.append(8)
            if y+1<=4:
                if self.coordinate[x+1][y+1] == 0:
                    position.append(9)
        return position

    #The player move the flag
    def changePosition(self,p,x,y):
        if x>=0 and x<=4 and y>=0 and y<=4 and self.coordinate[x][y]==self.turn:
            position=self.getPossiblePosition(x,y)
            if p in position:
                self.changePositionHelper(p,x,y)
                self.changeRole()
                self.coordinate[x][y]=0
                if p == 1:
                    return [x - 1, y - 1]
                elif p == 2:
                    return [x - 1, y]
                elif p == 3:
                    return [x - 1, y + 1]
                elif p == 4:
                    return [x, y - 1]
                elif p == 6:
                    return [x, y + 1]
                elif p == 7:
                    return [x + 1, y - 1]
                elif p == 8:
                    return [x + 1, y]
                elif p == 9:
                    return [x + 1, y + 1]

            else:
                print("You can't move the flag to this position")
                return False
        else:
            if self.coordinate[x][y]!=self.turn:
                print("This place has been taken")
            else:
                print("x,y is out of border")
            return False

    def changePositionHelper(self,p,x,y):
        lastIndex=x*5+y+1
        if p==1:
            self.changeState(lastIndex,x-1,y-1)
        elif p==2:
            self.changeState(lastIndex,x-1,y)
        elif p==3:
            self.changeState(lastIndex,x-1,y+1)
        elif p==4:
            self.changeState(lastIndex,x,y-1)
        elif p==6:
            self.changeState(lastIndex,x,y+1)
        elif p==7:
            self.changeState(lastIndex,x+1,y-1)
        elif p==8:
            self.changeState(lastIndex,x+1,y)
        elif p==9:
            self.changeState(lastIndex,x+1,y+1)

    def getPossibleCheckPosition(self, x, y):
        position = []
        if x - 1 >= 0:
            if y - 1 >= 0:
                if self.coordinate[x - 1][y - 1] == 0:
                    position.append(1)
            if self.coordinate[x - 1][y] == 0:
                position.append(2)
            if y + 1 <= 4:
                if self.coordinate[x - 1][y + 1] == 0:
                    position.append(3)
        if y - 1 >= 0:
            if self.coordinate[x][y - 1] == 0:
                position.append(4)
        if y + 1 <= 4:
            if self.coordinate[x][y + 1] == 0:
                position.append(6)
        if x + 1 <= 4:
            if y - 1 >= 0:
                if self.coordinate[x + 1][y - 1] == 0:
                    position.append(7)
            if self.coordinate[x + 1][y] == 0:
                position.append(8)
            if y + 1 <= 4:
                if self.coordinate[x + 1][y + 1] == 0:
                    position.append(9)
        return position

    def checkPosition(self,p,x,y):
            if p in range(10) and p != 0 and p != 5:
                if x >= 0 and x <= 4 and y >= 0 and y <= 4:
                    return self.checkPositionHelper(p,x,y)
            else:
                return 3

    def checkPositionHelper(self,p,x,y):
        if p==1:
            return self.coordinate[x-1][y-1]
        elif p==2:
            return self.coordinate[x-1][y]
        elif p==3:
            return self.coordinate[x-1][y+1]
        elif p==4:
            return self.coordinate[x][y-1]
        elif p==6:
            return self.coordinate[x][y+1]
        elif p==7:
            return self.coordinate[x+1][y-1]
        elif p==8:
            return self.coordinate[x+1][y]
        elif p==9:
            return self.coordinate[x+1][y+1]


    #judge whether the player win
    def whether_win(self):
        for i in range(5):
            for j in range(5):
                if self.coordinate[i][j] == self.turn:
                    x=i
                    y=j
                    break
            else:
                continue
            break
        return self.winHelper(x, y)


    def winHelper(self,x,y):
        if x < 4 and y < 4 and self.coordinate[x][y + 1] == self.coordinate[x + 1][y] == self.coordinate[x + 1][y + 1] == self.turn:  # carré
            return True
        elif y < 2 and self.coordinate[x][y + 1] == self.coordinate[x][y + 2] == self.coordinate[x][y + 3] == self.turn:  # ligne
            return True
        elif x< 2 and self.coordinate[x + 1][y] == self.coordinate[x + 2][y] == self.coordinate[x + 3][y] == self.turn:  # colonne
            return True
        elif x < 2 and y < 2 and self.coordinate[x + 1][y + 1] == self.coordinate[x + 2][y + 2] == self.coordinate[x + 3][y + 3] == self.turn:  # diagonale
            return True
        elif x < 2 and y > 2 and self.coordinate[x + 1][y - 1] == self.coordinate[x + 2][y - 2] == self.coordinate[x + 3][y - 3] == self.turn:  # diagonale
            return True
        else:
            return False
    #juge
    def nearlyWin(self):
        for i in range(5):
            for j in range(5):
                if self.coordinate[i][j] == self.turn:
                    x=i
                    y=j
                    if self.nearlyWinHelper(x,y) == True:
                        return self.nearlyWinHelper(x,y)
                    else:
                        continue
        return False

    def nearlyWinHelper(self,x,y):
        if x < 4 and y < 4 and self.coordinate[x][y + 1] == self.coordinate[x + 1][y] == self.turn:  # carré
            return True
        elif x < 4 and y < 4 and self.coordinate[x][y + 1] == self.coordinate[x + 1][y + 1] == self.turn:  # carré
            return True
        elif x < 4 and y < 4 and self.coordinate[x + 1][y] == self.coordinate[x + 1][y + 1] == self.turn:  # carré
            return True
        elif x < 4 and y <= 4 and self.coordinate[x + 1][y - 1] == self.coordinate[x + 1][y] == self.turn:  # carré
            return True
        elif y <= 2 and self.coordinate[x][y + 1] == self.coordinate[x][y + 2] == self.turn:  # ligne
            return True
        elif x <= 2 and self.coordinate[x + 1][y] == self.coordinate[x + 2][y] == self.turn:  # colonne
            return True
        elif x <= 2 and y <= 2 and self.coordinate[x + 1][y + 1] == self.coordinate[x + 2][y + 2] == self.turn:  # diagonale
            if (x == 2 and y == 0) or (x == 0 and y == 2):
                return False
            else:
                return True
        elif x <= 2 and y >= 2 and self.coordinate[x + 1][y - 1] == self.coordinate[x + 2][y - 2] == self.turn:  # diagonale
            if (x == 0 and y == 2) or (x == 2 and y == 4):
                return False
            else:
                return True
        else:
            return False

    def moveHelper(self,diffX,diffY):
        if diffX == -1 and diffY == -1:
            return 1
        elif diffX == -1 and diffY == 0:
            return 2
        elif diffX == -1 and diffY == 1:
            return 3
        elif diffX == 0 and diffY == -1:
            return 4
        elif diffX == 0 and diffY == 1:
            return 6
        elif diffX == 1 and diffY == -1:
            return 7
        elif diffX == 1 and diffY == 0:
            return 8
        elif diffX ==1 and diffY == 1:
            return 9
        else:
            return False

