from tetris import Tetris
from playTetris import TetrisWindow
import random
import pickle
from controller import Controller

class AutomatedTetris():

    def __init__(self, controller, initrandomstate=None, recordMoves=True):
        self.controller = controller
        self.tetris = Tetris(initrandomstate=initrandomstate)
        self.recordMoves = recordMoves
        self.moves = []

    def step(self):
        if self.tetris.gameOver:
            return False
        m = self.controller.getMove(self.tetris.boardAsArray())
        if self.recordMoves:
            self.moves.append(m)
        if m == Tetris.LEFT:
            self.tetris.tryMoveLeft()
        elif m == Tetris.RIGHT:
            self.tetris.tryMoveRight()
        elif m == Tetris.ROTATE:
            self.tetris.tryRotateClockwise()
        elif m == Tetris.DOWN:
            self.tetris.tryMoveDown()
        elif m == Tetris.DROP:
            self.tetris.dropFallingPiece()
        elif m == Tetris.NOP:
            self.tetris.step()
        return True

    def score(self):
        return self.tetris.score

    def play(self, maxMoves=-1):
        moveCount = 0
        while not self.tetris.gameOver and moveCount != maxMoves:
            moveCount += 1
            self.step()

    def saveGame(self, filename):
        with open(filename, "wb") as f:
            pickle.dump((self.tetris.initrandomstate,self.moves), f) 

class RandomController(Controller):
    def getMove(self, board):
        return random.choice([Tetris.LEFT, Tetris.RIGHT, Tetris.ROTATE,
            Tetris.DOWN, Tetris.DROP, Tetris.NOP])

class AutomatedTetrisMovie(AutomatedTetris):

    class MovieController(Controller):
        def __init__(self, moves):
            self.moves = moves
            self.index = 0

        def getMove(self, board):
            if self.index >= len(self.moves):
                return Tetris.NOP
            move = self.moves[self.index]
            self.index += 1
            return move

        def step(self):
            if self.index < len(self.moves):
                AutomatedTetris.step(self)

    def __init__(self, filename):
        with open(filename, "rb") as f:
            initrandomstate, moves = pickle.load(f)
        controller = AutomatedTetrisMovie.MovieController(moves)
        AutomatedTetris.__init__(self, controller, initrandomstate)

class AutomatedTetrisWindow(TetrisWindow):
    
    def __init__(self, autoTetris, shadowsEnabled=False):
        TetrisWindow.__init__(self, shadowsEnabled, automated=True)
        self.delay = 1000
        self.autoTetris = autoTetris
        self.game = autoTetris.tetris
        self.refreshTimerFired()
        self.bind("<Key>", self.keyPressed)
        self.canvas.after(self.delay, self.stepMovie)

    def stepMovie(self):
        if not self.game.isPaused:
            self.autoTetris.step()
            self.needToRedraw = True 
        self.canvas.after(self.delay, self.stepMovie)
        
    def keyPressed(self, event):
        print("key pressed with char", event.char, "keysym", event.keysym)
        if event.keysym == "p":
            self.game.togglePaused()
        elif self.game.gameOver or self.game.isPaused:
            return
        elif event.keysym == "minus":
            if self.delay > 50:
                self.delay -= 50
        elif event.keysym == "plus":
            self.delay += 50
        self.needToRedraw = True

    def play(self):
        self.mainloop()

class TetrisMovie(AutomatedTetrisWindow):

        def __init__(self, filename, shadowsEnabled=False):
            autoTetris = AutomatedTetrisMovie(filename)
            AutomatedTetrisWindow.__init__(self, autoTetris, shadowsEnabled)
