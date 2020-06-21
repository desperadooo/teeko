from random import *


class IA:
    def __init__(self, board):
        self.depth = 2  # Game difficulty
        self.board = board # Controller
        self.weights = [
            [4, 6, 5, 6, 4],
            [6, 10, 10, 10, 6],
            [5, 10, 12, 10, 5],
            [6, 10, 10, 10, 6],
            [4, 6, 5, 6, 4]
        ]
        self.turn = 0

    # Who's moving the records?
    def addTurn(self):
        if self.board.turn==1:
            self.turn +=1

    def first_step(self):
        x = randint(0, 4)
        y = randint(0, 4)
        self.board.putFlag(y, x)
        self.turn = self.turn + 2

    def minmax(self):
        IAmin = 5000
        alpha = -5000
        beta = 5000
        if self.turn < 8:  # For the first 8 times, all positions on the map are estimated, and the AI takes the max layer and the player takes the min layer.
            max_y = 0  # initial position
            max_x = 0
            for y in range(5):
                for x in range(5):  # Traversing the map
                    if self.board.coordinate[y][x] == 0:  # If it's equal to zero, it means there are no discs in the point, so you can do a child node search with an IA of 2.
                        self.board.coordinate[y][x] = 2  # Take your place on the map first.
                        tmp = self.max(self.depth - 1, alpha, beta)
                        self.board.coordinate[y][x] = 0  # Put the map location back.
                        if tmp < IAmin:  # If the situation gets better, we'll take it.
                            IAmin = tmp
                            max_x = x
                            max_y = y
            #self.board.coordinate[max_y][max_x] = 2
            self.board.putFlag(max_y,max_x)
            self.turn += 2
        else:  # 8次以后 只能移动棋子
            max_x = 0
            max_y = 0
            dic = 0
            for y in range(5):
                for x in range(5):
                    if self.board.coordinate[y][x] == 2:
                        position = self.board.getPossiblePosition(y, x)
                        for direction in position:
                            ab=self.board.changePosition(direction, y, x)
                            tmp = self.max(self.depth - 1, alpha, beta)
                            self.board.changeRole()
                            self.board.changePosition(10-direction, ab[0], ab[1])  # restore to the original state
                            self.board.changeRole()
                            if tmp < IAmin:
                                dic = direction
                                IAmin = tmp
                                max_x = x
                                max_y = y
            self.board.changePosition(dic, max_y, max_x)
            self.turn += 2

    def min(self, current_depth,alpha,beta):
        if current_depth == 0 :
            return self.value(current_depth)
        if self.board.whether_win() is True :
            return self.value(current_depth)
        self.board.changeRole()
        if self.board.whether_win() is True:
            self.board.changeRole()
            return self.value(current_depth)
        self.board.changeRole()
        IAmin = 5000
        if current_depth > 0 and self.turn <8:
            for y in range(5):
                for x in range(5):
                    if self.board.coordinate[y][x] == 0:
                        self.board.coordinate[y][x] = 2
                        beta = self.max(current_depth - 1,alpha,beta)
                        self.board.coordinate[y][x] = 0
                        tmp = beta
                        if tmp < IAmin:
                            IAmin = tmp
                        if alpha >= beta :
                            return beta
        else:
            for y in range(5):
                for x in range(5):
                    if self.board.coordinate[y][x] == 2:
                        position = self.board.getPossiblePosition(y, x)
                        for direction in position:
                            ab=self.board.changePosition(direction, y, x)
                            beta = self.max(current_depth - 1,alpha,beta)
                            self.board.changeRole()
                            self.board.changePosition(10-direction, ab[0], ab[1])
                            self.board.changeRole()
                            tmp = beta
                            if tmp < IAmin:
                                IAmin = tmp
                            if alpha >= beta:
                                return beta
        return IAmin

    def max(self, current_depth,alpha,beta):
        if  current_depth == 0:
            return self.value(current_depth)
        self.board.changeRole()
        if self.board.whether_win() is True :
            self.board.changeRole()
            return self.value(current_depth)
        self.board.changeRole()
        if self.board.whether_win() is True :
            return self.value(current_depth)
        IAmax = -5000
        if current_depth > 0 and self.turn < 8:
            for x in range(5):
                for y in range(5):
                    if self.board.coordinate[y][x] == 0:
                        self.board.coordinate[y][x] = 1
                        alpha = self.min(current_depth - 1,alpha,beta)
                        self.board.coordinate[y][x] = 0
                        tmp = alpha
                        if tmp > IAmax:
                            IAmax = tmp
                        if alpha >= beta:
                            return alpha
        else:
            for y in range(5):
                for x in range(5):
                    if self.board.coordinate[y][x] == 1:
                        position = self.board.getPossiblePosition(y, x)
                        for direction in position:
                            ab=self.board.changePosition(direction, y, x)
                            alpha = self.min(current_depth - 1,alpha,beta)
                            self.board.changeRole()
                            self.board.changePosition(10-direction, ab[0], ab[1])
                            self.board.changeRole()
                            tmp = alpha
                            if tmp > IAmax:
                                IAmax = tmp
                            if alpha >= beta:
                                return alpha
        return IAmax

    def value(self, current_depth):
        value = 0
        if self.board.whether_win():
            if self.board.turn==1:
                value += 2500 + 5*current_depth
            else:
                value -= 2000 + 5*current_depth
        self.board.changeRole()
        if self.board.whether_win():
            if self.board.turn==1:
                value += 2500 + 5*current_depth
            else:
                value -= 2000 + 5*current_depth
        self.board.changeRole()
        for i in self.board.player:
            if i!=0:
                i=i-1
                value += 2*self.playeraround(i%5, int((i - i % 5) / 5))
                i=i+1
        for i in self.board.robot:
            if i!=0:
                i=i-1
                value -= 2*self.robotaround(i%5, int((i - i % 5) / 5))
                i=i+1
        if self.board.turn==2:
            if self.board.nearlyWin():
                if self.board.turn==1:
                    value += 500
                else:
                    value -= 500
        return value

    def robotaround(self, y, x):
        notrevalue = 0
        for i in range(10):
            if i != 5 and i != 0:
                position = self.board.getPossibleCheckPosition(y,x)
                for i in position:
                    self.board.checkPosition(i, y, x)
                    if self.board.coordinate[y][x] == 0:
                        notrevalue += int(self.weights[y][x]/2)
                    elif self.board.coordinate[y][x] == 1:
                        notrevalue += 0
                    else:
                        notrevalue += self.weights[y][x]
        notrevalue += self.weights[y][x]
        return notrevalue

    def playeraround(self, y, x):
        notrevalue = 0
        for i in range(10):
            if i != 5 and i != 0:
                position = self.board.getPossibleCheckPosition(y, x)
                for i in position:
                    self.board.checkPosition(i, y, x)
                    if self.board.coordinate[y][x] == 0:
                        notrevalue += int(self.weights[y][x]/2)
                    elif self.board.coordinate[y][x] == 2:
                        notrevalue += 0
                    else:
                        notrevalue += self.weights[y][x]
        return notrevalue

