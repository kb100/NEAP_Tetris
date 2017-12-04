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
        self.numTetriminos = len(self.tetriminos)
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
        success = self.fallingPiece.tryMoveDown()
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
        return self.step()

    def tryRotateClockwise(self):
        return self.fallingPiece.tryRotateClockwise()

    def tryRotateCounterClockwise(self):
        return self.fallingPiece.tryRotateCounterClockwise()

    def makeBoard(self, rows, cols):
        return np.zeros((rows,cols), dtype=int)

    def boardAsArray(self):
        arr = np.minimum(self.ONES, self.board)
        fp = self.fallingPiece
        ar, ac = fp.anchor
        dr, dc = fp.row-ar, fp.col-ac
        for r,c in fp.mask:
            arr[r+dr,c+dc] = 1
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
        clazz = self.tetriminos[self.rng.randint(0, self.numTetriminos-1)]
        self.fallingPiece = clazz(self,-self.maxDimOfTetrimino+1,self.cols//2-1)
        for i in range(self.rng.randint(0,3)):
            self.fallingPiece.rotateClockwise()
        while self.fallingPiece.minRow() != 0:
            self.fallingPiece.moveDown()
    
    def placeFallingPiece(self):
        fp = self.fallingPiece
        ar, ac = fp.anchor
        dr, dc = fp.row-ar, fp.col-ac
        rep = fp.rep
        for r,c in fp.mask:
            self.board[r+dr][c+dc] = rep

    def dim(self):
        return self.rows, self.cols

class Tetrimino:
    color = "black"
    shadowColor = "black"

    def __init__(self, game, row, col):
        self.row, self.col = row, col
        self.game = game
        self.moveTo(row, col)
        self.mask = self.masks[0]
        self.anchor = self.anchors[0]
        self.maskIndex = 0

    def rotateCounterClockwise(self):
        self.maskIndex += 3
        self.maskIndex %= 4
        self.mask = self.masks[self.maskIndex]
        self.anchor = self.anchors[self.maskIndex]

    def rotateClockwise(self):
        self.maskIndex += 1
        self.maskIndex %= 4
        self.mask = self.masks[self.maskIndex]
        self.anchor = self.anchors[self.maskIndex]

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
        dr, dc = self.row-ar, self.col-ac
        for row, col in self.mask:
            #yield (self.row + row - self.anchor[0], self.col+col-self.anchor[1])
            yield (dr+row, dc+col) 
    
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
        ar, ac = self.anchor
        dr, dc = self.row-ar, self.col-ac
        for row, col in self.mask:
            xr, xc = dr+row, dc+col
            if not (0 <= xr < rows and 0 <= xc < cols) or board[xr][xc]:
                return False
        return True

class Tetrimino_I(Tetrimino):
    masks = [
                [(0, 0), (0, 1), (0, 2), (0, 3)],
                [(0, 0), (1, 0), (2, 0), (3, 0)],
                [(0, 0), (0, 1), (0, 2), (0, 3)],
                [(0, 0), (1, 0), (2, 0), (3, 0)]
            ]
    anchors = [(0, 1),(1, 0),(0, 1),(1, 0)]
    color = "red"
    rep = 1

class Tetrimino_J(Tetrimino):
    masks = [
                [(0, 0), (1, 0), (1, 1), (1, 2)],
                [(0, 1), (0, 0), (1, 0), (2, 0)],
                [(1, 2), (0, 2), (0, 1), (0, 0)],
                [(2, 0), (2, 1), (1, 1), (0, 1)]
            ]
    anchors = [(1, 1),(1, 0),(0, 1),(1, 1)]
    color = "yellow"
    rep = 2

class Tetrimino_L(Tetrimino):
    masks = [
                [(0, 2), (1, 0), (1, 1), (1, 2)],
                [(2, 1), (0, 0), (1, 0), (2, 0)],
                [(1, 0), (0, 2), (0, 1), (0, 0)],
                [(0, 0), (2, 1), (1, 1), (0, 1)]
            ]
    anchors = [(1, 1),(1, 0),(0, 1),(1, 1)]
    color = "magenta"
    rep = 3

class Tetrimino_O(Tetrimino):
    masks = [
                [(0, 0), (0, 1), (1, 0), (1, 1)],
                [(0, 0), (0, 1), (1, 0), (1, 1)],
                [(0, 0), (0, 1), (1, 0), (1, 1)],
                [(0, 0), (0, 1), (1, 0), (1, 1)]
            ]
    anchors = [(0, 0),(0, 0),(0, 0),(0, 0)]
    color = "blue"
    rep = 4
    
    # Overrides
    def rotateClockwise(self): pass
    def rotateCounterClockwise(self): pass

class Tetrimino_S(Tetrimino):
    masks = [
                [(0, 1), (0, 2), (1, 0), (1, 1)],
                [(1, 1), (2, 1), (0, 0), (1, 0)],
                [(1, 1), (1, 0), (0, 2), (0, 1)],
                [(1, 0), (0, 0), (2, 1), (1, 1)]
            ]
    anchors = [(1, 1),(1, 0),(0, 1),(1, 1)]
    color = "cyan"
    rep = 5

class Tetrimino_T(Tetrimino):
    masks = [
                [(0, 1), (1, 0), (1, 1), (1, 2)],
                [(1, 1), (0, 0), (1, 0), (2, 0)],
                [(1, 1), (0, 2), (0, 1), (0, 0)],
                [(1, 0), (2, 1), (1, 1), (0, 1)]
            ]
    anchors = [(1, 1),(1, 0),(0, 1),(1, 1)]
    color = "lime"
    rep = 6

class Tetrimino_Z(Tetrimino):
    masks = [
                [(0, 0), (0, 1), (1, 1), (1, 2)],
                [(0, 1), (1, 1), (1, 0), (2, 0)],
                [(1, 2), (1, 1), (0, 1), (0, 0)],
                [(2, 0), (1, 0), (1, 1), (0, 1)]
            ]
    anchors = [(1, 1),(1, 0),(0, 1),(1, 1)]
    color = "orange"
    rep = 7

