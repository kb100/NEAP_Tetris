from tetris import *


def loop1():
    J = Tetrimino_J(None, 0,1)
    for i in range(1000000):
        n1 = 0
        n2 = 0
        for r,c in J:
            n1 += r
            n2 += c

def loop2():
    J = Tetrimino_J(None, 0,1)
    for i in range(1000000):
        n1 = 0
        n2 = 0
        ar, ac = J.anchor
        r, c = J.row, J.col
        for row,col in J.mask:
            n1 += r + row-ar
            n2 += c + col-ac

def loop3():
    J = Tetrimino_J(None, 0,1)
    for i in range(1000000):
        n1 = 0
        n2 = 0
        ar, ac = J.anchor
        r, c = J.row, J.col
        n1 += r + J.mask[0][0]-ar
        n2 += c + J.mask[0][1]-ac

        n1 += r + J.mask[1][0]-ar
        n2 += c + J.mask[1][1]-ac

        n1 += r + J.mask[2][0]-ar
        n2 += c + J.mask[2][1]-ac

        n1 += r + J.mask[3][0]-ar
        n2 += c + J.mask[3][1]-ac


class test1():
    masks = [1,2]
    def __init__(self):
        self.mask = test1.masks[0]

class test2(test1):
    masks = [2,3]

x = test2()
print(x.mask)

t = Tetris()
for clazz in t.tetriminos:
    print(clazz)
    x = clazz(None, 0,0)
    print("anchors = [",end="")
    for i in range(4):
        print(x.anchor, end=",")
        x.rotateClockwise()
    print("]")

