from automatedTetris import RandomController, AutomatedTetris, AutomatedTetrisWindow

controller = RandomController()
autoTetris = AutomatedTetris(controller)
AutomatedTetrisWindow(autoTetris).play()
