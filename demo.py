from automatedTetris import TetrisMovie, RandomController, AutomatedTetris, AutomatedTetrisWindow

# plays randomly until it gets a nonzero score, then saves the game
def saveRandomGame():
    controller = RandomController() #replace with neural network
    score = 0
    while score == 0:
        autoTetris = AutomatedTetris(controller)
        autoTetris.play()
        score = autoTetris.score()
    print("Final score was ", autoTetris.score())
    autoTetris.saveGame("test.game")

#saveRandomGame()

#play back a saved game
#TetrisMovie("test.game", shadowsEnabled=True).play()

#watch a controller play live
controller = RandomController()
autoTetris = AutomatedTetris(controller)
AutomatedTetrisWindow(autoTetris).play()

