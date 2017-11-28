class Controller():

    # returns: one of Tetris.LEFT, Tetris.RIGHT, Tetris.DOWN, Tetris.DROP,
    #   Tetris.ROTATE, Tetris.NOP
    # board: a numpy array representing the current board
    def getMove(self, board):
        raise Exception("Abstract function not implemented")
