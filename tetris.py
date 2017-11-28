import random
import numpy as np

class Tetris:
    DEFAULT_ROWS = 15
    MIN_ROWS = 4
    MIN_COLS = 4
    DEFAULT_COLS = 10
    DEFAULT_EMPTY_COLOR = "gray"
    DEFAULT_STEP_DELAY = 1000 #millis
    LEFT = 0
    RIGHT = 1
    ROTATE = 2
    DOWN = 3
    DROP = 4
    NOP = 5

    def __init__(self, rows=None, cols=None, initrandomstate=None):
        if rows == None: rows = Tetris.DEFAULT_ROWS 
        if cols == None: cols = Tetris.DEFAULT_COLS
        self.rows, self.cols = rows, cols
        self.score = 0
        self.emptyColor = Tetris.DEFAULT_EMPTY_COLOR
        self.rng = random.Random()
        if initrandomstate:
            self.rng.setstate(initrandomstate)
        self.initrandomstate = self.rng.getstate()
        self.newBoard()
        self.stepDelay = Tetris.DEFAULT_STEP_DELAY
        self.tetriminos = (Tetrimino_T, Tetrimino_O, Tetrimino_I, Tetrimino_J,
                Tetrimino_L, Tetrimino_S, Tetrimino_Z)
        self.maxDimOfTetrimino = self.computeMaxDimOfTetrimino()
        self.newFallingPiece()
        self.gameOver = False
        self.isPaused = False
    
    def togglePaused(self):
        self.isPaused = not self.isPaused

    def setDim(self, rows, cols):
        rows = max(rows, Tetris.MIN_ROWS)
        cols = max(cols, Tetris.MIN_COLS)
        drow = rows-self.rows
        dcol = cols-self.cols
        if drow < 0:
            self.board[0:-drow] = []
        elif drow > 0:
            self.board[0:0] = self.makeBoard(drow, self.cols) 
        if dcol < 0:
            for row in self.board:
                row[dcol:] = []
        elif dcol > 0:
            for row in self.board:
                row += [self.emptyColor] * dcol
        self.rows, self.cols = rows, cols
        if not self.fallingPiece.fitsOnBoard():
            self.newFallingPiece()

    def computeMaxDimOfTetrimino(self):
        maximum = 0
        for clazz in self.tetriminos:
            t = clazz(self,0,0)
            if len(t.mask) > maximum:
                maximum = len(t.mask)
            if len(t.mask[0]) > maximum:
                maximum = len(t.mask[0])
        return maximum

    def step(self):
        if self.gameOver:
            return False
        success = self.tryMoveDown()
        if not success:
            self.placeFallingPiece()
            self.deleteCompleteRows()
            self.newFallingPiece()
            if not self.fallingPiece.fitsOnBoard():
                self.gameOver = True
        return success

    def rowIsComplete(self, row):
        return self.emptyColor not in self.board[row]

    def pointsFromCompleteRows(self, deletedCount):
        return [0, 40, 100, 300, 1200][deletedCount]

    def deleteCompleteRows(self):
        self.board[:] = [self.board[row] for row in range(self.rows) 
                if not self.rowIsComplete(row)]
        deletedCount = self.rows - len(self.board)
        self.score += self.pointsFromCompleteRows(deletedCount)
        self.board[0:0] = [[self.emptyColor]*self.cols 
                for row in range(deletedCount)] 
        return deletedCount

    def dropFallingPiece(self):
        while self.step(): pass

    def tryMoveLeft(self):
        if self.fallingPiece.canMoveLeft():
            self.fallingPiece.moveLeft()
            return True
        return False

    def tryMoveRight(self):
        if self.fallingPiece.canMoveRight():
            self.fallingPiece.moveRight()
            return True
        return False

    def tryMoveDown(self):
        if self.fallingPiece.canMoveDown():
            self.fallingPiece.moveDown()
            return True
        return False

    def tryRotateClockwise(self):
        if self.fallingPiece.canRotateClockwise():
            self.fallingPiece.rotateClockwise()
            return True
        return False

    def tryRotateCounterClockwise(self):
        if self.fallingPiece.canRotateCounterClockwise():
            self.fallingPiece.rotateCounterClockwise()
            return True
        return False

    def makeBoard(self, rows, cols):
        board = []
        for i in range(rows):
            board.append([self.emptyColor] * cols)
        return board

    def boardAsArray(self):
        arr = np.zeros(self.dim(), dtype=np.float64)
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] != self.emptyColor:
                    arr[row, col] = 1.0
        for row, col in self.fallingPiece:
            arr[row, col] = 1.0

        return arr
         
    def newBoard(self):
        self.board = self.makeBoard(self.rows, self.cols)

    def newFallingPiece(self):
        numTetriminos = len(self.tetriminos)

        clazz = self.tetriminos[self.rng.randint(0, numTetriminos-1)]
        self.fallingPiece = clazz(self,-self.maxDimOfTetrimino+1,self.cols//2-1)
        for i in range(self.rng.randint(0,3)):
            self.fallingPiece.rotateClockwise()
        while self.fallingPiece.minRow() != 0:
            self.fallingPiece.moveDown()
    
    def placeFallingPiece(self):
        for row, col in self.fallingPiece:
            self.board[row][col] = self.fallingPiece.color

    def dim(self):
        return self.rows, self.cols

class Tetrimino:
    def __init__(self, game, row, col):
        self.row, self.col = row, col
        self.game = game
        self.moveTo(row, col)
        self.color = "black"
        self.shadowColor = "black"

    def canRotateClockwise(self):
        self.rotateClockwise()
        result = self.fitsOnBoard()
        self.rotateCounterClockwise()
        return result
    
    def canRotateCounterClockwise(self):
        self.rotateCounterClockwise()
        result = self.fitsOnBoard()
        self.rotateClockwise()
        return result

    def rotateCounterClockwise(self):
        rows = len(self.mask)
        cols = len(self.mask[0])
        self.mask = [
                [self.mask[row][cols-col-1] for row in range(rows)] 
                for col in range(cols) ]
        self.anchor = (cols-self.anchor[1]-1, self.anchor[0]) 

    def rotateClockwise(self):
        rows = len(self.mask)
        cols = len(self.mask[0])
        self.mask = [ 
                [self.mask[rows-row-1][col]  for row in range(rows)] 
                for col in range(cols)] 
        self.anchor = (self.anchor[1], rows-self.anchor[0]-1)

    def canMoveTo(self, newRow, newCol):
        row, col = self.row, self.col
        self.moveTo(newRow, newCol)
        result = self.fitsOnBoard()
        self.moveTo(row, col)
        return result
    
    def canMoveDown(self): return self.canMoveTo(self.row+1, self.col)
    def canMoveLeft(self): return self.canMoveTo(self.row, self.col-1)
    def canMoveRight(self): return self.canMoveTo(self.row, self.col+1)

    def moveTo(self, row, col):
        self.row = row
        self.col = col

    def moveUp(self): self.moveTo(self.row-1, self.col)
    def moveDown(self): self.moveTo(self.row+1, self.col)
    def moveLeft(self): self.moveTo(self.row, self.col-1)
    def moveRight(self): self.moveTo(self.row, self.col+1)

    def __iter__(self):
        ar, ac = self.anchor
        r, c = self.row, self.col
        for row in range(len(self.mask)):
            for col in range(len(self.mask[0])):
                if self.mask[row][col]:
                    yield (r + row-ar, c + col-ac) 
    
    def shadow(self):
        originalRow, originalCol = self.row, self.col
        dRow = 0 
        if self.fitsOnBoard():
            while self.fitsOnBoard():
                dRow += 1
                self.moveDown()
            self.moveUp()
            dRow -= 1
            self.moveTo(originalRow, originalCol)
        for row, col in self:
            yield row+dRow, col

    def minRow(self):
        minimum = self.game.rows
        for row, col in self:
            if row < minimum:
                minimum = row
        return minimum

    def fitsOnBoard(self):
        game = self.game
        board = game.board
        rows, cols = game.dim()
        for row, col in self:
            if not (0 <= row < rows and 0 <= col < cols) \
                or board[row][col] != game.emptyColor:
                return False
        return True

class Tetrimino_I(Tetrimino):
    def __init__(self, game, x, y):
        Tetrimino.__init__(self, game, x, y)
        self.mask = [[True,True,True,True]]
        self.anchor = (0,1)
        self.color = "red"

    # Override
    def rotateCounterClockwise(self):
        self.rotateClockwise()

    # Override    
    def rotateClockwise(self):
        if len(self.mask) == 1:
            Tetrimino.rotateClockwise(self)
        else:
            Tetrimino.rotateCounterClockwise(self)

class Tetrimino_J(Tetrimino):
    def __init__(self, game, x, y):
        Tetrimino.__init__(self, game, x, y)
        self.mask = [[True,False,False],
                     [True,True,True]]
        self.anchor = (1,1)
        self.color = "yellow"

class Tetrimino_L(Tetrimino):
    def __init__(self, game, x, y):
        Tetrimino.__init__(self, game, x, y)
        self.mask = [[False,False,True],
                     [True,True,True]]
        self.anchor = (1,1)
        self.color = "magenta"

class Tetrimino_O(Tetrimino):
    def __init__(self, game, x, y):
        Tetrimino.__init__(self, game, x, y)
        self.mask = [[True, True],
                     [True,True]]
        self.anchor = (0,0)
        self.color = "blue"
    
    # Overrides
    def rotateClockwise(self): pass
    def rotateCounterClockwise(self): pass

class Tetrimino_S(Tetrimino):
    def __init__(self, game, x, y):
        Tetrimino.__init__(self, game, x, y)
        self.mask = [[False,True,True],
                     [True,True,False]]
        self.anchor = (1,1)
        self.color = "cyan"

class Tetrimino_T(Tetrimino):
    def __init__(self, game, x, y):
        Tetrimino.__init__(self, game, x, y)
        self.mask = [[False,True,False],
                     [True,True,True]]
        self.anchor = (1,1)
        self.color = "lime"

class Tetrimino_Z(Tetrimino):
    def __init__(self, game, x, y):
        Tetrimino.__init__(self, game, x, y)
        self.mask = [[True,True,False],
                     [False,True,True]]
        self.anchor = (1,1)
        self.color = "orange"

