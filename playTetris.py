from tkinter import Tk, Canvas, ALL, BOTH, CENTER, LEFT, SW, NW, NE, SE
from tetris import Tetris

class TetrisWindow(Tk):
    DEFAULT_WIDTH = 500
    DEFAULT_HEIGHT = 300

    REFRESH_RATE = 60
    REFRESH_MILLIS = 1000 // REFRESH_RATE 

    def __init__(self, shadowsEnabled=True, automated=False):
        self.game = Tetris()

        Tk.__init__(self)
        self.canvas = Canvas(self, 
            width=TetrisWindow.DEFAULT_WIDTH,
            height=TetrisWindow.DEFAULT_HEIGHT)
        self.canvas.pack(fill=BOTH, expand=1)
        self.needToRedraw = False
        self.shadowsEnabled = shadowsEnabled

        if not automated:
            self.refreshTimerFired()
            self.canvas.after(1000, self.gameTimerFired)
            self.bind("<Button-1>", self.mousePressed)
            self.bind("<Key>", self.keyPressed)
        self.canvas.bind("<Configure>", self.onResize)

    def getBoardBoundingBox(self):
        x0, y0 = 0, 0
        x1, y1 = self.canvas.winfo_width(), self.canvas.winfo_height()
        rows, cols = self.game.dim()
        desiredRatio = rows / cols
        boundingRatio = (y1-y0) / (x1-x0)
        if boundingRatio > desiredRatio:
            y1 = y0 + (x1-x0)*desiredRatio
            y1 = int(y1)
        else:
            x1 = x0 + (y1-y0)/desiredRatio
            x1 = int(x1)
        return (x0, y0, x1, y1)

    def getCellBoundingBox(self, row, col):
        x0, y0, x1, y1 = self.getBoardBoundingBox()
        rows, cols = self.game.dim()
        dx = (x1-x0) / cols
        dy = (y1-y0) / rows 
        x2, y2 = x0 + dx*col, y0 + dy*row
        return (x2, y2, x2 + dx, y2 + dy)

    def drawCell(self, row, col, color):
        x0, y0, x1, y1 = self.getCellBoundingBox(row, col)
        board = self.game.board
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def repToColor(self, rep, clist=["gray", "red", "yellow", "magenta", "blue", "cyan", "lime", "orange"]):
        return clist[rep]

    def drawBoard(self):
        board = self.game.board
        for row in range(len(board)):
            for col in range(len(board[0])):
                self.drawCell(row, col, self.repToColor(board[row][col]))

    def drawFallingPiece(self):
        for row, col in self.game.fallingPiece:
            self.drawCell(row, col, self.game.fallingPiece.color) 

    def drawFallingPieceShadow(self):
        for row, col in self.game.fallingPiece.shadow():
            self.drawCell(row, col, self.game.fallingPiece.shadowColor)

    def drawGame(self):
        self.canvas.delete(ALL)
        self.drawBoard()
        if self.shadowsEnabled:
            self.drawFallingPieceShadow()
        self.drawFallingPiece()
        self.drawScore()
        if self.game.gameOver:
            self.drawGameOverScreen()
        elif self.game.isPaused:
            self.drawPausedScreen()

    def drawScore(self):
        x0, y0, x1, y1 = self.getBoardBoundingBox()
        text = "Score: {}".format(self.game.score)
        fontName = "DejaVu sans mono"
        fontSize =  (y1-y0)//20 #in pixels
        self.canvas.create_text(x0, y0,
                text=text,
                anchor=NW,
                font=(fontName, -fontSize, "bold"),
                fill="white")

    def drawGameOverScreen(self):
        x0, y0, x1, y1 = self.getBoardBoundingBox()
        cx, cy = (x0+x1)/2, (y0+y1)/2
        text = "Game Over!\nHit r to restart."
        fontName = "DejaVu sans mono"
        fontSize =  (y1-y0)//20 #in pixels
        self.canvas.create_text(cx, cy,
                text=text,
                justify=CENTER,
                font=(fontName, -fontSize, "bold"),
                fill="white")

    def drawPausedScreen(self):
        x0, y0, x1, y1 = self.getBoardBoundingBox()
        cx, cy = (x0+x1)/2, (y0+y1)/2
        text = "Paused.\nHit p to unpause."
        fontName = "DejaVu sans mono"
        fontSize =  (y1-y0)//20 #in pixels
        self.canvas.create_text(cx, cy,
                text=text,
                justify=CENTER,
                font=(fontName, -fontSize, "bold"),
                fill="white")

    def onResize(self, event):
        width, height = event.width, event.height
        self.canvas.config(width=width, height=height)
        self.needToRedraw = True

    def gameTimerFired(self):
        if not self.game.isPaused:
            self.game.step()
            self.needToRedraw = True
        delay = self.game.stepDelay
        self.canvas.after(delay, self.gameTimerFired)

    def refreshTimerFired(self):
        if self.needToRedraw: 
            self.drawGame()
            self.needToRedraw = False
        delay = TetrisWindow.REFRESH_MILLIS
        self.canvas.after(delay, self.refreshTimerFired)

    def mousePressed(self, event):
        pass
        #print("mouse pressed at ", event.x, event.y)

    def keyPressed(self, event):
        #print("key pressed with char", event.char, "keysym", event.keysym)
        if event.keysym == 'r':
            self.game = Tetris(self.game.rows, self.game.cols)
        elif event.keysym == "p":
            self.game.togglePaused()
        elif self.game.gameOver or self.game.isPaused:
            return
        elif event.keysym == "Left":
            self.game.tryMoveLeft()
        elif event.keysym == "Right":
            self.game.tryMoveRight()
        elif event.keysym == "Down":
            self.game.tryMoveDown()
        elif event.keysym == "Up":
            self.game.tryRotateClockwise()
        elif event.keysym == "space":
            self.game.dropFallingPiece()
        self.needToRedraw = True

def main():
    TetrisWindow().mainloop()
