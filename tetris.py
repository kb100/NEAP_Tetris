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
    POSSIBLE_MOVES = [LEFT, RIGHT, ROTATE, DOWN]

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
        self.EMPTY_ROW = np.zeros((1,Tetris.DEFAULT_COLS))
        self.ONES = np.ones_like(self.board)
        self.gameOver = False
        self.isPaused = False
    
    def togglePaused(self):
        self.isPaused = not self.isPaused

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
        return row >= 0 and np.all(self.board[row])

    def rowIsEmpty(self, row):
        return row >= 0 and not np.any(self.board[row])

    def pointsFromCompleteRows(self, deletedCount):
        return [0, 40, 100, 300, 1200][deletedCount]

    def deleteCompleteRows(self):
        i = self.rows-1
        deleted = 0
        while i >= 0:
            while self.rowIsComplete(i-deleted):
                deleted += 1
            if deleted > 0:
                if i-deleted >= 0:
                    self.board[i] = self.board[i-deleted] 
                else:
                    self.board[i] = self.EMPTY_ROW
            i -= 1
        self.score += self.pointsFromCompleteRows(deleted)
        return deleted

    def dropFallingPiece(self):
        while self.step(): pass

    def tryMoveLeft(self):
        return self.fallingPiece.tryMoveLeft()

    def tryMoveRight(self):
        return self.fallingPiece.tryMoveRight()

    def tryMoveDown(self):
        return self.fallingPiece.tryMoveDown()

    def tryRotateClockwise(self):
        return self.fallingPiece.tryRotateClockwise()

    def tryRotateCounterClockwise(self):
        return self.fallingPiece.tryRotateCounterClockwise()

    def makeBoard(self, rows, cols):
        return np.zeros((rows,cols), dtype=int)

    def boardAsArray(self):
        arr = np.minimum(self.ONES, self.board)
        for r,c in self.fallingPiece:
            arr[r,c] = 1
        return arr.ravel()

    def topFourNonemptyRowsAndShadowAsArray(self):
        row = 0
        while self.rowIsEmpty(row) and row+4 < self.rows:
            row += 1
        arr = np.minimum(self.ONES, self.board)
        for r,c in self.fallingPiece.shadow():
            arr[r,c] = 1
        arr = arr[row:row+4]
        return arr.ravel()
         
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
            self.board[row][col] = self.fallingPiece.rep

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
        rows, cols = self.maskdim
        self.mask = [(cols-c-1, r) for r,c in self.mask]
        self.maskdim = (cols, rows)
        self.anchor = (cols-self.anchor[1]-1, self.anchor[0]) 

    def rotateClockwise(self):
        rows, cols = self.maskdim
        self.mask = [(c,rows-r-1) for r,c in self.mask]
        self.maskdim = (cols, rows)
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

    def tryMoveTo(self, newRow, newCol):
        row, col = self.row, self.col
        self.moveTo(newRow, newCol)
        result = self.fitsOnBoard()
        if not result:
            self.moveTo(row, col)
        return result

    def tryMoveUp(self): return self.tryMoveTo(self.row-1, self.col)
    def tryMoveDown(self): return self.tryMoveTo(self.row+1, self.col)
    def tryMoveLeft(self): return self.tryMoveTo(self.row, self.col-1)
    def tryMoveRight(self): return self.tryMoveTo(self.row, self.col+1)

    def tryRotateClockwise(self):
        self.rotateClockwise()
        result = self.fitsOnBoard()
        if not result:
            self.rotateCounterClockwise()
        return result

    def tryRotateCounterClockwise(self):
        self.rotateCounterClockwise()
        result = self.fitsOnBoard()
        if not result:
            self.rotateClockwise()
        return result

    def __iter__(self):
        ar, ac = self.anchor
        r, c = self.row, self.col
        mr, mc = self.maskdim
        for row, col in self.mask:
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
                or board[row][col] != 0:
                return False
        return True

class Tetrimino_I(Tetrimino):
    def __init__(self, game, x, y):
        Tetrimino.__init__(self, game, x, y)
        self.mask = [(0,0), (0,1), (0,2), (0,3)]
        self.maskdim = (1,4)
        self.anchor = (0,1)
        self.color = "red"
        self.rep = 1

    # Override
    def rotateCounterClockwise(self):
        self.rotateClockwise()

    # Override    
    def rotateClockwise(self):
        if self.maskdim[0] == 1:
            Tetrimino.rotateClockwise(self)
        else:
            Tetrimino.rotateCounterClockwise(self)

class Tetrimino_J(Tetrimino):
    def __init__(self, game, x, y):
        Tetrimino.__init__(self, game, x, y)
        self.mask = [(0,0),(1,0),(1,1),(1,2)]
        self.maskdim = (2,3)
        self.anchor = (1,1)
        self.color = "yellow"
        self.rep = 2

class Tetrimino_L(Tetrimino):
    def __init__(self, game, x, y):
        Tetrimino.__init__(self, game, x, y)
        self.mask = [(0,2),(1,0),(1,1),(1,2)]
        self.maskdim = (2,3)
        self.anchor = (1,1)
        self.color = "magenta"
        self.rep = 3

class Tetrimino_O(Tetrimino):
    def __init__(self, game, x, y):
        Tetrimino.__init__(self, game, x, y)
        self.mask = [(0,0),(0,1),(1,0),(1,1)]
        self.maskdim = (2,2)
        self.anchor = (0,0)
        self.color = "blue"
        self.rep = 4
    
    # Overrides
    def rotateClockwise(self): pass
    def rotateCounterClockwise(self): pass

class Tetrimino_S(Tetrimino):
    def __init__(self, game, x, y):
        Tetrimino.__init__(self, game, x, y)
        self.mask = [(0,1),(0,2),(1,0),(1,1)]
        self.maskdim = (2,3)
        self.anchor = (1,1)
        self.color = "cyan"
        self.rep = 5

class Tetrimino_T(Tetrimino):
    def __init__(self, game, x, y):
        Tetrimino.__init__(self, game, x, y)
        self.mask = [(0,1),(1,0),(1,1),(1,2)]
        self.maskdim = (2,3)
        self.anchor = (1,1)
        self.color = "lime"
        self.rep = 6

class Tetrimino_Z(Tetrimino):
    def __init__(self, game, x, y):
        Tetrimino.__init__(self, game, x, y)
        self.mask = [(0,0),(0,1),(1,1),(1,2)]
        self.maskdim = (2,3)
        self.anchor = (1,1)
        self.color = "orange"
        self.rep = 7

