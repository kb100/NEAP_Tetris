from automatedTetris import TetrisMovie, RandomController, AutomatedTetris, AutomatedTetrisWindow
import random
import cProfile, pstats
# plays randomly until it gets a nonzero score, then saves the game
def saveRandomGame():
    controller = RandomController() #replace with neural network
    score = 0
    n = 0
    while score == 0:
        random.seed(n)
        autoTetris = AutomatedTetris(controller, initrandomstate=random.getstate())
        autoTetris.play()
        score = autoTetris.score()
        n += 1
    print("Final score was ", autoTetris.score())
    print("It took {} trials".format(n))
    autoTetris.saveGame("test.game")

cProfile.run('saveRandomGame()', 'profile')
p = pstats.Stats('profile')
p.strip_dirs().sort_stats('time').print_stats(10)


#play back a saved game
#TetrisMovie("test.game", shadowsEnabled=True).play()

#watch a controller play live
#controller = RandomController()
#autoTetris = AutomatedTetris(controller)
#AutomatedTetrisWindow(autoTetris).play()

